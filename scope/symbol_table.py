from .variable import Variable
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SymbolTable:
    # Recursive typing, see: https://stackoverflow.com/a/38341145
    def __init__(self, name: Optional[str], parent: Optional["SymbolTable"] = None):
        """The SymbolTable is responsible for keeping track of all the symbols (variables, classes, methods) of the language.

        It is very similar to a plain dictionary, except it can recursively search through its parents. This is used for 
        inheritance.

        A symbol *must* have a name attribute to be used in the data structure.

        Arguments:
            - name [str]: The name of the things we're keeping track of.
            - parent [SymbolTable]: Optional. The SymbolTable of the parent if there is one.
        """
        self._parent = parent
        self._name = name
        self._symbols = dict()

    def __str__(self):
        return f"Name: {self._name}\n Parent: {self._parent}\n Symbols ({self._name}):\n {self._symbols}"

    @property
    def name(self) -> str:
        """The name of the SymbolTable.

        Returns:
            - [str] The name of the table.
        """
        return self._name

    @property
    def parent(self) -> Optional["SymbolTable"]:
        """The parent of the SymbolTable.

        Returns:
            - The SymbolTable if there is a parent. None otherwise.
        """
        return self._parent

    @property
    def symbols(self) -> Dict[str, Any]:
        """The symbols (variables, methods, classes, etc.) contained in this instance.

        Returns:
            - [Dict(str, Any)] The dictionary containing the symbols.
        """
        return self._symbols

    def search(self, name: str) -> Optional[Any]:
        """Searches recursively through the SymbolTable and its parents to find a symbol.

        Arguments:
            - name [str]: The name of the symbol we are looking for.

        Returns:
            - The symbol's value if found. None otherwise.
        """
        if name in self._symbols:
            return self._symbols[name]
        elif self._parent:
            return self._parent.search(name)

        return None

    def add_symbol(self, symbol: Any) -> None:
        """Adds a symbol to the table.

        Arguments:
            - symbol [Any]: The symbol to add. MUST have name attribute to be added.

        Raises:
            - Exception: if the symbol is already in the table it raises an Exception.
        """
        if self.search(symbol.name) is not None:
            raise Exception(
                f'Symbol "{symbol.name}" already exists in {self._name}.')

        logger.debug(f"Added {symbol.name} to {self._name}")
        self._symbols[symbol.name] = symbol
        logger.debug(self._symbols)
