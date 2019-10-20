class Variable:
    def __init__(self, name: str, value: str, access_modifier: str):
        self._name = name
        self._value = value
        self._access_modifier = access_modifier
    
    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def access_modifier(self):
        return self._value
