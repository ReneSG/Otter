from helpers.operations import Operations
from memory.compilation_memory import CompilationMemory
from .runtime_memory.method_memory import MethodMemory
from ast import literal_eval
import operator
import logging


logger = logging.getLogger(__name__)


class VirtualMachine:

    def __init__(self, quads):
        self.__instruction_pointer = 0
        self.__quads = quads
        self.__method_memory = MethodMemory(CompilationMemory.get_const_memory())
        self.__operations = {
            Operations.GOTO: self.goto,
            Operations.ASSIGN: self.assign,
            Operations.END_FUNC: self.end_func,
            Operations.ADD: self.solveExpression,
            Operations.SUBS: self.solveExpression,
            Operations.DIV: self.solveExpression,
            Operations.PROD: self.solveExpression,
            Operations.GREATER: self.solveExpression,
            Operations.GREATER_EQUAL_THAN: self.solveExpression,
            Operations.LESS: self.solveExpression,
            Operations.LESS_EQUAL_THAN: self.solveExpression,
            Operations.NOT: self.solveExpression,
            Operations.EQUAL: self.solveExpression,

            Operations.WRITE: self.write,

            Operations.GOTOF: self.go_to_f,
        }

        self.__expression_operations = {
                Operations.ADD: operator.add,
                Operations.SUBS: operator.sub,
                Operations.DIV: operator.truediv,
                Operations.PROD: operator.mul,
                Operations.GREATER: operator.gt,
                Operations.GREATER_EQUAL_THAN: operator.ge,
                Operations.LESS: operator.lt,
                Operations.LESS_EQUAL_THAN: operator.le,
                Operations.NOT: operator.ne,
                Operations.EQUAL: operator.eq,
                }

    @property
    def current_instruction(self):
        return self.__quads[self.__instruction_pointer]

    def run(self):
        while self.__instruction_pointer < len(self.__quads):
            logger.debug(f"Current instruction: {self.current_instruction}")
            self.__operations.get(self.current_instruction[0])()

    def goto(self):
        self.__instruction_pointer = self.current_instruction[2]

    def solveExpression(self):
        quad = self.current_instruction

        # TODO: search whole memory instead of const memory
        l_val = self.__method_memory.get_value(quad[1].memory_space)
        r_val = self.__method_memory.get_value(quad[2].memory_space)
        result = self.__expression_operations.get(quad[0])(literal_eval(str(l_val)), literal_eval(str(r_val)))
        self.__method_memory.set_value(quad[3], result)

        logger.debug(f"Added values: {quad[1]} + {quad[2]} = {result}")
        self.increase_instruction_pointer()

    def write(self):
        quad = self.current_instruction

        val = self.__method_memory.get_value(quad[1].memory_space)
        print(val)
        self.increase_instruction_pointer()

    def assign(self):
        quad = self.current_instruction
        value = self.__method_memory.get_value(quad[2].memory_space)
        self.__method_memory.set_value(quad[3], value)

        logger.debug(f"Assigned value {value} to {quad[1].name}")
        self.increase_instruction_pointer()

    def end_func(self):
        logger.debug("Ended method.")
        self.increase_instruction_pointer()

    def go_to_f(self):
        quad = self.current_instruction
        print(quad)

        if self.get_value(quad[1]) == False:
            self.move_instruction_pointer(quad[2])
        else:
            self.increase_instruction_pointer()

    def increase_instruction_pointer(self):
        self.__instruction_pointer += 1

    def get_value(self, variable):
        return self.__method_memory.get_value(variable.memory_space)

    def move_instruction_pointer(self, new_pointer: int):
        self.__instruction_pointer = new_pointer
        logger.debug(
            f"Moved instruction pointer to {new_pointer} from {self.__instruction_pointer}")
