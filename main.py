import sys
from lexer import lexer

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "testInput.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer.input(text)  # Give the lexer some input

    for token in lexer:
        print("(%d): %s (%s)" % (token.lineno, token.type, token.value))
