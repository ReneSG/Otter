from enum import Enum


class Scopes(Enum):
    """The Scopes for memory in which a variable can be in."""
    GLOBAL = "global"
    LOCAL = "local"
    CONSTANT = "constant"
    TEMP = "temp"

    @staticmethod
    def is_global_scope(scope: str) -> bool:
        """Checks if the scope is global.

        Returns:
            - [bool] Whether the scope is global.
        """
        return scope == Scopes.GLOBAL.value

    @staticmethod
    def is_local_scope(scope: str) -> bool:
        """Checks if the scope is local.

        Returns:
            - [bool] Whether the scope is local.
        """
        return scope == Scopes.LOCAL.value

    @staticmethod
    def is_constant_scope(scope: str) -> bool:
        """Checks if the scope is constant.

        Returns:
            - [bool] Whether the scope is constant.
        """
        return scope == Scopes.CONSTANT.value

    @staticmethod
    def is_temp_scope(scope: str) -> bool:
        """Checks if the scope is temporary.

        Returns:
            - [bool] Whether the scope is temporary.
        """
        return scope == Scopes.TEMP.value
