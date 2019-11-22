from .base_memory import BaseMemory
from .ranges import TypeRanges
from helpers.types import Types
from scope.variable import Variable
import logging


logger = logging.getLogger(__name__)


class ConstMemory:
    def __init__(self, scope_name: str, limits: (int, int)):
        """This class is responsible for storing the constants that are parsed during compilation.

        Arguments:
            - scope_name [str]: The name of the scope.
            - limits [(int, int)]: The limits of the memory. 
        """
        self.__inf_limit, self.__max_limit = limits
        self.__scope_name = scope_name
        self.__int_memory = BaseMemory(scope_name, Types.INT, TypeRanges.INT)
        self.__float_memory = BaseMemory(
            scope_name, Types.FLOAT, TypeRanges.FLOAT)
        self.__bool_memory = BaseMemory(
            scope_name, Types.BOOL, TypeRanges.BOOL)
        self.__string_memory = BaseMemory(
            scope_name, Types.STRING, TypeRanges.STRING)
        self.__const_dict = dict()
        self.__const_dict_mirror = dict()

    def get_value(self, variable):
        return self.__const_dict.get(variable.memory_space)

    def get_value_from_address(self, address):
        return self.__const_dict.get(address)

    def next_memory_space(self, value: str, var_type: str) -> int:
        """Retrieves the next available memory space if needed. If the value was already cached it returns
        the memory address previously used.

        Arguments:
            - value [str]: The value to store.
            - var_type [str]: The type of the value.

        Returns:
            - [int] The next available memory address if it didn't already exist. Else it returns the memory address
            previously used for the same value.

        Raises:
            ValueError: If the type is not one of the primitive Data Types it raises a ValueError.
        """
        # If value is already in memory return the existing memory space
        if (value, var_type) in self.__const_dict_mirror:
            memory_space = self.__const_dict_mirror[(value, var_type)]
            logger.debug(
                f"Retrieving already created const {value}: {var_type} in memory space {memory_space}.")
            return memory_space

        memory_space = 0
        if Types.is_int(var_type):
            memory_space = self.__int_memory.next_available()
        elif Types.is_float(var_type):
            memory_space = self.__float_memory.next_available()
        elif Types.is_bool(var_type):
            memory_space = self.__bool_memory.next_available()
        elif Types.is_string(var_type):
            memory_space = self.__string_memory.next_available()
        else:
            raise ValueError(f"Unrecognized constant type '{var_type}'.")

        self.__const_dict[memory_space] = value
        self.__const_dict_mirror[(value, var_type)] = memory_space
        logger.debug(
            f"Store const {value}: {var_type} in memory space {memory_space}.")
        return memory_space
