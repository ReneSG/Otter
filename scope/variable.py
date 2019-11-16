from typing import Optional


class Variable:
    def __init__(self, name: str, var_type: str, memory_space: int, access_modifier: Optional[str] = None):
        self._name = name
        self._memory_space = memory_space
        self._var_type = var_type
        self._access_modifier = access_modifier

    @property
    def name(self) -> str:
        return self._name

    @property
    def var_type(self) -> str:
        return self._var_type

    @property
    def memory_space(self) -> int:
        return self._memory_space

    @property
    def access_modifier(self) -> Optional[str]:
        return self._access_modifier
