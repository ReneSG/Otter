from .variable import Variable
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SymbolTable:
    # Recursive typing, see: https://stackoverflow.com/a/38341145
    def __init__(self, name: Optional[str], parent: Optional["SymbolTable"] = None):
        self._parent = parent
        self._name = name
        self._symbols = dict()

    def __str__(self):
        return f"Name: {self._name}\n Parent: {self._parent}\n Symbols ({self._name}):\n {self._symbols}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional["SymbolTable"]:
        return self._parent

    @property
    def symbols(self) -> Dict[str, Any]:
        return self._symbols

    def search(self, name: str) -> Optional[Any]:
        if name in self._symbols:
            return self._symbols[name]
        elif self._parent:
            return self._parent.search(name)

        return None

    def add_symbol(self, symbol: Any) -> None:
        if self.search(symbol.name) is not None:
            raise Exception(
                f'Symbol "{symbol.name}" already exists in {self._name}.')

        logger.debug(f"Added {symbol.name} to {self._name}")
        self._symbols[symbol.name] = symbol
        logger.debug(self._symbols)
