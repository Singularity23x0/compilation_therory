import sys
import traceback
from lexer import lexer
from parser_tree import PARSER,get_structure,TreePrinter,SemanticChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "test2.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer.input(text)

    # for token in lexer:
    #     print("(%d): %s(%s)" % (token.lineno, token.type, token.value))

    PARSER.parse(text, lexer=lexer)
    tree_structure = get_structure()
    if tree_structure is not None:
        TreePrinter("resART.txt").draw(tree_structure)
        S=SemanticChecker()
        try:
            S.visit(tree_structure)
        except Exception as err:
            print(err,traceback.format_exc())
        for err in S.errorList:
            print(err)

