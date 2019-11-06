from helpers.Operations import Operations
from helpers.Types import Types
from helpers.OperationsCube import OperationsCube
from helpers.CustomStack import Stack
import logging

class Interpreter:
    def __init__(self):
        self.__operands = Stack()
        self.__operators = Stack()
        self.__jumps = Stack()
        self.__quads = []

    @property
    def quads(self):
        return self.__quads

    def push_operator(self, operator):
        self.__operators.push(Operations(operator))

    def push_constant(self, type_, value):
        self.__operands.push(value)

    def assign(self) -> bool:
        logging.info("Current quads at assign", self.quads)
        op = self.__operators.pop()
        l_op = self.__operands.pop()
        self.__quads.append((Operations.ASSIGN, op, l_op, None))
        print("=====")
        for i, c in enumerate(self.__quads):
            print(i, c)

    def check_pending_sum_sub(self) -> bool:
        if not self.__operands.isEmpty() and Operations.is_add_or_sub_op_(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_div_prod(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_div_or_prod_op_(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_rel_op(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_rel_op(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_and_or(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_and_or_op(self.__operators.top()):
            self.gen_quad_for_next_op()

    def maybe_gen_not_quad(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_not_op(self.__operators.top()):
            op = self.__operators.pop()
            l_op = self.__operands.pop()
            self.__quads.append((Operations.NOT, op, l_op, None))

    def gen_quad_for_next_op(self) -> bool:
        r_op = self.__operands.pop()
        l_op = self.__operands.pop()
        op = self.__operators.pop()

        self.__quads.append((op, r_op, l_op, None))
        self.__operands.push("t")

    def open_par(self):
        self.__operators.push(Operations.FAKE_BOTTOM)

    def close_par(self):
        self.__operators.pop()

    def start_condition_quad(self):
        # TODO: Get last temporal.
        condVar = "cond"
        condJumpAddr = self.getNextInstructionAddr()
        self.__jumps.push(condJumpAddr)
        self.__quads.append((Operations.GOTOF, condVar, None))

    def end_condition_quad(self):
        print(vars(self.__jumps))
        condJumpAddr = self.__jumps.pop()
        goToFQuad = self.__quads[condJumpAddr]
        self.__quads[condJumpAddr] = (goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def start_else_if_quad(self):
        condVar = "cond"
        self.__quads.append((Operations.GOTOF, condVar, None))

        self.end_condition_quad()

        self.__jumps.push(self.getNextInstructionAddr())
    def end_else_if_quad(self):
        self.end_condition_quad()
        # for i, c in enumerate(self.__quads):
            # print(i, c)

    def gen_goto_quad(self):
        condVar = "cond"
        self.__quads.append((Operations.GOTO, condVar, None))
        self.end_condition_quad()
        self.__jumps.push(self.getCurrentInstructionAddr())

    def getNextInstructionAddr(self):
        return len(self.__quads)

    def getCurrentInstructionAddr(self):
        return len(self.__quads) - 1

