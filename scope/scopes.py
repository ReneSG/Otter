from enum import Enum


class Scopes(Enum):
    GLOBAL = "global"
    LOCAL = "local"
    CONSTANT = "constant"
    TEMP = "temp"

    @staticmethod
    def is_global_scope(scope: str) -> bool:
        return scope == Scopes.GLOBAL

    @staticmethod
    def is_local_scope(scope: str) -> bool:
        return scope == Scopes.LOCAL

    @staticmethod
    def is_constant_scope(scope: str) -> bool:
        return scope == Scopes.CONSTANT

    @staticmethod
    def is_temp_scope(scope: str) -> bool:
        return scope == Scopes.TEMP
