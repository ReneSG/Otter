from enum import Enum


class Types(Enum):

    # Primitive data types
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"
    ARRAY_POINTER = "array_pointer"
    ID = "id"

    ERROR = "error"

    @staticmethod
    def is_int(var_type: str) -> bool:
        return var_type == Types.INT

    @staticmethod
    def is_float(var_type: str) -> bool:
        return var_type == Types.FLOAT

    @staticmethod
    def is_string(var_type: str) -> bool:
        return var_type == Types.STRING

    @staticmethod
    def is_bool(var_type: str) -> bool:
        return var_type == Types.BOOL

    @staticmethod
    def is_array_pointer(var_type: str) -> bool:
        return var_type == Types.ARRAY_POINTER
