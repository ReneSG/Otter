from scope.method_directory import MethodDirectory

class Compiler:
    _current_method = None
    _method_directory = None
    _errors = []

    def __init__(self):
        _method_directory = MethodDirectory()

    def add_method(self, name: str, return_type: str):
        try:
            _method_directory.add_method(name)
        except error:
            _errors.append(error.message)

