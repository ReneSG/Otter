from scope.method_directory import MethodDirectory
from .interpreter import Interpreter

class Compiler:
    _current_method = None
    _method_directory = None
    _errors = []

    def __init__(self):
        _method_directory = MethodDirectory()
        self.__interpreter = Interpreter()

    def add_method(self, name: str, return_type: str):
        try:
            _method_directory.add_method(name)
        except error:
            _errors.append(error.message)

    def gen_quad_assign(self):
        self.__interpreter.assign()

    def gen_quad_add_op(self, op):
        self.__interpreter.push_operator(op)


