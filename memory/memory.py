from .base_memory import BaseMemory
from .ranges import TypeRanges
from helpers.types import Types
from scope.variable import Variable
from scope.scopes import Scopes


class Memory:
    def __init__(self, scope_name: str, limits: (int, int)):
        """The Memory class groups several BaseMemory classes of different types (int, string, bool, float, objects, pointers).

        Arguments:
            - scope_name [str]: The name of the scope
            - limits [(int, int)]: The limits of this type of scope. One of ScopeRanges.
        """
        self.__inf_limit = limits.inf
        self.__max_limit = limits.max
        self.__scope_name = scope_name
        self.__int_memory = BaseMemory(scope_name, Types.INT, TypeRanges.INT)
        self.__float_memory = BaseMemory(
            scope_name, Types.FLOAT, TypeRanges.FLOAT)
        self.__bool_memory = BaseMemory(
            scope_name, Types.BOOL, TypeRanges.BOOL)
        self.__string_memory = BaseMemory(
            scope_name, Types.STRING, TypeRanges.STRING)
        self.__object_memory = BaseMemory(
            scope_name, Types.OBJECT, TypeRanges.OBJECT)

        # If memory is temporary we need to store array pointer values as well.
        if Scopes.is_temp_scope(scope_name):
            self.__array_pointer_memory = BaseMemory(
                scope_name, Types.ARRAY_POINTER, TypeRanges.ARRAY_POINTER)

    def next_memory_space(self, var_type: str) -> int:
        """Gets the next memory address for the type of variable.

        Arguments:
            - var_type [str]: The type of the variable.

        Returns:
            - [int] The memory address for the variable.

        Raises:
            - Exception: If the limits of the memory are exceeded.
        """
        if Types.is_int(var_type):
            return self.__int_memory.next_available()
        if Types.is_float(var_type):
            return self.__float_memory.next_available()
        if Types.is_bool(var_type):
            return self.__bool_memory.next_available()
        if Types.is_string(var_type):
            return self.__string_memory.next_available()
        if Types.is_array_pointer(var_type):
            return self.__array_pointer_memory.next_available()

        return self.__object_memory.next_available()

    def next_memory_chunk(self, var_type: str, chunk_size: int) -> int:
        """Gets the next memory address chunk for the type of variable.

        Arguments:
            - var_type [str]: The type of the variable.

        Returns:
            - [int] The memory address for the variable.

        Raises:
            - Exception: If the limits of the memory are exceeded.
        """
        if Types.is_int(var_type):
            return self.__int_memory.next_memory_chunk(chunk_size)
        if Types.is_float(var_type):
            return self.__float_memory.next_memory_chunk(chunk_size)
        if Types.is_bool(var_type):
            return self.__bool_memory.next_memory_chunk(chunk_size)
        if Types.is_string(var_type):
            return self.__string_memory.next_memory_chunk(chunk_size)
        if Types.is_array_pointer(var_type):
            raise ValueError(
                "Unable to get memory chunk for ARRAY_POINTER type.")

        return self.__object_memory.next_memory_chunk(chunk_size)
