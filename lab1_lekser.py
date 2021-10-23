import ply.lex as lex

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


def t_error(t):  # to correct add precise info about error
    print("error in line:", t.lexer.lineno, " unknown expression:", t.value.split('\n',1)[0].split(';',1)[0])
    t.lexer.skip(len(t.value.split('\n',1)[0].split(';',1)[0]))


lexer = lex.lex()
text = """A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
D1 = A.+B' ; # add element-wise A with transpose of B
D2 -= A.-B' ; # substract element-wise A with transpose of B
D3 *= A.*B' ; # multiply element-wise A with transpose of B
D4 /= A./B' ; # divide element-wise A with transpose of B

E1 = [ [ 1, 2, 3],
       [ 4, 5, 6],
       [ 7, 8, 9] ];

res1 = 60.500;
res2 = 60.;
res3 = .500;
res4 = 60.52E2;
str = "Hello\\\\" \\t world";

if (m==n) { 
    if (m >= n) 
        print res;
}"""
lexer.input(text)
for token in lexer:
    print("(%d): %s(%s)" % (token.lineno, token.type, token.value))
