from typing import Optional


class Variable:
    def __init__(self, name: str, var_type: str, value: Optional[str] = None, access_modifier: Optional[str] = None):
        self._name = name
        self._value = value
        self._var_type = var_type
        self._access_modifier = access_modifier

    @property
    def name(self) -> str:
        return self._name

    @property
    def var_type(self) -> str:
        return self._var_type

    @property
    def value(self) -> Optional[str]:
        return self._value

    @property
    def access_modifier(self) -> Optional[str]:
        return self._value
