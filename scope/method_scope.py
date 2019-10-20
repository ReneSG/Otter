from .symbol_table import SymbolTable

class MethodScope:
    def __init__(self, name: str, return_type: str):
        self._name = name
        self._return_type = return_type
        self._symbol_table = SymbolTable(name)
