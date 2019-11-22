from helpers.operations import Operations
from memory.compilation_memory import CompilationMemory
from virtual_machine.runtime_memory.method_memory import MethodMemory

class VirtualMachine:

    def __init__(self, quads):
        self.__instruction_pointer = 0
        self.__quads = quads
        self.__const_memory = CompilationMemory.get_const_memory()
        self.__method_memory = MethodMemory(None)
        self.__operations = {
                Operations.ADD: self.add,
                Operations.GOTO: self.goto,
                }
    @property
    def current_instruction(self):
        return self.__quads[self.__instruction_pointer]

    def run(self):
        while self.__instruction_pointer < len(self.__quads):
            self.__operations.get(self.current_instruction[0])()

    def goto(self):
        self.__instruction_pointer = self.current_instruction[1]

    def add(self):
        quad = self.current_instruction
        result = self.__const_memory.get_value(quad[1]) + self.__const_memory.get_value(quad[2])
        self.__method_memory.set_value(quad[3], result)
        self.increase_ip()


    def increase_ip(self):
        self.__instruction_pointer += 1

