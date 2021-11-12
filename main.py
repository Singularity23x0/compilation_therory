import parserTree
import sys
from parserTree import *

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "testInput2.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer.input(text)

    for token in lexer:
        print("(%d): %s(%s)" % (token.lineno, token.type, token.value))

    parserTree.parserA.parse(text, lexer=lexer)
