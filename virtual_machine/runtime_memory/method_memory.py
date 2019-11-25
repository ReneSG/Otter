from memory.ranges import ScopeRanges, remove_base_prefix
from typing import Any, List
from memory.const_memory import ConstMemory

import logging

logger = logging.getLogger(__name__)


class MethodMemory:
    """ The MethodMemory class is responsible for taking care of the runtime memory
        of a method.

        The main parts of the MethodMemory are:
            __temp_memory [List[Any]]: Keeps track of the temporal memory.
            __local_memory [List[Any]]: Keeps track of the local memory.
            __global_memory [List[Any]]: Keeps track of the global memory.
            __const_memory [ConstMemory]: Keeps track of the const memory.
    """
    def __init__(self, const_memory: ConstMemory, global_memory: List):
        self.__temp_memory = [None] * 12000
        self.__local_memory = [None] * 10000
        self.__global_memory = global_memory
        self.__const_memory = const_memory

    def set_value(self, address: int, value: Any) -> None:
        """ Sets the provided value to the provided address.

        Arguments:
            - address [int]: The address where the value should be set.
            - value [Any]: The value to be set.
        """
        if ScopeRanges.is_local(address):
            self.__local_memory[remove_base_prefix(address)] = value
        elif ScopeRanges.is_temp(address):
            self.__temp_memory[remove_base_prefix(address)] = value
        elif ScopeRanges.is_global(address):
            self.__global_memory[remove_base_prefix(address)] = value
        else:
            raise NotImplementedError("Variable no es temp ni local ni global.")

    def get_value(self, address: int) -> Any:
        """ Sets the provided value to the provided address.

        Arguments:
            - address [int]: The address where the value should be set.
            - value [Any]: The value to be set.
         """
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
        """ Pretty prints the memory.
        """
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

