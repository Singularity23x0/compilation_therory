import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONT',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = ("MTX_SUM", "MTX_DIFFERENCE", "MTX_PRODUCT", "MTX_QUOTIENT", "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE",
          "SMALLER_OR_EQUAL", "LARGER_OR_EQUAL", "NOT_EQUAL", "EQUAL", "ID", "INT",
          "FLOAT", "STRING") + tuple(reserved.values())

literals = ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}', ',', ';', ':', '\'', '=', '<', '>']

t_MTX_SUM = r'\.\+'
t_MTX_DIFFERENCE = r'\.\-'
t_MTX_PRODUCT = r'\.\*'
t_MTX_QUOTIENT = r'\./'
t_ADD = r'\+='
t_SUBTRACT = r'\-='
t_MULTIPLY = r'\*='
t_DIVIDE = r'/='
t_SMALLER_OR_EQUAL = r'<='
t_LARGER_OR_EQUAL = r'>='
t_NOT_EQUAL = r'!='
t_EQUAL = r'=='

t_ignore = ' \t'


def t_STRING(t):
    r'"(\\"|[^"])*"'
    t.value = t.value[1:-1]
    return t


def t_FLOAT(t):
    r'([1-9]\d*|0?)\.\d*(E-?\d+)?'
    if t.value[0] == '.':
        t.value = '0' + t.value
    t.value = float(t.value)
    return t


def t_INT(t):
    r'[1-9]\d*'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[_a-zA-Z][_\w]*'
    t.type = reserved.get(t.value, "ID")
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_comment(t):
    r'\#.*(\n|\Z)'
    t.lexer.lineno += 1


def t_error(t):
    print("error in line:", t.lexer.lineno, " unknown expression:", t.value.split('\n', 1)[0].split(';', 1)[0])
    t.lexer.skip(len(t.value.split('\n', 1)[0].split(';', 1)[0]))


lexer = lex.lex()
