import sys
from antlr4 import *
from grammar.otterLexer import otterLexer
from grammar.otterParser import otterParser
from antlr4.tree.Trees import Trees
from compilation.compiler import Compiler
import logging


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = otterLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = otterParser(stream)
    tree = parser.program()
    #   print(Trees.toStringTree(tree, None, parser))

    if parser.getNumberOfSyntaxErrors() == 0 and len(Compiler.errors) == 0:
        print("PROGRAMA CORRECTO")
    else:
        [logging.error(msg) for msg in Compiler.errors]


if __name__ == '__main__':
    main(sys.argv)
