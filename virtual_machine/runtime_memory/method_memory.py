from memory.ranges import ScopeRanges

class MethodMemory:
    def __init__(self, parent_memory):
        self.__temp_memory = [None]*12000
        self.__local_memory = [None]*12000
        self.__parent_memory = parent_memory

    def set_value(self, address, value):
        if ScopeRanges.is_local(address):
            self.__local_memory[address] = value
        elif ScopeRanges.is_temp(address):
            self.__temp_memory[address] = value
        else:
            raise NotImplemented("Variable no es temp ni local.")
