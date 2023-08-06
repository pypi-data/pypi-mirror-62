import random
import string

from .parse import QueryParser
from .ast import Validate

from .ast.ast import *  # TODO Why?


"""
    Modifies parsed ASTs to augment with information needed
    to support differential privacy.  Uses a matching Schema
    object which contains metadata necessary for differential
    privacy, such as min/max, cardinality, and key columns.

    This routine is intended to be used prior to post-processing
    with random noise generation.

"""
class Rewriter:
    def __init__(self, metadata):
        self.metadata = metadata
        self.max_contrib = 5  # max projection magnitude for an individual

    """
        Takes an expression for a noisy mean and rewrites
        to a noisy sum and a noisy count
    """
    def calculate_avg(self, exp, scope):
        expr = exp.expression
        quant = exp.quantifier

        sum_expr = self.push_sum_or_count(AggFunction("SUM", quant, expr), scope)
        count_expr = self.push_sum_or_count(AggFunction("COUNT", quant, expr), scope)

        new_exp = NestedExpression(ArithmeticExpression(sum_expr, "/", count_expr))
        return new_exp

    """
        Takes an expression for a noisy mean and rewrites
        to a noisy sum and a noisy count
    """
    def calculate_variance(self, exp, scope):
        expr = exp.expression
        quant = exp.quantifier

        avg_of_square = self.calculate_avg(AggFunction("AVG", quant, ArithmeticExpression(expr, '*', expr)), scope)
        avg = self.calculate_avg(AggFunction("AVG", quant, expr), scope)
        avg_squared = ArithmeticExpression(avg, '*', avg)

        new_exp = ArithmeticExpression(avg_of_square, "-", avg_squared)
        return new_exp

    """
        Takes an expression for a noisy mean and rewrites
        to a noisy sum and a noisy count
    """
    def calculate_stddev(self, exp, scope):
        expr = AggFunction('STD', exp.quantifier, exp.expression)
        var_expr = self.calculate_variance(expr, scope)

        new_exp = MathFunction("SQRT", var_expr)
        return new_exp

    """
        Push a sum or count expression to child scope
        and convert to a sum
    """
    def push_sum_or_count(self, exp, scope):
        new_name = scope.push_name(AggFunction(exp.name, exp.quantifier, exp.expression))

        new_exp = AggFunction("SUM", None, Column(new_name))
        return new_exp

    """
        rewrite AVG, VAR, etc. and push all sum or count
        to child scope, preserving all other portions of
        expression
    """
    def rewrite_outer_named_expression(self, ne, scope):
        name = ne.name
        exp = ne.expression
        if type(exp) is not AggFunction:
            outer_col_exps = exp.find_nodes(Column, AggFunction)
        else:
            outer_col_exps = []
        if type(exp) is Column:
            outer_col_exps += [exp]
        for outer_col_exp in outer_col_exps:
            new_name = scope.push_name(Column(outer_col_exp.name))
            outer_col_exp.name = new_name
        agg_exps = exp.find_nodes(AggFunction)
        if type(exp) is AggFunction:
            agg_exps = agg_exps + [exp]
        for agg_exp in agg_exps:
            child_agg_exps = agg_exp.find_nodes(AggFunction)
            if len(child_agg_exps) > 0:
                raise ValueError("Cannot have nested aggregate functions: " + str(agg_exp))
            agg_func = agg_exp.name
            if agg_func in ["SUM", "COUNT"]:
                new_exp = self.push_sum_or_count(agg_exp, scope)
            elif agg_func == "AVG":
                new_exp = self.calculate_avg(agg_exp, scope)
            elif agg_func in ["VAR","VARIANCE"]:
                new_exp = self.calculate_variance(agg_exp, scope)
            elif agg_func in ["STD","STDDEV"]:
                new_exp = self.calculate_stddev(agg_exp, scope)
            else:
                raise ValueError("We don't know how to rewrite aggregate function: " + str(agg_exp))
            agg_exp.name = ""
            agg_exp.quantifier = None
            agg_exp.expression = new_exp
        return NamedExpression(name, exp)


    def query(self, query):
        query = QueryParser(self.metadata).query(str(query))
        Validate().validateQuery(query, self.metadata)

        child_scope = Scope()
        # we make sure aggregates are in select scope for subqueries
        if query.agg is not None:
            for ge in query.agg.groupingExpressions:
                child_scope.push_name(ge.expression)

        select = Seq([self.rewrite_outer_named_expression(ne, child_scope) for ne in query.select.namedExpressions])
        select = Select(None, select)

        subquery = Query(child_scope.select(), query.source, query.where, query.agg, query.having, None)
        subquery = self.exact_aggregates(subquery)
        subquery = [AliasedRelation(subquery, "exact_aggregates")]

        q = Query(select, From(subquery), None, query.agg, None, query.order)

        return QueryParser(self.metadata).query(str(q))

    def exact_aggregates(self, query):

        key_col = self.key_col(query)

        child_scope = Scope()

        keycount_expr = AggFunction("COUNT", "DISTINCT", Column(key_col))
        child_scope.push_name(keycount_expr.expression)
        keycount = NamedExpression("keycount", keycount_expr) # need to either treat this as reserved or pass through to outer

        select = Seq([keycount] + [self.rewrite_outer_named_expression(ne, child_scope) for ne in query.select.namedExpressions])
        select = Select(None, select)

        subquery = Query(child_scope.select(), query.source, query.where, query.agg, query.having, None)
        subquery = self.per_key_random(subquery)
        subquery = [AliasedRelation(subquery, "per_key_random")]

        filtered = Where(BooleanCompare(Column("per_key_random.row_num"), "<=", Literal(str(self.max_contrib), self.max_contrib)))
        return Query(select, From(subquery), filtered, query.agg, None, None)

    def per_key_random(self, query):
        key_col = self.key_col(query)

        select = Seq([NamedExpression(None, AllColumns()), NamedExpression("row_num", Expression("ROW_NUMBER() OVER (PARTITION BY {0} ORDER BY random())".format(key_col)))])
        select = Select(None, select)

        subquery = self.per_key_clamped(query)
        subquery = [AliasedRelation(subquery, "per_key_clamped")]

        return Query(select, From(subquery), None, None, None, None)


    def per_key_clamped(self, query):
        key_col = self.key_col(query)

        child_scope = Scope()

        keygroup = [GroupingExpression(Column(key_col))] + (query.agg.groupingExpressions.seq if query.agg is not None else [])
        new_agg = Aggregate(Seq(keygroup))

        relations = query.source.relations

        select = Seq([self.clampExpression(ne, relations, child_scope) for ne in query.select.namedExpressions])
        select = Select(None, select)

        subquery = Query(child_scope.select(), query.source, query.where, None, None, None)
        subquery = [AliasedRelation(subquery, "clamped")]

        return Query(select, From(subquery), None, new_agg, None, None)


    """
        Lookup the expression referenced in each named expression and
        write a clamped select for it, using the schema
    """
    def clampExpression(self, ne, relations, scope):
        exp = ne.expression
        cols = exp.find_nodes(Column)
        if type(exp) is Column:
            cols += [exp]
        for col in cols:
            colname = col.name
            minval = None
            maxval = None
            sym = col.symbol(relations)
            if sym.valtype in ["float", "int"] and not sym.unbounded:
                minval = sym.minval
                maxval = sym.maxval
                if minval is None or sym.is_key:
                    cexpr = Column(colname)
                    ce_name = scope.push_name(cexpr, str(colname))
                else:
                    clamped_string = "CASE WHEN {0} < {1} THEN {1} WHEN {0} > {2} THEN {2} ELSE {0} END".format(str(colname), minval, maxval)
                    cexpr = Expression(clamped_string)
                    ce_name = scope.push_name(cexpr, str(colname))
            else:
                cexpr = Column(colname)
                ce_name = scope.push_name(cexpr, str(colname))
            col.name = ce_name
        return ne

    """
        Return the key column, given a from clause
    """
    def key_col(self, query):
        rsyms = query.source.relations[0].all_symbols(AllColumns())
        tcsyms = [r for name, r in rsyms if type(r) is TableColumn]
        keys = [str(tc) for tc in tcsyms if tc.is_key]
        if len(keys) > 1:
            raise ValueError("We only know how to handle tables with one key: " + str(keys))
        elif len(keys) < 1:
            raise ValueError("No key column available in query relations")

        kp = keys[0].split(".")
        return kp[len(kp) - 1]



