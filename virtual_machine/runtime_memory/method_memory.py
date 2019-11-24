from memory.ranges import ScopeRanges, remove_base_prefix
from typing import Any

import logging

logger = logging.getLogger(__name__)


class MethodMemory:
    def __init__(self, const_memory, global_memory):
        self.__temp_memory = [None] * 12000
        self.__local_memory = [None] * 10000
        self.__global_memory = global_memory
        self.__const_memory = const_memory

    def set_value(self, address: int, value: Any) -> None:
        if ScopeRanges.is_local(address):
            self.__local_memory[remove_base_prefix(address)] = value
        elif ScopeRanges.is_temp(address):
            self.__temp_memory[remove_base_prefix(address)] = value
        elif ScopeRanges.is_global(address):
            self.__global_memory[remove_base_prefix(address)] = value
        else:
            raise NotImplementedError("Variable no es temp ni local ni global.")

    def get_value(self, address: int) -> Any:
        if ScopeRanges.is_local(address):
            return self.__local_memory[remove_base_prefix(address)]
        elif ScopeRanges.is_temp(address):
            return self.__temp_memory[remove_base_prefix(address)]
        elif ScopeRanges.is_global(address):
            return self.__global_memory[remove_base_prefix(address)]
        elif ScopeRanges.is_const(address):
            return self.__const_memory.get_value_from_address(address)
        else:
            raise NotImplementedError("Variable no es temp ni local ni global ni const.")

    def debug_memory(self):
        print("======= TEMP ========")
        for i in range(0, len(self.__temp_memory)):
            el = self.__temp_memory[i]
            if el is not None: print(f"{el} @{i+30000}")
        print("======= LOCAL ========")
        for i in range(0, len(self.__local_memory)):
            el = self.__local_memory[i]
            if el is not None: print(f"{el} @{i+10000}")
        print("======= GLOBAL ========")
        for i in range(0, len(self.__global_memory)):
            el = self.__global_memory[i]
            if el is not None: print(f"{el} @{i}")

