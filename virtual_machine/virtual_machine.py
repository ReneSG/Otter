from helpers.operations import Operations
from helpers.custom_stack import Stack
from memory.compilation_memory import CompilationMemory
from .runtime_memory.method_memory import MethodMemory
from ast import literal_eval
import operator
import logging


logger = logging.getLogger(__name__)


class VirtualMachine:

    def __init__(self, quads):
        self.__global_memory = [None] * 10000
        self.__instruction_pointer = 0
        self.__quads = quads
        self.__method_memory = MethodMemory(CompilationMemory.get_const_memory(), self.__global_memory)
        self.__memory_stack = Stack()
        self.__jump_stack = Stack()
        self.__keep_running = True

        self.__operations = {
            Operations.GOTO: self.goto,
            Operations.ASSIGN: self.assign,
            Operations.END_FUNC: self.end_func,
            Operations.ERA: self.era,
            Operations.GOSUB: self.go_sub,
            Operations.PARAM: self.param,
            Operations.RETURN: self.return_op,

            Operations.ADD: self.solveExpression,
            Operations.SUBS: self.solveExpression,
            Operations.DIV: self.solveExpression,
            Operations.PROD: self.solveExpression,
            Operations.GREATER: self.solveExpression,
            Operations.GREATER_EQUAL_THAN: self.solveExpression,
            Operations.LESS: self.solveExpression,
            Operations.LESS_EQUAL_THAN: self.solveExpression,
            Operations.NOT: self.not_op,
            Operations.EQUAL: self.solveExpression,
            Operations.VER_ACCS: self.verify_access,
            Operations.PROD_LIT: self.literal_product,
            Operations.ADD_LIT: self.literal_add,

            Operations.AND: self.solveExpression,
            Operations.OR: self.solveExpression,

            Operations.WRITE: self.write,

            Operations.GOTOF: self.go_to_f,
            Operations.GOTOT: self.go_to_t,
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
                Operations.EQUAL: operator.eq,

                Operations.AND: VirtualMachine.and_op,
                Operations.OR: VirtualMachine.or_op,
                }

    @property
    def current_instruction(self):
        return self.__quads[self.__instruction_pointer]

    def run(self):
        while self.__keep_running:
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

        logger.debug(f"Solved for values: <{quad[1]}> {quad[0]} <{quad[2]}> = {result}")

        logger.debug(f"Solved for values: {literal_eval(str(l_val))} {literal_eval(str(r_val))} = {result}")
        self.increase_instruction_pointer()

    def not_op(self):
        quad = self.current_instruction

        val = self.__method_memory.get_value(quad[1].memory_space)
        result = not val
        self.__method_memory.set_value(quad[2], result)

        logger.debug(f"Not operator: <{quad[1]}> = {result}")
        self.increase_instruction_pointer()

    def verify_access(self):
        quad = self.current_instruction
        index = literal_eval(self.__method_memory.get_value(quad[1].memory_space))
        upper_bound = quad[3]
        lower_bound = quad[2]
        if not (index >= lower_bound and index < upper_bound):
            raise ValueError("Segmentation fault.")

        self.increase_instruction_pointer()

    def literal_product(self):
        quad = self.current_instruction
        var = literal_eval(self.__method_memory.get_value(quad[1].memory_space))
        m = quad[2]
        result = var * m

        self.__method_memory.set_value(quad[3].memory_space, result)

        self.increase_instruction_pointer()

    def literal_add(self):
        quad = self.current_instruction
        var = self.__method_memory.get_value(quad[1].memory_space)
        m = quad[2]
        result = var + m

        self.__method_memory.set_value(quad[3].memory_space, result)

        self.increase_instruction_pointer()

    def era(self):
        new_memory = MethodMemory(CompilationMemory.get_const_memory(), self.__global_memory)
        self.__memory_stack.push(new_memory)
        self.increase_instruction_pointer()

    def go_sub(self):
        quad = self.current_instruction
        self.__jump_stack.push(self.get_next_ip)
        aux = self.__method_memory
        self.__method_memory = self.__memory_stack.pop()
        self.__memory_stack.push(aux)

        self.move_instruction_pointer(quad[2])

    def param(self):
        quad = self.current_instruction

        function_memory = self.__memory_stack.top()

        from_variable_value = self.get_value(quad[1])
        to_variable = quad[2]
        function_memory.set_value(to_variable.memory_space, from_variable_value)
        self.increase_instruction_pointer()

    @property
    def get_next_ip(self):
        return self.__instruction_pointer + 1

    @staticmethod
    def and_op(l, r):
        return l and r

    @staticmethod
    def or_op(l, r):
        return l or r

    def write(self):
        quad = self.current_instruction

        val = self.get_value(quad[1])
        print(val)
        self.increase_instruction_pointer()

    def assign(self):
        quad = self.current_instruction
        if quad[1].is_array_pointer():
            address = self.__method_memory.get_value(quad[1].memory_space)
            value = self.__method_memory.get_value(quad[2].memory_space)
        else:
            address = quad[1].memory_space
            value = self.__method_memory.get_value(quad[2].memory_space)

        self.__method_memory.set_value(address, value)

        logger.debug(f"Assigned value {value} to {address}")
        self.increase_instruction_pointer()

    def end_func(self):
        # TODO: Handle memory swaps.
        if self.__jump_stack.isEmpty():
            # END PROGRAM
            self.__keep_running = False
            return
        self.move_instruction_pointer(self.__jump_stack.pop())

    def go_to_f(self):
        quad = self.current_instruction

        if self.get_value(quad[1]) == False:
            self.move_instruction_pointer(quad[2])
        else:
            self.increase_instruction_pointer()

    def go_to_t(self):
        quad = self.current_instruction

        if self.get_value(quad[1]) == True:
            self.move_instruction_pointer(quad[2])
        else:
            self.increase_instruction_pointer()

    def return_op(self):
        # print("==========AT RETURN=====")
        # self.__method_memory.debug_memory()
        # print("==========AT RETURN=====")
        self.__method_memory = self.__memory_stack.pop()
        # print("==========AFTER SWAP=====")
        # self.__method_memory.debug_memory()
        # print("==========AFTER SWAP=====")
        self.move_instruction_pointer(self.__jump_stack.pop())

    def increase_instruction_pointer(self):
        self.__instruction_pointer += 1

    def get_value(self, variable):
        return self.get_value_from_memory(variable, self.__method_memory)

    def get_value_from_memory(self, variable, memory):
        if variable.is_array_pointer():
            address = memory.get_value(variable.memory_space)
            return memory.get_value(address)
        return memory.get_value(variable.memory_space)

    def move_instruction_pointer(self, new_pointer: int):
        logger.debug(
            f"Moved instruction pointer from {self.__instruction_pointer} to {new_pointer}")
        self.__instruction_pointer = new_pointer
