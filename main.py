import sys
from lexer import lexer
from abstract_parser_tree import PARSER

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "testInput2.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer.input(text)

    # for token in lexer:
    #     print("(%d): %s(%s)" % (token.lineno, token.type, token.value))

    PARSER.parse(text, lexer=lexer)
