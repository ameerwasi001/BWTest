#Nodes
class NumberNode:
    def __init__(self, number, pos_start, pos_end):
        self.number = number
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.number}"

class BinOpNode:
    def __init__(self, left, op_tok, right, pos_start, pos_end):
        self.left = left
        self.op_tok = op_tok
        self.right = right
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"({self.left}, {self.op_tok}, {self.right})"


class UnaryOpNode:
    def __init__(self, op_tok, number, pos_start, pos_end):
        self.op_tok = op_tok
        self.number = number
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{'Negative' if self.op_tok.type == TT_MINUS else 'Positive'} {self.number}"

class VarAssignNode:
    def __init__(self, identifier, expr, pos_start, pos_end):
        self.identifier = identifier
        self.value = expr
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.identifier} = {self.value}"

class VarAccessNode:
    def __init__(self, identifier, pos_start, pos_end):
        self.identifier = identifier
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.identifier } = ?"

class IfNode:
    def __init__(self, cases, else_case, pos_start, pos_end):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.cases} : {self.else_case}"

class ListNode:
    def __init__(self, elements, pos_start, pos_end):
        self.elements = elements
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'{", ".join([str(x) for x in self.elements])}'

class WhileNode:
    def __init__(self, condition, body, pos_start, pos_end):
        self.condition = condition
        self.body = body
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"while ({self.condition})"+"{"+f"{self.body}"+"}"

class RunNode:
    def __init__(self, fn, pos_start, pos_end):
        self.fn = fn
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"while ({self.condition})"+"{"+f"{self.body}"+"}"

class StringNode:
    def __init__(self, value, pos_start, pos_end):
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'{self.value}'

class CallNode:
    def __init__(self, identifier, args, kwargs, pos_start, pos_end):
        self.identifier = identifier
        self.args = args
        self.kwargs = kwargs
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        f"{self.identifier} ({self.args}, {self.kwargs})"

class TryNode(object):
    def __init__(self, try_block, except_block, may_return, pos_start, pos_end):
        self.try_block = try_block
        self.except_block = except_block
        self.may_return = may_return
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return "try {"+f"{self.try_block}"+"} except {"+f"{self.except_block}"+"}"


class RestartNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self, arg):
        return "restart"

class StopNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self, arg):
        return "stop"

class EveryNode:
    def __init__(self, times, body, pos_start, pos_end):
        self.times = times
        self.body = body
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"every time in {self.times} time; {self.body}; end"
