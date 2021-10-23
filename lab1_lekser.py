import ply.lex as lex
import sys

# TODO file read from template on Kuta web,check other formats for data, string may need clean up

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

tokens = ("MADD", "MDIFF", "MMULT", "MDIV", "AADD", "ADIFF", "AMULT", "ADIV",
          "R_SMALL_EQUAL", "R_BIGER_EQUAL", "R_NOT_EQUAL", "R_EQUAL", "ID", "INT",
          "FLOAT", "STRING") + tuple(reserved.values())

literals = ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}', ',', ';', ':', '\'', '=', '<', '>']

t_MADD = r'\.\+'
t_MDIFF = r'\.\-'
t_MMULT = r'\.\*'
t_MDIV = r'\./'
t_AADD = r'\+='
t_ADIFF = r'\-='
t_AMULT = r'\*='
t_ADIV = r'/='
t_R_SMALL_EQUAL = r'<='
t_R_BIGER_EQUAL = r'>='
t_R_NOT_EQUAL = r'!='
t_R_EQUAL = r'=='

t_ignore = ' \t'


def t_STRING(t):  # to correct
    r'"(\\"|[^"])*"'
    t.value = t.value[1:-1]
    return t


def t_FLOAT(t):  # modified
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
    print("error in line:", t.lexer.lineno, " unknown expression:", t.value.split('\n',1)[0].split(';',1)[0])
    t.lexer.skip(len(t.value.split('\n',1)[0].split(';',1)[0]))


lexer = lex.lex()


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer.input(text)  # Give the lexer some input

    for token in lexer:
        print("(%d): %s(%s)" % (token.lineno, token.type, token.value))
