import os
from os.path import dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx.model import pprint_tree
from drawingPrinter import init_drawing_printer

THIS_FOLDER = dirname(__file__)

def main(debug=False):
    mm = metamodel_from_file('drawing.tx', debug=debug)
    proba_model = mm.model_from_file('drawingExample.txt')
    export_dot(mm, proba_model)

    print('\n\nORIGINAL:\n\n')
    printer = init_drawing_printer()
    printer.pprint_model(proba_model)

    # refactor_model_extract_method(proba_model, mm)
    # refactor_model_change_order(proba_model)

    # print('\n\nREFACTORED:\n\n')
    # printer.pprint_model(proba_model)

def refactor_model_change_order(model):
    model.functions.reverse()
    model._tx_pprint_data.reverse()

def refactor_model_extract_method(model, metamodel):
    existing_function = model.functions[0]
    
    # Create a new Function instance
    function_metaclass = existing_function.__class__
    new_function = function_metaclass.__new__(function_metaclass)
    metamodel._init_obj_attrs(new_function)
    
    # Set a name and arguments for the new function
    new_function.args = ['x', 'y', 'radius1', 'radius2']
    new_function.name = 'print_circles'

    # Add 2 statements from the existing function to the new function
    new_function.statements = [existing_function.statements[4], existing_function.statements[5]]

    # Add the new function to the model
    model.functions.append(new_function)
    model._tx_pprint_data.append(new_function)

    # Create a function call for the new function
    function_call_metaclass = metamodel.__getitem__('FunctionCall')
    new_function_call = function_call_metaclass.__new__(function_call_metaclass)
    metamodel._init_obj_attrs(new_function_call)

    new_function_call.name = new_function.name
    new_function_call.args = new_function.args
    new_function_call.whitespaces_before = existing_function._tx_pprint_data[16]._tx_pprint_data[0].layout_before

    # Remove the statements from the existing function and replace them with the function call
    existing_function.statements[4] = new_function_call
    existing_function.statements.pop(5)
    existing_function._tx_pprint_data.pop(16)
    existing_function._tx_pprint_data.pop(16)
    existing_function._tx_pprint_data.pop(16)
    existing_function._tx_pprint_data.insert(16, new_function_call)


def export_dot(mm, model):
    metamodel_export(mm, 'metamodel.dot')
    model_export(model, 'model.dot')


if __name__ == "__main__":
    main()