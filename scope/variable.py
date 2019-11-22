from typing import Optional
from helpers.types import Types
from .dimension import Dimension


class Variable:
    def __init__(self, name: str, var_type: Types, memory_space: int, access_modifier: Optional[str] = None):
        """Responsible for storing all the information pertaining to a variable.

        Arguments:
            - name [str]: The name of the variable.
            - var_type [Types]: The type of the variable.
            - memory_space [int]: Where this variable is stored in memory.
            - access_modifier [str]: Optional, if a variable is global it does not have one. Whether the variable is public or private.  
        """
        self._name = name
        self._memory_space = memory_space
        self._var_type = var_type
        self._access_modifier = access_modifier
        self._dimension_info = None
        self._dimension_count = 0
        self._size = 1

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

    def getDimensionNumber(self, dimension_number) -> int:
        current_dimension = self._dimension_info

        while dimension_number > 0:
            current_dimension = current_dimension.next_dimension
            dimension_number -= 1
            if current_dimension == None:
                raise ValueError(f"{self.name} is not indexable.")

        return current_dimension

    def debug_dimensions(self) -> None:
        """Method used to debug the dimensions of an object."""
        print("==============")
        current_dimension = self._dimension_info
        while current_dimension:
            print(vars(current_dimension))
            current_dimension = current_dimension.next_dimension
