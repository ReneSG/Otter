class Dimension:
    def __init__(self, size: int, m: int = 0):
        self._size = size
        self._m = 1
        self._next_dimension = None

    @property
    def size(self) -> int:
        return self._size

    @property
    def m(self) -> int:
        return self._m

    @property
    def next_dimension(self) -> "Dimension":
        return self._next_dimension

    def has_next_dimension(self):
        return self._next_dimension != None

    @next_dimension.setter
    def next_dimension(self, dimension: "Dimension"):
        self._next_dimension = dimension

    @m.setter
    def m(self, m):
        self._m = m
