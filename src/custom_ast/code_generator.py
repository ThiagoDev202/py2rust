from transpiler_ast import ProgramNode, AssignmentNode, PrintNode, IfNode, FunctionNode, ExpressionNode

def generate_rust(node):
    if isinstance(node, ProgramNode):
        return "\n".join(generate_rust(child) for child in node.children)
    elif isinstance(node, AssignmentNode):
        return f"let {node.identifier} = {generate_rust(node.expression)};"
    elif isinstance(node, PrintNode):
        return f"println!(\"{{}}\", {generate_rust(node.expression)});"
    elif isinstance(node, IfNode):
        if_body = "\n".join(generate_rust(stmt) for stmt in node.if_body)
        else_body = "\n    else {\n" + "\n".join(generate_rust(stmt) for stmt in node.else_body) + "\n    }" if node.else_body else ""
        return f"if {generate_rust(node.condition)} {{\n{if_body}\n}}{else_body}"
    elif isinstance(node, FunctionNode):
        body = "\n".join(generate_rust(stmt) for stmt in node.body)
        return f"fn {node.name}() {{\n{body}\n}}"
    elif isinstance(node, ExpressionNode):
        return node.expression
    return ""

def main(ast_root):
    rust_code = generate_rust(ast_root)
    print(rust_code)

if __name__ == "__main__":
    # Certifique-se de importar a AST correta de python_parser.py
    from python_parser import program_node as ast_root
    main(ast_root)
