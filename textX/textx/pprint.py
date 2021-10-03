from arpeggio import PTNodeVisitor, Terminal, visit_parse_tree

class EmptyLine:
    def __init__(self, empty_lines):
        self.empty_lines = empty_lines

def _get_first_terminal_empty_lines(node):
    if isinstance(node, Terminal):
        if node.layout_before.count('\n') > 1:
            last_newline_location = node.layout_before.rfind('\n')
            empty_lines = node.layout_before[0:last_newline_location]
            node.layout_before = node.layout_before.removeprefix(empty_lines)
            return empty_lines
        return None
    if hasattr(node, '_tx_pprint_data'):
        return _get_first_terminal_empty_lines(node._tx_pprint_data[0])
    return None

def _prepare_process_node(node):
    skip_next = False
    for idx, n in enumerate(node._tx_pprint_data):
        if skip_next:
            skip_next = False
            continue

        empty_lines = _get_first_terminal_empty_lines(n)
        if empty_lines:
            node._tx_pprint_data.insert(idx, EmptyLine(empty_lines))
            skip_next = True

        if isinstance(n, Terminal):
            continue
        if hasattr(n, '_tx_pprint_data'):
            _prepare_process_node(n)


def prepare_model(model):
    """
    Post-processing in order to prepare model for refactoring
    """
    _prepare_process_node(model)    




def pprint_parse_tree(parse_tree):
    visit_parse_tree(parse_tree, PPrintVisitor(debug=False))

# Visitor for printing a full Arpeggio parse tree
class PPrintVisitor(PTNodeVisitor):
    def __init__(self, debug):
        self.debug = debug

        super(PPrintVisitor, self).__init__()

    def visit__default__(self, node, chilren):
        if isinstance(node, Terminal):
            if node.comment_before:
                print(node.comment_before, end='')
            if node.layout_before:
                print(node.layout_before, end='')
            print(node, end='')

# Class for printing a TextX model which includes additional printing data
class PrettyPrinter:
    def __init__(self):
        self.processors = {}
        self.result = ''

    def append(self, value):
        self.result += str(value)

    def write_to_file(self, filename):
        file = open(filename, 'w')
        file.write(self.result)
        file.close()
    
    def get_result(self):
        return self.result

    def register_processor(self, className, processor):
        self.processors[className] = processor

    def pprint_model(self, model):
        self.result = ''
        self.process_node(model)

    def process_node(self, node):
        for n in node._tx_pprint_data:
            n_class = n.__class__.__name__

            if isinstance(n, Terminal):
                self._pprint_terminal(n)
            elif isinstance(n, EmptyLine):
                self._pprint_empty_line(n)
            elif n_class in self.processors and not hasattr(n, '_tx_pprint_data'):
                self.processors[n_class](n, self)
            else:
                self.process_node(n)
    
    def _pprint_terminal(self, node):
        if node.layout_before:
            self.append(node.layout_before)
        for comment in node.comments:
            self.append(str(comment))
        self.append(node)
        if hasattr(node, 'comment_after') and hasattr(node, 'comment_after_ws'):
            self.append(node.comment_after_ws)
            self.append(node.comment_after)

    def _pprint_empty_line(self, node):
        self.append(node.empty_lines)
