from enum import Enum
from collections import namedtuple

range_tuple = namedtuple('range_tuple', 'inf max')


class ScopeRanges(Enum):
    GLOBAL = range_tuple(0, 9999)
    LOCAL = range_tuple(10000, 19999)
    CONSTANTS = range_tuple(20000, 29999)
    TEMP = range_tuple(30000, 41999)

    @staticmethod
    def is_global(value: int) -> bool:
        return ScopeRanges.GLOBAL.inf <= value <= ScopeRanges.GLOBAL.max

    @staticmethod
    def is_local(value: int) -> bool:
        return ScopeRanges.LOCAL.inf <= value <= ScopeRanges.LOCAL.max

    @staticmethod
    def is_temp(value: int) -> bool:
        return ScopeRanges.TEMP.inf <= value <= ScopeRanges.TEMP.max

    @staticmethod
    def is_const(value: int) -> bool:
        return ScopeRanges.CONSTANTS.inf <= value <= ScopeRanges.CONSTANTS.max


class TypeRanges(Enum):
    INT = range_tuple(0, 1999)
    FLOAT = range_tuple(2000, 3999)
    BOOL = range_tuple(4000, 5999)
    STRING = range_tuple(6000, 7999)
    OBJECT = range_tuple(8000, 9999)
    ARRAY_POINTER = range_tuple(10000, 11999)

    @staticmethod
    def is_int(value: int) -> bool:
        return TypeRanges.INT.inf <= value <= TypeRanges.INT.max

    @staticmethod
    def is_float(value: int) -> bool:
        return TypeRanges.FLOAT.inf <= value <= TypeRanges.FLOAT.max

    @staticmethod
    def is_boolean(value: int) -> bool:
        return TypeRanges.BOOL.inf <= value <= TypeRanges.BOOL.max

    @staticmethod
    def is_string(value: int) -> bool:
        return TypeRanges.STRING.inf <= value <= TypeRanges.STRING.max

    @staticmethod
    def is_object(value: int) -> bool:
        return TypeRanges.OBJECT.inf <= value <= TypeRanges.OBJECT.max

    @staticmethod
    def is_array_pointer(value: int) -> bool:
        return TypeRanges.ARRAY_POINTER.inf <= value <= TypeRanges.ARRAY_POINTER.max
