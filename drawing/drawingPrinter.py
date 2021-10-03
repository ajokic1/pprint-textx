from textx.pprint import PrettyPrinter

def init_drawing_printer():
    printer = PrettyPrinter()
    printer.register_processor('Function', pprint_function)
    printer.register_processor('FunctionCall', pprint_function_call)

    return printer


def pprint_function(node, printer):
    function_name = node.name
    function_arguments = ', '.join(node.args)
    
    printer.append('\n\nfunction {} ({}) {{'.format(function_name, function_arguments))
    for statement in node.statements:
        printer.process_node(statement)
    printer.append('\n}')

def pprint_function_call(node, printer):
    function_name = node.name
    function_arguments = ', '.join(node.args)
    whitespaces = node.whitespaces_before
    printer.append('{}{}({});'.format(whitespaces, function_name, function_arguments))