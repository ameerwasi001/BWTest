import ast
from astor import to_source
import sys

class MyOptimizer(ast.NodeTransformer):

    def visit_Num(self, node):
        if isinstance(node.n, int):
            return ast.Call(func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='number', ctx=ast.Load()),
                            args=[node], keywords=[])
        return node

    def visit_Str(self, node):
        return ast.Call(func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='string', ctx=ast.Load()),
                args=[node], keywords=[])
        return node

tree = ast.parse(open(sys.argv[1], "r").read())
optimizer = MyOptimizer()
tree = optimizer.visit(tree)
print(to_source(tree))
open("Extensions.py", "w").write(to_source(tree))
