from memory.ranges import TypeRanges, remove_base_type_prefix
from typing import Any


class RuntimeMemory:
    def __init__(self, memory_counters: (int, int, int, int, int, int)):
        print("CREATED MEMORY WITH")
        print(memory_counters)
        int_m, float_m, bool_m, string_m, object_m, ap_m = memory_counters
        self.__int_memory = [None] * int_m
        self.__float_memory = [None] * float_m
        self.__bool_memory = [None] * bool_m
        self.__string_memory = [None] * string_m
        self.__object_memory = [None] * object_m
        self.__array_pointer_memory = [None] * ap_m

    def set_value(self, address: int, value: Any):
        address_without_prefix = remove_base_type_prefix(address)
        if TypeRanges.is_int(address):
            self.__int_memory[address_without_prefix] = value
        if TypeRanges.is_float(address):
            self.__float_memory[address_without_prefix] = value
        if TypeRanges.is_bool(address):
            self.__bool_memory[address_without_prefix] = value
        if TypeRanges.is_string(address):
            self.__string_memory[address_without_prefix] = value
        if TypeRanges.is_object(address):
            self.__object_memory[address_without_prefix] = value
        if TypeRanges.is_array_pointer(address):
            self.__array_pointer_memory[address_without_prefix] = value
    
    def get_value(self, address: int) -> Any:
        address_without_prefix = remove_base_type_prefix(address)
        if TypeRanges.is_int(address):
            return self.__int_memory[address_without_prefix]
        if TypeRanges.is_float(address):
            return self.__float_memory[address_without_prefix]
        if TypeRanges.is_bool(address):
            return self.__bool_memory[address_without_prefix]
        if TypeRanges.is_string(address):
            return self.__string_memory[address_without_prefix]
        if TypeRanges.is_object(address):
            return self.__object_memory[address_without_prefix]
        if TypeRanges.is_array_pointer(address):
            return self.__array_pointer_memory[address_without_prefix]
