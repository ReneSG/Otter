import sys
from antlr4 import *
from grammar.otterLexer import otterLexer
from grammar.otterParser import otterParser
from antlr4.tree.Trees import Trees
from compilation.compiler import Compiler
from virtual_machine.virtual_machine import VirtualMachine
import logging

logger = logging.getLogger(__name__)


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = otterLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = otterParser(stream)
    tree = parser.program()
    logger.debug(Trees.toStringTree(tree, None, parser))

    if parser.getNumberOfSyntaxErrors() == 0 and len(Compiler.errors) == 0:
        logger.debug("PROGRAMA CORRECTO")
        logger.debug(
            "===========================================STARTING VIRTUAL MACHINE EXECUTION===========================================")
        quads = Compiler.get_quads()
        vm = VirtualMachine(quads)
        try:
            vm.run()
        except Exception as error:
            logger.error(error)
    else:
        [logger.error(msg) for msg in Compiler.errors]
        exit(1)


if __name__ == '__main__':
    main(sys.argv)
