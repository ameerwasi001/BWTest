from Values import *
from Lexer import *
from Tokens import *
from Parser_ import *
from Errors import *
from Extensions import Helper
import copy
import traceback

class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def register(self, res):
        if res.error: self.error = res.error
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return (
            self.error or
            self.loop_should_continue or
            self.loop_should_break
        )


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, identifier):
        value = self.symbols.get(identifier, None)
        if value == None and self.parent:
            return self.parent.get(identifier)
        return value

    def set(self, identifier, value):
        self.symbols[identifier] = value
        return value

    def delete(self, identifier):
        value = self.get(identifier)
        del self.symbols[identifier]
        return value

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f"visit_{type(node).__name__} is undefined")

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.number).set_pos(node.pos_start, node.pos_end).set_context(context)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.value).set_pos(node.pos_start, node.pos_end).set_context(context)
        )

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.number, context))
        if res.should_return(): return res
        error = None
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.type == TT_NOT:
            number, error = number.notted()
        if error: res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        identifier = node.identifier.value
        value = res.register(self.visit(node.value, context))
        if res.should_return(): return res
        value = context.symbol_table.set(identifier, value)
        return res.success(value)

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        identifier = node.identifier.value
        value = context.symbol_table.get(identifier)
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                context,
                f"Undefined variable {identifier}"
            ))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left, context))
        if res.error: return res
        right = res.register(self.visit(node.right, context))
        if res.error: return res
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.lt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.lte(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.gt(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.gte(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.ee(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.ne(right)
        elif node.op_tok.type == TT_OR:
            result, error = left.ored(right)
        elif node.op_tok.type == TT_AND:
            result, error = left.anded(right)

        if error: return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()
        for condition, expression in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res
            if condition_value.is_true():
                expr_value = res.register(self.visit(expression, context))
                if res.should_return(): return res
                return res.success(expr_value)
        if node.else_case:
            else_value = expr_value = res.register(self.visit(node.else_case, context))
            if res.should_return(): return res
            return res.success(else_value)
        return res.success(nil)

    def visit_WhileNode(self, node, context):
        res = RTResult()
        condition = res.register(self.visit(node.condition, context))
        if res.should_return(): return res
        while True:
            condition = res.register(self.visit(node.condition, context))
            if res.should_return(): return res
            if not condition.is_true(): break
            res.register(self.visit(node.body, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
            if res.loop_should_continue:
                continue
            if res.loop_should_break:
                break
        return res.success(nil)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = node.args[:]
        kwargs = copy.deepcopy(node.kwargs)
        for k in kwargs:
            kwargs[k] = res.register(self.visit(kwargs[k], context))
            if res.should_return(): return res
        index = 0
        while index<len(args):
            args[index] = res.register(self.visit(args[index], context))
            if res.should_return(): return res
            index+=1
        try:
            getattr(helpers, node.identifier.value) (*args, **kwargs)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("Python Error,", e)
            res.failure(RTError(
                node.pos_start, node.pos_end,
                context,
                f'Selenium Error, {e}'
            ))
        return res.success(nil)

    def visit_EveryNode(self, node, context):
        res = RTResult()
        times = res.register(self.visit(node.times, context))
        if res.should_return(): return res
        if not node.times:
            res.failure(RTError(
                node.pos_start, node.pos_end,
                context,
                "Expected time to be a number"
            ))
        times = times.value
        new_context = Context(id(times), context, node.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        i=0
        while i<=times:
            new_context.symbol_table.set("current", Number(i))
            body = res.register(self.visit(node.body, new_context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
            if res.loop_should_continue:
                continue
            if res.loop_should_break:
                break
            i+=1
        return res.success(body)


    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []
        for node in node.elements:
            elements.append(res.register(self.visit(node, context)))
            if res.should_return(): return res
        return res.success(
                List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
            )

    def visit_TryNode(self, node, context):
        res = RTResult()
        try_block = res.register(self.visit(node.try_block, context))
        ret_value = try_block if node.may_return else nil
        if res.error:
            res.reset()
            except_block = res.register(self.visit(node.except_block, context))
            if res.error: return res
            ret_value = except_block if node.may_return else nil
        return res.success(ret_value)

    def visit_RunNode(self, node, context):
        res = RTResult()
        string = res.register(self.visit(node.fn, context))
        try:
            file = open(string.value, 'r').read()
        except:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                context,
                f"{string} file doesn't exist"
            ))
        fresult, ferror = run(string.value, file)
        if ferror: print(ferror.as_string())
        return res.success(nil)

    def visit_RestartNode(self, node, context):
        return RTResult().success_continue()

    def visit_StopNode(self, node, context):
        return RTResult().success_break()

helpers = Helper()
global_symbol_table = SymbolTable()
global_symbol_table.set('false', false)
global_symbol_table.set('true', true)
global_symbol_table.set('nil', nil)

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.generate_tokens()
    if error: return None, error
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    interpreter = Interpreter()
    context = Context(fn)
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error

while True:
    inp = input("BWTst >")
    result, error = run("<module>", inp)
    if error:
        print(error.as_string())
    else:
        if len(result.elements) == 1:
            print(result.elements[0])
        else:
            print(result)
