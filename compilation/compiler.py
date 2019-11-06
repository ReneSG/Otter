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

    def push_op(self, op):
        self.__interpreter.push_operator(op)

    def open_par(self):
        self.__interpreter.open_par()

    def close_par(self):
        self.__interpreter.close_par()

    def push_constant(self, type_, value):
        self.__interpreter.push_constant(type_, value)

    def check_pending_sum_sub(self):
        self.__interpreter.check_pending_sum_sub()

    def check_pending_div_prod(self):
        self.__interpreter.check_pending_div_prod()

    def check_pending_rel_op(self):
        self.__interpreter.check_pending_rel_op()

    def check_pending_and_or(self):
        self.__interpreter.check_pending_and_or()

    def maybe_gen_not_quad(self):
        self.__interpreter.maybe_gen_not_quad()

    def start_condition_quad(self):
        self.__interpreter.start_condition_quad()

    def end_condition_quad(self):
        self.__interpreter.end_condition_quad()

    def start_else_if_quad(self):
        self.__interpreter.start_else_if_quad()

    def end_else_if_quad(self):
        self.__interpreter.end_else_if_quad()

    def start_else_if_quad(self):
        self.__interpreter.start_else_if_quad()

    def end_else_if_quad(self):
        self.__interpreter.end_else_if_quad()

    def gen_goto_quad(self):
        self.__interpreter.gen_goto_quad()
