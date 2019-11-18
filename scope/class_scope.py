from .symbol_table import SymbolTable
from .method_scope import MethodScope
from .variable import Variable
from typing import Optional
from memory.memory import Memory
from memory.ranges import ScopeRanges
from scope.scopes import Scopes


class ClassScope:
    # Recursive typing, see: https://stackoverflow.com/a/38341145
    def __init__(self, name: str, inherits: Optional["ClassScope"] = None):
        self._name = name
        if inherits is None:
            self._method_directory = SymbolTable(name)
            self._attribute_directory = SymbolTable(name)
            self._local_memory = Memory(Scopes.LOCAL, ScopeRanges.LOCAL)
        else:
            self._method_directory = SymbolTable(
                name, inherits.method_directory)
            self._attribute_directory = SymbolTable(
                name, inherits.attribute_directory)
            self._local_memory = inherits.local_memory

    @property
    def name(self) -> str:
        return self._name

    @property
    def method_directory(self) -> SymbolTable:
        return self._method_directory

    @property
    def attribute_directory(self) -> SymbolTable:
        return self._attribute_directory

    @property
    def local_memory(self) -> Memory:
        return self._local_memory

    def add_method(self, name: str, access_modifier: str) -> MethodScope:
        method_scope = MethodScope(
            name, access_modifier, self._attribute_directory, self._local_memory)
        self._method_directory.add_symbol(method_scope)

        return method_scope

    def add_attribute(self, name: str, var_type: str, access_modifier: str) -> None:
        memory_address = self._local_memory.next_memory_space(var_type)
        self._attribute_directory.add_symbol(
            Variable(f"@{name}", var_type, memory_address, access_modifier=access_modifier))