"""
    A name scope for a select query
"""
class Scope:
    def __init__(self):
        self.expressions = {}

    def select(self, quantifier=None):
        return Select(quantifier, [NamedExpression(name, self.expressions[name]) for name in self.expressions.keys()])

    """
        Returns a named expression from an expression, using
        an existing name if already provided in this scope,
        or generating a new name and adding to the names
        dictionary if the expression does not exist in scope.
    """
    def push_name(self, expression, proposed=None):
        # see if the proposed name is taken
        if proposed is not None:
            if proposed in self.expressions:
                if self.expressions[proposed] == expression:
                    return proposed
                else:
                    pass
            else:
                self.expressions[proposed] = expression
                return proposed

        # see if the expression has been used 
        names = [name for name in self.expressions.keys() if self.expressions[name] == expression]
        if len(names) > 0:
            return names[0]

        # see if the expression has been used under the symbol name
        proposed = expression.symbol_name()
        if proposed in self.expressions:
            if self.expressions[proposed] == expression:
                return proposed
            else:
                pass
        else:
            self.expressions[proposed] = expression
            return proposed

        # Expression hasn't been used, but name is taken. Generate random.
        while not proposed in self.expressions:
            proposed = ''.join(random.choice(string.ascii_letters) for i in range(7))

        self.expressions[proposed] = expression
        return proposed
