from memory.ranges import ScopeRanges, remove_base_prefix
from typing import Any

import logging

logger = logging.getLogger(__name__)


class MethodMemory:
    def __init__(self, parent_memory, global_memory):
        self.__temp_memory = [None] * 12000
        self.__local_memory = [None] * 10000
        self.__global_memory = global_memory
        self.__parent_memory = parent_memory

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
        else:
            return self.__parent_memory.get_value_from_address(remove_base_prefix(address))
