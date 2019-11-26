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
        """ClassScope is responsible for keeping track of a classes methods, attributes, and local memory.

        Arguments:
            - name [str]: The name of the class.
            - inherits [ClassScope]: The class scope of the parent class if there is one.
        """
        self._name = name
        if inherits is None:
            self._method_directory = SymbolTable(name)
            self._attribute_directory = SymbolTable(name)
            self._instance_memory = Memory(
                Scopes.INSTANCE, ScopeRanges.INSTANCE)
        else:
            self._method_directory = SymbolTable(
                name, inherits.method_directory)
            self._attribute_directory = SymbolTable(
                name, inherits.attribute_directory)
            self._instance_memory = inherits.instance_memory

    @property
    def name(self) -> str:
        """The name of the class.

        Returns:
            - The name [str] of the class.
        """
        return self._name

    @property
    def method_directory(self) -> SymbolTable:
        """The SymbolTable which keeps track of the methods in the class.

        Returns:
            - The SymbolTable instance. 
        """
        return self._method_directory

    @property
    def attribute_directory(self) -> SymbolTable:
        """The SymbolTable which keeps track of the attributes in the class.

        Returns:
            - The SymbolTable instance.
        """
        return self._attribute_directory

    @property
    def instance_memory(self) -> Memory:
        return self._instance_memory

    def add_method(self, name: str, access_modifier: str) -> MethodScope:
        """Adds a method to the class.

        Arguments:
            - name [str]: The name of the method.
            - access_modifier [str]: Whether the method is public or private.

        Returns:
            - The MethodScope object created for this method.
        """
        method_scope = MethodScope(
            name, access_modifier, self._attribute_directory)
        self._method_directory.add_symbol(method_scope)

        return method_scope

    def add_attribute(self, name: str, var_type: str, access_modifier: str) -> None:
        """Adds an attribute to the class.

        Arguments:
            - name [str]: The name of the attribute.
            - var_type [str]: The type of the attribute.
            - access_modifier [str]: Whether the attribute is public or private.
        """
        memory_address = self._instance_memory.next_memory_space(var_type)
        self._attribute_directory.add_symbol(
            Variable(f"@{name}", var_type, memory_address, access_modifier=access_modifier))
