from .symbol_table import SymbolTable
from .method_scope import MethodScope
from .variable import Variable
from typing import Optional


class ClassScope:
    # Recursive typing, see: https://stackoverflow.com/a/38341145
    def __init__(self, name: str, inherits: Optional["ClassScope"] = None):
        self._name = name
        if inherits is None:
            self._method_directory = SymbolTable(name)
            self._attribute_directory = SymbolTable(name)
        else:
            self._method_directory = SymbolTable(
                name, inherits.method_directory)
            self._attribute_directory = SymbolTable(
                name, inherits.attribute_directory)

    @property
    def name(self) -> str:
        return self._name

    @property
    def method_directory(self) -> SymbolTable:
        return self._method_directory

    @property
    def attribute_directory(self) -> SymbolTable:
        return self._attribute_directory

    def add_method(self, method_scope: MethodScope) -> None:
        self._method_directory.add_symbol(method_scope)

    def add_attribute(self, name: str, var_type: str, access_modifier: str, value: Optional[str] = None) -> None:
        self._method_directory.add_symbol(
            Variable(name, var_type, value, access_modifier))
