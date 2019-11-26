from helpers.operations import Operations
from helpers.custom_stack import Stack
from memory.compilation_memory import CompilationMemory
from .runtime_memory.method_memory import MethodMemory
from ast import literal_eval
from scope.variable import Variable
from typing import Tuple, List
from compilation.compiler import Compiler
import operator
import logging


logger = logging.getLogger(__name__)


class VirtualMachine:
    """ The Virtual Machine class is responsible for taking a list of quads as its input
        and based on the operation code of the quad take certain actions.

        The main parts of the VirtualMachine are:
            __global_memory [List[Any]]: A list to represent the global memory.
            __instruction_pointer [int]: Points to the current quad.
            __quads [List[Any]]: List with all the quads for the program.
            __method_memory [MethodMemory]: Keeps track of the current active runtime memory.
            __memory_stack [Stack]: Keeps track of the stack of memory.
            __jump_stack [Stack]: Keeps track of the jumps in the virtual machine.
            __keep_running [bool]: Keeps track of wether we should keep executing the program or stop.
            __operations [dict]: Dictionary mapping all the Operations to its correct handler.
            __expression_operations [dict]: Dictionary mapping each operation in a expression to its handler.
    """

    def __init__(self, quads: List):
        self.__global_memory = [None] * 10000
        self.__instruction_pointer = 0
        self.__quads = quads
        self.__current_instance = [None] * 10000
        self.__method_memory = MethodMemory(CompilationMemory.get_const_memory(), self.__global_memory, self.__current_instance)
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
            Operations.NOT_EQUAL: self.solveExpression,
            Operations.EQUAL: self.solveExpression,
            Operations.VER_ACCS: self.verify_access,
            Operations.PROD_LIT: self.literal_product,
            Operations.ADD_LIT: self.literal_add,
            Operations.RES_POINTER: self.resolve_pointer,

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
                Operations.NOT_EQUAL: operator.ne,

                Operations.AND: VirtualMachine.and_op,
                Operations.OR: VirtualMachine.or_op,
                }

    @property
    def current_instruction(self):
        """ Takes the current quad.

            Returns:
                - The quad that is pointed by __instruction_pointer.
        """
        return self.__quads[self.__instruction_pointer]

    def run(self):
        """ Executes the virtual machine by looping thought all the quads and
            running its corresponding handler.
        """
        while self.__keep_running:
            logger.debug(f"Current instruction: {self.current_instruction}")
            self.__operations.get(self.current_instruction[0])()

    def goto(self):
        """ Handler for goto operation. Moves the __instruction_pointer to the
            address indicated in the quad.
        """
        self.__instruction_pointer = self.current_instruction[2]

    def solveExpression(self):
        """ Solves an operation.
        """
        quad = self.current_instruction

        # TODO: search whole memory instead of const memory
        l_val = self.get_value(quad[1])
        r_val = self.get_value(quad[2])
        result = self.__expression_operations.get(quad[0])(literal_eval(str(l_val)), literal_eval(str(r_val)))
        self.__method_memory.set_value(quad[3], result)

        logger.debug(f"Solved for values: <{quad[1]}> {quad[0]} <{quad[2]}> = {result}")

        logger.debug(f"Solved for values: {literal_eval(str(l_val))} {literal_eval(str(r_val))} = {result}")
        self.increase_instruction_pointer()

    def not_op(self):
        """ Handler for a Not Operation.
        """
        quad = self.current_instruction

        val = self.get_value(quad[1])
        result = not val
        self.__method_memory.set_value(quad[2], result)

        logger.debug(f"Not operator: <{quad[1]}> = {result}")
        self.increase_instruction_pointer()

    def verify_access(self):
        """ Handler to verify that an index is within the range of a dimensional
            variable.

            Raises:
                - Exception: When the index is out of bounds.
        """
        quad = self.current_instruction
        index = self.get_value(quad[1])
        if type(index) == str:
            index = literal_eval(index)
        upper_bound = quad[3]
        lower_bound = quad[2]
        if not (index >= lower_bound and index < upper_bound):
            raise ValueError(f"Segmentation fault. Index: {index} is out of range({lower_bound, upper_bound})")

        self.increase_instruction_pointer()

    def literal_product(self):
        """ Handler to make a product with a int primitive instead of a variable.
        """
        quad = self.current_instruction
        var = self.get_value(quad[1])
        if type(var) == str:
            var = literal_eval(var)
        m = quad[2]
        result = var * m

        self.__method_memory.set_value(quad[3].memory_space, result)

        self.increase_instruction_pointer()

    def literal_add(self):
        """ Handler to make an addition with a int primitive instead of a variable.
        """
        quad = self.current_instruction
        var = self.get_value(quad[1])
        m = quad[2]
        result = var + m

        self.__method_memory.set_value(quad[3].memory_space, result)

        self.increase_instruction_pointer()

    def era(self):
        """ Handler for ERA Operation. Creates a new method memory for the method
            that is going to be called.
        """
        quad = self.current_instruction
        if quad[1] == "constructor":
            self.__current_instance = [None] * 10000
        elif quad[1] != "self":
            self.__current_instance = self.get_value(quad[1])

        new_memory = MethodMemory(CompilationMemory.get_const_memory(), self.__global_memory, self.__current_instance)
        self.__memory_stack.push(new_memory)
        self.increase_instruction_pointer()

    def go_sub(self):
        """ Handler for GOSUB Operation. Assigns the __method_memory to the memory of the method
            that is going to go to, and stores the current memory in the memory stack.
        """
        quad = self.current_instruction
        self.__jump_stack.push(self.get_next_ip)
        aux = self.__method_memory
        self.__method_memory = self.__memory_stack.pop()
        self.__memory_stack.push(aux)

        self.move_instruction_pointer(quad[2])

    def param(self):
        """ Handler for PARAM Operation. Assigns the function arguments from the current memory to
            the memory of the method to be called.
        """
        quad = self.current_instruction

        function_memory = self.__memory_stack.top()

        from_variable = quad[1]
        to_variable = quad[2]

        if from_variable.has_multiple_dimensions():
            for index in range(0, from_variable.size):
                from_variable_value = self.get_value_from_memory_address(from_variable.memory_space + index)
                function_memory.set_value(to_variable.memory_space + index, from_variable_value)

        else:
            from_variable_value = self.get_value(quad[1])
            function_memory.set_value(to_variable.memory_space, from_variable_value)
        self.increase_instruction_pointer()

    @property
    def get_next_ip(self) -> int:
        """ Returns the next instruction pointer.

            Returns:
                - [int]: The next instruction pointer.
        """
        return self.__instruction_pointer + 1

    @staticmethod
    def and_op(l: bool, r: bool) -> bool:
        """ Handler for and operation.

            Arguments:
                - l [bool]: Left operator of and operation.
                - r [bool]: Right operator of and operation.

            Returns:
                - [int]: Result of the and operation.
        """
        return l and r

    @staticmethod
    def or_op(l, r):
        """ Handler for or operation.

            Arguments:
                - l [bool]: Left operator of or operation.
                - r [bool]: Right operator of or operation.

            Returns:
                - [int]: Result of the or operation.
        """
        return l or r

    def write(self):
        """ Handler for WRITE Operation.
        """
        quad = self.current_instruction

        val = self.get_value(quad[1])
        print(val, end="")
        self.increase_instruction_pointer()

    def assign(self):
        """ Handler for ASSIGN operation. When the variable is an array pointer, instead of
            just using its direction for the assing operation, its memory_space should be
            looked on memory and use the value as the address.
        """
        quad = self.current_instruction
        if quad[1].is_array_pointer() and quad[2].is_array_pointer():
            address = self.__method_memory.get_value(quad[1].memory_space)
            pointer_address = self.__method_memory.get_value(quad[2].memory_space)
            value = self.__method_memory.get_value(pointer_address)
        elif quad[1].is_array_pointer():
            address = self.__method_memory.get_value(quad[1].memory_space)
            value = self.__method_memory.get_value(quad[2].memory_space)
        elif quad[2].is_array_pointer():
            ## Assign of a quad of type (<Operations.ASSIGN: '='>, <temp: int | 10012>, <40004: array_pointer | 40004>, 10012).
            address = quad[1].memory_space
            pointer_address = self.__method_memory.get_value(quad[2].memory_space)
            value = self.__method_memory.get_value(pointer_address)
        else:
            address = quad[1].memory_space
            value = self.__method_memory.get_value(quad[2].memory_space)

        self.__method_memory.set_value(address, value)

        logger.debug(f"Assigned value {value} to {address}")
        self.increase_instruction_pointer()

    def end_func(self):
        """ Handler for ENDFUNC Operation. Finish the execution of the VirtualMachine if it is 
            the end of the program.
        """
        # TODO: Handle memory swaps.
        if self.__jump_stack.isEmpty():
            # END PROGRAM
            self.__keep_running = False
            return

        self.move_instruction_pointer(self.__jump_stack.pop())

    def go_to_f(self):
        """ Handler for GOTOF. Moves the __instruction_pointer when the condition value is false.
        """
        quad = self.current_instruction

        if self.get_value(quad[1]) == False:
            self.move_instruction_pointer(quad[2])
        else:
            self.increase_instruction_pointer()

    def go_to_t(self):
        """ Handler for GOTOT. Moves the __instruction_pointer when the condition variable is true.
        """
        quad = self.current_instruction

        if self.get_value(quad[1]) == True:
            self.move_instruction_pointer(quad[2])
        else:
            self.increase_instruction_pointer()

    def resolve_pointer(self):
        quad = self.current_instruction

        value = self.get_value(quad[1])
        self.__method_memory.set_value(quad[2].memory_space, value)
        self.increase_instruction_pointer()

    def return_op(self):
        """ Handler for RETURN Operation. Swaps active memory and moves the instruction pointer
            to where it was before the GOSUB Operation.
        """
        quad = self.current_instruction

        # The return from Main will not have a next memory.
        if not self.__jump_stack.isEmpty():
            if not self.__memory_stack.isEmpty() and len(quad) > 1 and quad[1] == "constructor":
                self.__memory_stack.top().set_value(quad[2].memory_space, self.__current_instance)

            self.__method_memory = self.__memory_stack.pop()
            self.move_instruction_pointer(self.__jump_stack.pop())
        else:
            self.increase_instruction_pointer()

    def increase_instruction_pointer(self):
        """ Increases the instruction pointer by one.
        """
        self.__instruction_pointer += 1

    def get_value(self, variable: Variable):
        """ Retrieves the value of the variabel from the active memory.

            Arguments:
                - variable [Variable]: The variable to be retrieved.

            Returns:
                - The value in memory of the provieded variable.
        """
        return self.get_value_from_memory(variable, self.__method_memory)

    def get_value_from_memory(self, variable: Variable, memory: MethodMemory):
        """ Retrieves the value of the variable from the provided memory.

            Arguments:
                - variable [Variable]: The variable to be retrieved.
                - memory [MethodMemory]: The memory to be used to retireved the variable.

            Returns:
                - The value in memory of the provieded variable.
        """
        if variable.is_array_pointer():
            address = memory.get_value(variable.memory_space)
            return memory.get_value(address)
        return memory.get_value(variable.memory_space)

    def get_value_from_memory_address(self, address):
        return self.__method_memory.get_value(address)

    def move_instruction_pointer(self, new_pointer: int):
        """ Moves the instruction pointer to the provided address.

            Arguments:
                - new_pointer [int]: Pointer to new address.
        """
        logger.debug(
            f"Moved instruction pointer from {self.__instruction_pointer} to {new_pointer}")
        self.__instruction_pointer = new_pointer
