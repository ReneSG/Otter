from .const_memory import ConstMemory
from .memory import Memory
from .ranges import ScopeRanges
from scope.scopes import Scopes
from typing import Optional


class CompilationMemory:
    """The CompilationMemory is a static class in charge of assigning memory addresses during compilation."""
    __global_memory = Memory(Scopes.GLOBAL, ScopeRanges.GLOBAL)
    __temp_memory = Memory(Scopes.TEMP, ScopeRanges.TEMP)
    __const_memory = ConstMemory(Scopes.CONSTANT, ScopeRanges.CONSTANTS)

    @staticmethod
    def get_const_memory():
        """ Returns the const memory.

            Returns:
                - [Memory]: The const memory.
        """
        return CompilationMemory.__const_memory

    @staticmethod
    def next_const_memory_space(value: str, var_type: str) -> int:
        """Gets the next available memory address for constants.

        Arguments:
            - value [str]: The value of the constant to be stored.
            - var_type [str]: The type of the constant.

        Returns:
            - [int] The memory address of the constant.
        """
        return CompilationMemory.__const_memory.next_memory_space(value, var_type)

    @staticmethod
    def next_global_memory_space(var_type: str) -> int:
        """Gets the next available memory address for globals.

        Arguments:
            - var_type [str]: The type of the variable.

        Returns:
            - [int] The memory address of the global.
        """
        return CompilationMemory.__global_memory.next_memory_space(var_type)

    @staticmethod
    def next_temp_memory_space(var_type: str) -> int:
        """Gets the next available memory address for temporals.

        Arguments:
            - var_type [str]: The type of the variable.

        Returns:
            - [int] The memory address of the temporal.
        """
        return CompilationMemory.__temp_memory.next_memory_space(var_type)

    @staticmethod
    def next_temp_memory_chunk(var_type: str, size: int) -> int:
        """Gets the next available memory chunk for temp.

        Arguments:
            - var_type [str]: The type of the constant.
            - size [int]: The size of the chunk

        Returns:
            - [int] The first memory address of the global.
        """
        return CompilationMemory.__temp_memory.next_memory_chunk(value, var_type)

    @staticmethod
    def next_global_memory_chunk(var_type: str, size: int) -> int:
        """Gets the next available memory chunk for globals.

        Arguments:
            - var_type [str]: The type of the constant.
            - size [int]: The size of the chunk

        Returns:
            - [int] The first memory address of the global.
        """
        return CompilationMemory.__global_memory.next_memory_chunk(value, var_type)

    @staticmethod
    def clear_temp_memory() -> None:
        """Clears the temporary memory."""
        CompilationMemory.__temp_memory = Memory(Scopes.TEMP, ScopeRanges.TEMP)
