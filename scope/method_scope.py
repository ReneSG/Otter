from .symbol_table import SymbolTable
from .variable import Variable
from typing import Optional


class MethodScope:
    def __init__(self, name: str, acesss_modifier: str, parent: SymbolTable):
        self._name = name
        self._access_modifier = acesss_modifier

        # These are added later, as there could be multiple arguments,
        # so we parse them one by one, and finally add the return type
        # which goes after the arguments
        self._arguments = SymbolTable(f'{name} Arguments', parent)
        self._return_type = None

        self._variables_directory = SymbolTable(name, self._arguments)

    @property
    def name(self) -> str:
        return self._name

    def add_return_type(self, return_type: str) -> None:
        self._return_type = return_type

    def add_argument(self, name: str, arg_type: str) -> None:
        self._arguments.add_symbol(Variable(name, arg_type))
        # TODO: eventually we will need to add the value for the arguments.
        # I don't know how we will do that yet.

    def add_variable(self, name: str, var_type: str, value: str) -> None:
        self._variables_directory.add_symbol(Variable(name, var_type, value))
