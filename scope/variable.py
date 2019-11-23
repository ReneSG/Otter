from typing import Optional
from helpers.types import Types
from memory.ranges import ScopeRanges
from .dimension import Dimension

class Variable:
    def __init__(self, name: str, var_type: Types, memory_space: int, access_modifier: Optional[str] = None):
        """Responsible for storing all the information pertaining to a variable.

        Arguments:
            - name [str]: The name of the variable.
            - var_type [Types]: The type of the variable.
            - memory_space [int]: Where this variable is stored in memory.
            - access_modifier [str]: Optional, if a variable is global/local it does not have one. Whether the variable is public or private.  
        """
        self._name = name
        self._memory_space = memory_space
        self._var_type = var_type
        self._access_modifier = access_modifier
        self._dimension_info = None
        self._dimension_count = 0
        self._size = 1

    def __str__(self):
        return f"Var: {self._name} | Type: {self._var_type} | Access: {self._access_modifier} | Memory: {self._memory_space}"

    def __repr__(self):
        return f"<{self._name}: {self._var_type} | {self._memory_space}>"

    @property
    def name(self) -> str:
        """The name of the variable.

        Returns:
            - [str] The name of the variable.
        """
        return self._name

    @property
    def var_type(self) -> Types:
        """The type of the variable.

        Returns:
            - [Types] The type of the variable.
        """
        return self._var_type

    @property
    def size(self) -> int:
        """The size of the variable.

        Returns:
            - [int] The size of the variable.
        """
        return self._size

    @property
    def memory_space(self) -> int:
        """Where the variable is contained in memory.

        Returns:
            - [int] The memory address assigned to this variable.
        """
        return self._memory_space

    @property
    def access_modifier(self) -> Optional[str]:
        """Whether the variable is private or public.

        Returns:
            - [str | None] Returns the access_modifier if there is one. None otherwise. 
        """
        return self._access_modifier

    def has_multiple_dimensions(self) -> bool:
        """Whether the variable is an array or not.

        Returns:
            - True if the variable is an array, False otherwise.
        """
        return self._dimension_count > 0

    def add_new_dimension(self, size: int) -> None:
        """Adds a new dimension to the variable.

        Arguments:
            - size [int]: The size of the new dimension to be added.
        """
        self._size *= size
        if self._dimension_count == 0:
            self._dimension_info = Dimension(size)
        else:
            current_dimension = self._dimension_info
            while current_dimension.has_next_dimension():
                current_dimension = current_dimension.next_dimension
            current_dimension.next_dimension = Dimension(size)

        self._dimension_count += 1

    def populate_dimension_attributes(self) -> None:
        current_m = self._size
        current_dimension = self._dimension_info

        while current_dimension.has_next_dimension():
            current_m /= current_dimension.size
            current_dimension.m = int(current_m)
            current_dimension = current_dimension.next_dimension

    def is_global(self):
        return ScopeRanges.is_global(self.memory_space)

    def is_local(self):
        return ScopeRanges.is_local(self.memory_space)

    def is_temp(self):
        return ScopeRanges.is_temp(self.memory_space)

    def is_constant(self):
        return ScopeRanges.is_const(self.memory_space)

    def getDimensionNumber(self, dimension_number) -> int:
        current_dimension = self._dimension_info

        while dimension_number > 0:
            current_dimension = current_dimension.next_dimension
            dimension_number -= 1
            if current_dimension == None:
                raise ValueError(f"{self.name} is not indexable.")

        return current_dimension

    def is_array_pointer(self):
        return self._var_type == Types.ARRAY_POINTER

    def debug_dimensions(self) -> None:
        """Method used to debug the dimensions of an object."""
        print("==============")
        current_dimension = self._dimension_info
        while current_dimension:
            print(vars(current_dimension))
            current_dimension = current_dimension.next_dimension
