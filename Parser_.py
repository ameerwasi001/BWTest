from Tokens import *
from Nodes import *
from Errors import *

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

#Parsers
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.next_tok_idx = 0
        self.third_tok_idx = 1
        self.advance()

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx<len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        if self.next_tok_idx >= 0 and self.next_tok_idx<len(self.tokens):
            self.next_tok = self.tokens[self.next_tok_idx]
        if self.third_tok_idx >= 0 and self.third_tok_idx<len(self.tokens):
            self.third_tok = self.tokens[self.third_tok_idx]

    def advance(self):
        self.tok_idx += 1
        self.next_tok_idx += 1
        self.third_tok_idx += 1
        self.update_current_tok()

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', and '/'"
            ))
        return res

    def bin_op(self, func_a, ops, func_b):
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res
        pos_start = self.current_tok.pos_start.copy()
        if res.error: return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right, pos_start, self.current_tok.pos_end)
        return res.success(left)

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()
        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)
        more_statements = True
        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)
        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        if self.current_tok.matches(TT_KEYWORD, "restart"):
            self.advance()
            return res.success(RestartNode(pos_start, self.current_tok.pos_end.copy()))
        if self.current_tok.matches(TT_KEYWORD, "stop"):
            self.advance()
            return res.success(StopNode(pos_start, self.current_tok.pos_end.copy()))
        expr = res.register(self.expr())
        if res.error: return res
        return res.success(expr)


    def expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start
        if (self.current_tok.type == TT_IDENTIFIER) and (self.next_tok.type == TT_EQUALS):
            identifier = self.current_tok
            res.register_advancement()
            self.advance()
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            pos_end = self.current_tok.pos_end
            return res.success(VarAssignNode(identifier, expr, pos_start, pos_end))
        else:
            return self.bin_op(self.comp_expr, (TT_OR, TT_AND), self.comp_expr)

    def comp_expr(self):
        res = ParseResult()
        if self.current_tok.type == TT_NOT:
            pos_start = self.current_tok.pos_start.copy()
            unaryOp = self.current_tok
            res.register_advancement()
            self.advance()
            comp = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(unaryOp, comp, pos_start, self.current_tok.pos_end.copy()))
        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_LTE, TT_GT, TT_GTE), self.arith_expr))
        if res.error: return res
        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS), self.term)

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV), self.factor)

    def call(self):
        res = ParseResult()
        args = []
        kwargs = {}
        name = self.current_tok
        res.register_advancement()
        self.advance()
        pos_start = self.current_tok.pos_start
        if self.current_tok.type != TT_DARROW:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '=>'"
            ))
        res.register_advancement()
        self.advance()
        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"
            ))
        res.register_advancement()
        self.advance()
        if self.current_tok.type != TT_LPAREN:
            if self.next_tok.type != TT_SARROW:
                expr = res.register(self.expr())
                if res.error: return res
                args.append(expr)
            else:
                identifier = self.current_tok.value
                res.register_advancement()
                self.advance()
                if self.current_tok.type != TT_SARROW:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected '->'"
                        ))
                res.register_advancement()
                self.advance()
                expr = res.register(self.expr())
                if res.error: return res
                kwargs[identifier] = expr
            while (self.current_tok.type == TT_COMMA):
                res.register_advancement()
                self.advance()
                if self.next_tok.type == TT_SARROW:
                    identifier = self.current_tok.value
                    res.register_advancement()
                    self.advance()
                    if self.current_tok.type != TT_SARROW:
                        return res.failure(InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected '->'"
                            ))
                    res.register_advancement()
                    self.advance()
                    expr = res.register(self.expr())
                    if res.error: return res
                    kwargs[identifier] = expr
                else:
                    expr = res.register(self.expr())
                    if res.error: return res
                    args.append(expr)
        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')'"
            ))
        res.register_advancement()
        self.advance()
        return res.success(CallNode(name, args, kwargs, pos_start, self.current_tok.pos_end))


    def factor(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        if self.current_tok.type in (TT_PLUS, TT_MINUS):
            unaryOp = self.current_tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(unaryOp, factor, pos_start, self.current_tok.pos_end))
        if self.current_tok.type == TT_IDENTIFIER:
            pos_end = self.current_tok.pos_end.copy()
            if self.next_tok.type == TT_DARROW:
                return self.call()
            identifier = self.current_tok
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(identifier, pos_start, pos_end))
        if self.current_tok.type == TT_NUMBER:
            pos_end = self.current_tok.pos_end.copy()
            value = self.current_tok.value
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(value, pos_start, pos_end))
        elif self.current_tok.type == TT_STRING:
            pos_end = self.current_tok.pos_end.copy()
            value = self.current_tok.value
            res.register_advancement()
            self.advance()
            return res.success(StringNode(value, pos_start, pos_end))
        elif self.current_tok.type == TT_RPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
            res.register_advancement()
            self.advance()
            return res.success(expr)
        elif self.current_tok.matches(TT_KEYWORD, 'IF'):
            expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(expr)
        elif self.current_tok.matches(TT_KEYWORD, 'while'):
            expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(expr)
        elif self.current_tok.matches(TT_KEYWORD, 'run'):
            expr = res.register(self.run_expr())
            if res.error: return res
            return res.success(expr)
        elif self.current_tok.matches(TT_KEYWORD, 'every'):
            expr = res.register(self.every_expr())
            if res.error: return res
            return res.success(expr)
        return res.failure(InvalidSyntaxError(
            pos_start, self.current_tok.pos_end,
            "Expected NUMBER, IDENTIFIER, or '('"
        ))

    def every_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        if not self.current_tok.matches(TT_KEYWORD, 'every'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'every'"
            ))
        res.register_advancement()
        self.advance()
        if not self.current_tok.matches(TT_KEYWORD, 'time'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'time'"
            ))
        res.register_advancement()
        self.advance()
        if not self.current_tok.matches(TT_KEYWORD, 'in'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'in'"
            ))
        res.register_advancement()
        self.advance()
        times = res.register(self.expr())
        if res.error: return res
        if not self.current_tok.matches(TT_KEYWORD, 'times'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'times'"
            ))
        res.register_advancement()
        self.advance()
        if self.current_tok.type == TT_NEWLINE:
            body = res.register(self.statements())
            if res.error: return res
            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                ))
            res.register_advancement()
            self.advance()
        else:
            body = res.register(self.expr())
            if res.error: return res
        return res.success(EveryNode(times, body, pos_start, self.current_tok.pos_end.copy()))


    def run_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        if not self.current_tok.matches(TT_KEYWORD, 'run'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'run'"
            ))
        res.register_advancement()
        self.advance()
        fn = res.register(self.expr())
        if res.error: return res
        return res.success(RunNode(fn, pos_start, self.current_tok.pos_end.copy()))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None
        pos_start = self.current_tok.pos_start.copy()
        if not self.current_tok.matches(TT_KEYWORD, 'IF'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'IF'"
            ))
        res.register_advancement()
        self.advance()
        condition = res.register(self.expr())
        if res.error: return res
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'THEN'"
            ))
        res.register_advancement()
        self.advance()
        expr = res.register(self.statement())
        if res.error: return res
        cases.append((condition, expr))
        while self.current_tok.matches(TT_KEYWORD, 'ELSEIF'):
            res.register_advancement()
            self.advance()
            condition = res.register(self.expr())
            if res.error: return res
            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'THEN'"
                ))
            res.register_advancement()
            self.advance()
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr))
        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()
            else_case = res.register(self.statement())
        return res.success(IfNode(cases, else_case, pos_start, self.current_tok.pos_end.copy()))

    def while_expr(self):
        res = ParseResult()
        condition = None
        body = None
        pos_start = self.current_tok.pos_start.copy()
        if not self.current_tok.matches(TT_KEYWORD, 'while'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'while'"
            ))
        res.register_advancement()
        self.advance()
        condition = res.register(self.expr())
        if res.error: return res
        body = res.register(self.statements())
        if res.error: return res
        if not self.current_tok.matches(TT_KEYWORD, 'end'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'end'"
            ))
        res.register_advancement()
        self.advance()
        return res.success(WhileNode(condition, body, pos_start, self.current_tok.pos_end.copy()))
