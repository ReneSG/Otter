from .method_scope import MethodScope

class MethodDirectory:
    def __init__(self):
        self._directory = dict()

    def add_method(self, name: str, return_type: str): 
        if name in self._directory:
            raise Exception("Method %s already declared." % name)

        self._directory[name] = MethodScope(name, return_type)