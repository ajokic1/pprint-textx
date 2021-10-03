"""
Layout and comment preservation utilities
"""

class Comment:
    def __init__(self, comment, layout_before, layout_after):
        self.layout_before = layout_before
        self.comment = comment
        self.layout_after = layout_after

    def __str__(self):
        return '{}{}{}'.format(self.layout_before, self.comment, self.layout_after)

def _get_dict_items_between_positions(dictionary, pos1, pos2, concatenate = False):
    def position_is_between(position):
        if pos2 == -1 and position > pos1:
            return True
        if position > pos1 and position < pos2:
            return True
        return False
    
    keys = list(filter(position_is_between, dictionary.keys()))
    
    if concatenate:
        result = ''
        for key in keys:
            result += str(dictionary[key])
    else:
        result = {}
        for key in keys:
            result[key] = dictionary[key]
    
    return result

def _get_last_terminal_pos(parser, parser_position):
    if not hasattr(parser, 'last_terminal_pos'):
        return 0
    return parser.last_terminal_pos if parser_position != parser.last_terminal_pos else parser.before_last_terminal_pos

def _get_comments(parser, last_terminal_pos, parser_position):
    """
    Returns a list of Comment objects between the previous and current Terminal
    """

    positions_and_comments = _get_dict_items_between_positions(parser.comments, last_terminal_pos, parser_position)
    positions_and_whitespaces = _get_dict_items_between_positions(parser.comment_whitespaces, last_terminal_pos, parser_position)

    comments = []
    last_comment_pos = 0
    sorted_comment_positions = sorted(list(positions_and_comments.keys()))
    for pos in sorted_comment_positions:
        if last_comment_pos == 0:
            last_comment_pos = pos
            continue

        # Create a Comment instance for the comment from the previous iteration and attach the whitespaces to it
        comment_whitespaces = _get_dict_items_between_positions(positions_and_whitespaces, last_comment_pos - 1, pos, True)
        comments.append(Comment(positions_and_comments[last_comment_pos], '', comment_whitespaces))

    # Handle last comment in the dict
    if len(positions_and_comments) > 0:
        last_comment_pos = sorted_comment_positions[len(sorted_comment_positions) - 1]
        comment_whitespaces = _get_dict_items_between_positions(positions_and_whitespaces, last_comment_pos - 1, -1, True)
        comments.append(Comment(positions_and_comments[last_comment_pos], '', comment_whitespaces))

    return comments


def _get_terminal_whitespaces(parser, match, parser_position, last_terminal_pos):
    """
    Returns the whitespaces between the current and the last parsed Terminal
    """

    layout_before = None
    if parser.keep_layout and match.rule_name != 'Comment':
        layout_before = _get_dict_items_between_positions(parser.whitespaces, last_terminal_pos, parser_position, True)

    return layout_before


def get_layout_data(parser, match, parser_position):
    last_terminal_pos = _get_last_terminal_pos(parser, parser_position)
    
    comments = []
    if match.rule_name != 'Comment':
        comments = _get_comments(parser, last_terminal_pos, parser_position)

    layout_before = _get_terminal_whitespaces(parser, match, parser_position, last_terminal_pos)
    
    if hasattr(parser, 'last_terminal_pos') and parser.last_terminal_pos != parser_position and match.rule_name != 'Comment':
        parser.before_last_terminal_pos = parser.last_terminal_pos
    
    if match.rule_name != 'Comment':
        parser.last_terminal_pos = parser_position

    
    # If first comment is inline attach it to previous node instead
    if len(comments) > 0 and (not layout_before or '\n' not in layout_before) and hasattr(parser, 'last_terminal'):
        parser.last_terminal.comment_after = comments[0].comment
        parser.last_terminal.comment_after_ws = layout_before
        layout_before = comments[0].layout_after
        comments.pop(0)

    return layout_before, comments