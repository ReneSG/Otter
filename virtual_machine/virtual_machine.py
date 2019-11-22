from helpers.operations import Operations
from memory.compilation_memory import CompilationMemory
from .runtime_memory.method_memory import MethodMemory
from ast import literal_eval
import logging


logger = logging.getLogger(__name__)


class VirtualMachine:

    def __init__(self, quads):
        self.__instruction_pointer = 0
        self.__quads = quads
        self.__const_memory = CompilationMemory.get_const_memory()
        self.__method_memory = MethodMemory(None)
        self.__operations = {
            Operations.ADD: self.add,
            Operations.GOTO: self.goto,
            Operations.ASSIGN: self.assign,
            Operations.END_FUNC: self.end_func,
            Operations.SUBS: self.sub,
        }

    @property
    def current_instruction(self):
        return self.__quads[self.__instruction_pointer]

    def run(self):
        while self.__instruction_pointer < len(self.__quads):
            logger.debug(f"Current instruction: {self.current_instruction}")
            self.__operations.get(self.current_instruction[0])()

    def goto(self):
        self.__instruction_pointer = self.current_instruction[1]

    def add(self):
        quad = self.current_instruction

        # TODO: search whole memory instead of const memory
        l_val, _ = self.__const_memory.get_value(quad[1])
        r_val, _ = self.__const_memory.get_value(quad[2])
        result = literal_eval(l_val) + literal_eval(r_val)
        self.__method_memory.set_value(quad[3], result)

        logger.debug(f"Added values: {quad[1]} + {quad[2]} = {result}")
        self.increase_instruction_pointer()

    def sub(self):
        quad = self.current_instruction
        l_val, _ = self.__const_memory.get_value(quad[1])
        r_val, _ = self.__const_memory.get_value(quad[2])
        result = literal_eval(l_val) - literal_eval(r_val)
        self.__method_memory.set_value(quad[3], result)

        logger.debug(f"Sub values: {quad[1]} + {quad[2]} = {result}")
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

    def increase_instruction_pointer(self):
        self.move_instruction_pointer(1)

    def move_instruction_pointer(self, amount: int):
        self.__instruction_pointer += amount
        logger.debug(
            f"Moved instruction pointer to {self.__instruction_pointer} from {self.__instruction_pointer - amount}")
