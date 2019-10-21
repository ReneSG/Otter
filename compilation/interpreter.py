from helpers.Operations import Operations
from helpers.Types import Types
from helpers.OperationsCube import OperationsCube
import logging

class Interpreter:
    def __init__(self):
        self.__operands = []
        self.__operators = []
        self.__quads = []

    @property
    def quads(self):
        return self.__quads

    def push_operator(self, operator):
        self.__operators.append(Operations(operator))
        print(Operations(operator))

    def assign(self) -> bool:
        logging.info("Current quads at assign", self.quads)
        self.__quads.append((Operations.ASSIGN, None, None, None))
