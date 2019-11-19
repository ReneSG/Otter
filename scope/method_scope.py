from .symbol_table import SymbolTable
from .variable import Variable
from memory.compilation_memory import CompilationMemory
from memory.memory import Memory
from typing import Optional
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)


class MethodScope:
    def __init__(self, name: str, access_modifier: str, parent: Optional[SymbolTable] = None, parent_memory: Optional[Memory] = None):
        self._name = name
        self._access_modifier = access_modifier
        self._parent = parent
        self._local_memory = deepcopy(parent_memory)

        if parent is not None:
            logger.debug(
                f"Created MethodScope {access_modifier} {name}, parent {parent.name}")
            logger.debug(parent)     

        # These are added later, as there could be multiple arguments,
        # so we parse them one by one, and finally add the return type
        # which goes after the arguments
        self._arguments = SymbolTable(f'{name} Arguments', parent)
        self._return_type = None
        self._return_memory_address = -1

        self._variables_directory = SymbolTable(name, self._arguments)

    @property
    def name(self) -> str:
        return self._name

    @property
    def variables_directory(self) -> SymbolTable:
        return self._variables_directory

    @property
    def return_type(self) -> str:
        return self._return_type

    @property
    def _return_memory_address(self):
        return self._return_memory_address

    def add_return_type(self, return_type: str) -> None:
        self._return_type = return_type
        if return_type != "void":
            self._return_memory_address = CompilationMemory.next_global_memory_space(return_type)

    def add_argument(self, name: str, arg_type: str) -> None:
        memory_space = self._local_memory.next_memory_space(arg_type)
        self._arguments.add_symbol(Variable(name, arg_type, memory_space))
        # TODO: eventually we will need to add the value for the arguments.
        # I don't know how we will do that yet.

    def add_variable(self, name: str, var_type: str) -> None:
        # It belongs to global memory if it has no parent.
        if self._local_memory is not None:
            memory_space = self._local_memory.next_memory_space(var_type)
        else:
            memory_space = CompilationMemory.next_global_memory_space(var_type)

        self._variables_directory.add_symbol(
            Variable(name, var_type, memory_space))
