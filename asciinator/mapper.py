"""
    Mapping strategies for turning grayscale
    values into ASCII characters.
"""

def get_mapper(name):
    """ Defaults to grayscale mapper
    """

    return MAPPERS.get(name, grayscale_mapper)


def grayscale_mapper(i):
    if i > 0.90: return ' '
    if i > 0.80: return '.'
    if i > 0.75: return ':'
    if i > 0.65: return '-'
    if i > 0.50: return '='
    if i > 0.40: return '+'
    if i > 0.30: return '*'
    if i > 0.25: return 'O'
    if i > 0.15: return '#'
    if i > 0.07: return '%'
    return '@'


def dashy_mapper(i):
    if i > 0.75: return ' '
    if i > 0.55: return '-'
    if i > 0.25: return '~'
    else: return '='


def punct_mapper(i):
    if i > 0.90: return '?'
    if i > 0.70: return '!'
    if i > 0.60: return ';'
    if i > 0.50: return ':'
    if i > 0.40: return ','
    if i > 0.25: return '.'
    return ' '


def and_or_mapper(i):
    if i > 0.75: return '|'
    if i > 0.25: return '&'
    else: return ' '


def black_white_mapper(i):
    if i > 0.50: return ' '
    return '#'


MAPPERS = {
    'grayscale': grayscale_mapper,
    'black_and_white': black_white_mapper,
    'dashy': dashy_mapper,
    'punct': punct_mapper,
    'and_or': and_or_mapper,
}
