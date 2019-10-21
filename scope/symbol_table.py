from .variable import Variable

class SymbolTable:
    def __init__(self, name: str, parent):
        self._parent = parent
        self._name = name
        self._symbols = dict()

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    def search(self, name: str):
        if name in self._symbols:
            return self._symbols[name]
        elif self._parent:
            return self._parent.search(name)

        return None

    def add_symbol(self, symbol: Variable):
        if self.search(symbol.name):
            raise Exception("Symbol already exists.")
        
        self._symbols[symbol.name] = symbol
