from .symbol_table import SymbolTable
from .variable import Variable
from memory.compilation_memory import CompilationMemory
from memory.memory import Memory
from memory.ranges import ScopeRanges
from typing import Optional
from scope.scopes import Scopes
import logging

logger = logging.getLogger(__name__)


class MethodScope:
    def __init__(self, name: str, access_modifier: str, parent: Optional[SymbolTable] = None):
        """The MethodScope object is responsible for keeping track of the information of a method.

        Arguments:
            - name [str]: The name of the method.
            - access_modifier [str]: Whether the method is public of private.
            - parent [SymbolTable]: The method's parent class attribute_directory, only Optional for the Global Scope.
            - parent_memory [Memory]: The memory of the parent class, only Optional for the Global Scope.
        """
        self._name = name
        self._access_modifier = access_modifier
        self._parent = parent
        self._local_memory = Memory(Scopes.LOCAL, ScopeRanges.LOCAL)
        self._instruction_pointer = None

        if parent is not None:
            logger.debug(
                f"Created MethodScope {access_modifier} {name}, parent {parent.name}")

        # These are added later, as there could be multiple arguments,
        # so we parse them one by one, and finally add the return type
        # which goes after the arguments
        self._arguments = SymbolTable(f'{name} Arguments', parent)
        self._ordered_arguments = []
        self._return_type = None
        self._return_memory_address = -1

        self._variables_directory = SymbolTable(name, self._arguments)

    @property
    def access_modifier(self):
        return self._access_modifier
    @property
    def name(self) -> str:
        """The name of the class.
        
        Returns:
            - The name [str] of the method.
        """
        return self._name

    @property
    def variables_directory(self) -> SymbolTable:
        """The SymbolTable which keeps track of the variables in the method.

        Returns:
            - The SymbolTable instance. 
        """
        return self._variables_directory

    @property
    def return_type(self) -> str:
        """The return type of the method.

        Returns:
            - The return type [str] of the method.
        """
        return self._return_type

    @property
    def return_memory_address(self) -> int:
        """Where the return value of the method will point to in memory.
        
        Returns:
            - The address [int] where the value of the return will be stored.
        """
        return self._return_memory_address

    @property
    def ordered_arguments(self):
        return self._ordered_arguments

    def add_return_type(self, return_type: str) -> None:
        """Adds the return type to the method after parsing it.
        
        Arguments:
            - return_type [str]: The return type of the method.
        """
        self._return_type = return_type
        if return_type != "void":
            address = CompilationMemory.next_global_memory_space(return_type)
            self._return_memory_address = Variable(address, return_type, address)

    def add_argument(self, name: str, arg_type: str) -> None:
        """Adds an argument to the method.

        Arguments:
            - name [str]: The name of the argument.
            - arg_type [str]: The type of the argument.
        """
        memory_space = self._local_memory.next_memory_space(arg_type)
        variable = Variable(name, arg_type, memory_space)
        self._arguments.add_symbol(variable)
        self._ordered_arguments.append(variable)

    def add_variable(self, name: str, var_type: str) -> None:
        """Adds a variable to the method after parsing it. 

        Arguments:
            - name [str]: The name of the variable.
            - var_type [str]: The type of the variable.
        """
        # It belongs to global memory if it has no parent.
        if self._parent is not None:
            memory_space = self._local_memory.next_memory_space(var_type)
        else:
            memory_space = CompilationMemory.next_global_memory_space(var_type)

        self._variables_directory.add_symbol(
            Variable(name, var_type, memory_space))

    def allocate_memory_chunk(self, variable) -> None:
        if variable.is_global():
            CompilationMemory.next_global_memory_chunk(variable.var_type, variable.size - 1)
        elif variable.is_local():
            self._local_memory.next_memory_chunk(variable.var_type, variable.size - 1)

    @property
    def instruction_pointer(self):
        return self._instruction_pointer

    @instruction_pointer.setter
    def instruction_pointer(self, ip):
        self._instruction_pointer = ip
