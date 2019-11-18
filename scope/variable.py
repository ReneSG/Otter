from typing import Optional
from helpers.types import Types
from .dimension import Dimension


class Variable:
    def __init__(self, name: str, var_type: Types, memory_space: int, access_modifier: Optional[str] = None):
        self._name = name
        self._memory_space = memory_space
        self._var_type = var_type
        self._access_modifier = access_modifier
        self._dimension_info = None
        self._dimension_count = 0
        self._size = 1

    @property
    def name(self) -> str:
        return self._name

    @property
    def var_type(self) -> Types:
        return self._var_type

    @property
    def memory_space(self) -> int:
        return self._memory_space

    @property
    def access_modifier(self) -> Optional[str]:
        return self._access_modifier

    def has_multiple_dimensions(self):
        return self._dimensions > 0

    def add_new_dimension(self, size):
        self._size *= size
        if self._dimension_count == 0:
            self._dimension_info = Dimension(size)
        else:
            current_dimension = self._dimension_info
            while current_dimension.has_next_dimension():
                current_dimension = current_dimension.next_dimension()
            current_dimension.next_dimension = Dimension(size)

        self._dimension_count += 1

    def populate_dimension_attributes(self):
        current_m = self._size
        current_dimension = self._dimension_info

        while current_dimension.has_next_dimension():
            current_m /= current_dimension.size
            current_dimension.m = int(current_m)
            current_dimension = current_dimension.next_dimension



    def debug_dimensions(self):
        print("==============")
        current_dimension = self._dimension_info
        while current_dimension:
            print(vars(current_dimension))
            current_dimension = current_dimension.next_dimension
