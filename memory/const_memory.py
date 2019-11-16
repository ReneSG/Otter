from .base_memory import BaseMemory
from .ranges import TypeRanges
from helpers.types import Types
from scope.variable import Variable
import logging

class ConstMemory:
    def __init__(self, scope_name: str, limits: (int, int)):
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

    def next_memory_space(self, value: str, var_type: str) -> int:
        # If value is already in memory return the existing memory space
        if (value, var_type) in self.__const_dict:
            memory_space = self.__const_dict[(value, var_type)]
            logging.debug(f"Retrieving already created const {value}: {var_type} in memory space {memory_space}.")
            return memory_space

        memory_space = 0
        if Types.is_int(var_type):
            memory_space = self.__int_memory.next_available()
        if Types.is_float(var_type):
            memory_space = self.__float_memory.next_available()
        if Types.is_bool(var_type):
            memory_space = self.__bool_memory.next_available()
        if Types.is_string(var_type):
            memory_space = self.__string_memory.next_available()

        self.__const_dict[(value, var_type)] = memory_space
        logging.debug(f"Store const {value}: {var_type} in memory space {memory_space}.")
        return memory_space



