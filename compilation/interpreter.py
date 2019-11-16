from helpers.operations import Operations
from helpers.types import Types
from helpers.operations_cube import OperationsCube
from helpers.custom_stack import Stack
import logging

class Interpreter:
    def __init__(self):
        self.__operands = Stack()
        self.__dim_operands = Stack()
        self.__operators = Stack()
        self.__jumps = Stack()
        self.__quads = []

    @property
    def quads(self):
        return self.__quads

    def push_operator(self, operator):
        self.__operators.push(Operations(operator))

    def push_constant(self, type_, value):
        if self.hasMultipleDimensions(value):
            self.__dim_operands.push((value, 1))
        else:
            self.__operands.push(value)

    def assign(self) -> bool:
        logging.debug(f"Current quads at assign: {self.quads}")
        op = self.__operators.pop()
        l_op = self.__operands.pop()
        self.__quads.append((Operations.ASSIGN, op, l_op, None))

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

    def start_condition_quad(self, isUnless=False):
        # TODO: Get last temporal.
        condVar = "cond"
        self.__jumps.push(self.getNextInstructionAddr())
        self.__quads.append((Operations.GOTOT if isUnless else Operations.GOTOF , condVar, None))

    def end_condition_quad(self):
        condJumpAddr = self.__jumps.pop()
        goToFQuad = self.__quads[condJumpAddr]
        self.__quads[condJumpAddr] = (goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def gen_goto_quad(self):
        self.__quads.append((Operations.GOTO, None))
        self.end_condition_quad()
        self.__jumps.push(self.getCurrentInstructionAddr())

    def end_while_quad(self):
        goToFAddress = self.__jumps.pop()
        goToFQuad = self.__quads[goToFAddress]
        self.__quads[goToFAddress] = (goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

        self.gen_goto_quad_to(self.__jumps.pop())

    def gen_goto_quad_to(self, address):
        self.__quads.append((Operations.GOTO, address))

    def push_instruction_address(self):
        self.__jumps.push(self.getNextInstructionAddr())

    def getNextInstructionAddr(self):
        return len(self.__quads)

    def getCurrentInstructionAddr(self):
        return len(self.__quads) - 1

    def read_quad(self):
        self.__quads.append((Operations.READ, "t"))

    def write_quad(self):
        self.__quads.append((Operations.WRITE, "t"))

    def return_quad(self):
        self.__quads.append((Operations.RETURN, "t"))

    def start_for_quad(self):
        self.push_instruction_address()
        self.start_condition_quad()

    def end_for_quad(self):
        upperBoundBy = self.__jumps.pop()
        lowerBoundBy = self.__jumps.pop()

        for i in range(lowerBoundBy + 1, upperBoundBy):
            self.__quads.append(self.__quads.pop(lowerBoundBy + 1))

        self.gen_goto_quad_to(self.__jumps.pop())
        goToFAddress = lowerBoundBy
        goToFQuad = self.__quads[goToFAddress]
        self.__quads[goToFAddress] = (goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def resolve_dimension_access(self):
        dim_tuple = self.__dim_operands.top()
        dim_variable = dim_tuple[0]
        index = self.__operands.top()
        self.__quads.append((Operations.VER_ACCS, index, self.getLowerBound(dim_variable), self.getUpperBound(dim_variable)))
        self.maybe_multiply_for_m(dim_tuple)
        self.__dim_operands.push((dim_tuple[0], dim_tuple[1] + 1))

    def maybe_multiply_for_m(self, dim_tuple):
        # Only compute mn*sn for second and higher dimensions.
        if dim_tuple[1] == 1: return

        index = self.__operands.pop()
        self.__quads.append((Operations.PROD, index, self.getMFor(dim_tuple[0]), "t"))
        self.__operands.push("t")

    def complete_dimension_access(self):
        dim_variable = self.__dim_operands.pop()[0]
        index = self.__operands.pop()
        self.__quads.append((Operations.ADD, index, self.getAddressFor(dim_variable), "t"))

    def allocate_mem_quad(self, instance, method):
        self.__quads.append((Operations.ERA, instance, method))

    def add_method_parameter(self):
        #TODO: Get param address once memory is implemented.
        self.__quads.append((Operations.PARAM, self.__operands.pop()))

    def complete_method_call(self, method):
        self.__quads.append((Operations.GOSUB, method))

        #TODO: If method has return assign to temp.
        self.__operands.push("return temp")


    def getLowerBound(self, dim_variable):
        # TODO: Get real value once memory is implemented.
        return "lower_bound"

    def getMFor(self, dim_variable):
        # TODO: Get real value once memory is implemented.
        return "dummy_m"

    def getUpperBound(self, dim_variable):
        # TODO: Get real value once memory is implemented.
        return "upper_bound"

    def getAddressFor(self, dim_variable):
        # TODO: Get real value once memory is implemented.
        return "dummy_address"

    def hasMultipleDimensions(self, operand):
        # TODO: Check dimension once memory is implemented.
        return operand == "A";

    def debug_quads(self):
        for i in range(0, len(self.__quads)):
            logging.debug(f"{i}, {self.__quads[i]}")
