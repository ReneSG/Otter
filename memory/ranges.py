from enum import Enum
from collections import namedtuple

range_tuple = namedtuple('range_tuple', 'inf max')


def merge_ranges(scope_range: (int, int), type_range: (int, int)):
    """Merges a scope range and a type ranges.

    E.g. Local: (10000, 19999) and Bool: (4000, 5999) = (14000, 15999)

    Arguments:
        - scope_range [(int, int)]: a valid ScopeRange.
        - type_range [(int, int)]: a valid TypeRange.

    Returns:
        The merged range tuple.
    """
    inf_scope_range, _ = scope_range
    inf_type_range, max_type_range = type_range

    return (inf_scope_range + inf_type_range, inf_scope_range + max_type_range)


def remove_base_prefix(address: int) -> int:
    """Removes the inferior range of the scope from the address.

    E.g. address = 24000, CONST ranges is (20000, 29999) = 4000

    Arguments:
        - address [int]: The address to remove the prefix from.

    Returns:
        - [int] the address without the prefix.

    """
    inf_range, _ = ScopeRanges.get_range(address)
    return address - inf_range


class ScopeRanges():
    """The ranges in memory for the different types of scope."""
    GLOBAL = range_tuple(0, 9999)
    LOCAL = range_tuple(10000, 19999)
    CONSTANTS = range_tuple(20000, 29999)

    # Only temps have array pointers, so they have an extra 2,000 spaces.
    TEMP = range_tuple(30000, 41999)

    @staticmethod
    def is_global(value: int) -> bool:
        """Whether a value is global based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is global. False otherwise.
        """
        return ScopeRanges.GLOBAL.inf <= value <= ScopeRanges.GLOBAL.max

    @staticmethod
    def is_local(value: int) -> bool:
        """Whether a value is local based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is local. False otherwise.
        """
        return ScopeRanges.LOCAL.inf <= value <= ScopeRanges.LOCAL.max

    @staticmethod
    def is_temp(value: int) -> bool:
        """Whether a value is temp based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is temp. False otherwise.
        """
        return ScopeRanges.TEMP.inf <= value <= ScopeRanges.TEMP.max

    @staticmethod
    def is_const(value: int) -> bool:
        """Whether a value is const based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is const. False otherwise.
        """
        return ScopeRanges.CONSTANTS.inf <= value <= ScopeRanges.CONSTANTS.max

    @staticmethod
    def get_range(address: int) -> (int, int):
        """Gets the range an address belongs to.

        Arguments:
            - address [int] = The address to evaluate.

        Returns:
            - [(int, int)] The tuple of the ranges.

        """
        if ScopeRanges.is_global(address):
            return ScopeRanges.GLOBAL
        if ScopeRanges.is_local(address):
            return ScopeRanges.LOCAL
        if ScopeRanges.is_const(address):
            return ScopeRanges.CONSTANTS
        if ScopeRanges.is_temp(address):
            return ScopeRanges.TEMP

        raise ValueError(f"Invalid memory address: f{address}.")


class TypeRanges():
    """The ranges in memory for each data type."""
    INT = range_tuple(0, 1999)
    FLOAT = range_tuple(2000, 3999)
    BOOL = range_tuple(4000, 5999)
    STRING = range_tuple(6000, 7999)
    OBJECT = range_tuple(8000, 9999)
    ARRAY_POINTER = range_tuple(10000, 11999)

    @staticmethod
    def is_int(value: int) -> bool:
        """Whether a value is const based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is const. False otherwise.
        """
        return TypeRanges.INT.inf <= value <= TypeRanges.INT.max

    @staticmethod
    def is_float(value: int) -> bool:
        """Whether a value is a float based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is a float. False otherwise.
        """
        return TypeRanges.FLOAT.inf <= value <= TypeRanges.FLOAT.max

    @staticmethod
    def is_boolean(value: int) -> bool:
        """Whether a value is a boolean based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is a boolean. False otherwise.
        """
        return TypeRanges.BOOL.inf <= value <= TypeRanges.BOOL.max

    @staticmethod
    def is_string(value: int) -> bool:
        """Whether a value is a string based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is a string. False otherwise.
        """
        return TypeRanges.STRING.inf <= value <= TypeRanges.STRING.max

    @staticmethod
    def is_object(value: int) -> bool:
        """Whether a value is an object based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is an object. False otherwise.
        """
        return TypeRanges.OBJECT.inf <= value <= TypeRanges.OBJECT.max

    @staticmethod
    def is_array_pointer(value: int) -> bool:
        """Whether a value is an array pointer based on its address.

        Arguments:
            - value [int]: The memory address.

        Returns:
            - [bool] True if it is an array pointer. False otherwise.
        """
        return TypeRanges.ARRAY_POINTER.inf <= value <= TypeRanges.ARRAY_POINTER.max
