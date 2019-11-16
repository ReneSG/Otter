from .const_memory import ConstMemory
from .memory import Memory
from .ranges import ScopeRanges
from scope.scopes import Scopes
from typing import Optional


class CompilationMemory:
    __global_memory = Memory(Scopes.GLOBAL, ScopeRanges.GLOBAL)
    __temp_memory = Memory(Scopes.TEMP, ScopeRanges.TEMP)
    __const_memory = ConstMemory(Scopes.CONSTANT, ScopeRanges.CONSTANTS)

    @staticmethod
    def next_const_memory_space(value: str, var_type: str) -> int:
        return CompilationMemory.__const_memory.next_memory_space(value, var_type)

    @staticmethod
    def next_global_memory_space(var_type: str) -> int:
        return CompilationMemory.__global_memory.next_memory_space(var_type)

    @staticmethod
    def next_temp_memory_space(var_type: str) -> int:
        return CompilationMemory.__temp_memory.next_memory_space(var_type)

    @staticmethod
    def clear_temp_memory() -> None:
        CompilationMemory.__temp_memory = Memory(Scopes.TEMP, Scopes.TEMP)
