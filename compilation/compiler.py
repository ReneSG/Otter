from .interpreter import Interpreter
from scope.class_scope import ClassScope
from scope.method_scope import MethodScope
from scope.symbol_table import SymbolTable
from typing import List, Optional
from memory.compilation_memory import CompilationMemory
from helpers.types import Types
import logging


FORMAT = "%(name)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('compiler.Compiler')


class Compiler:
    _global_scope: MethodScope = MethodScope("Global Scope", "private")
    _current_method: MethodScope = _global_scope
    _current_class: ClassScope = None
    _class_directory: SymbolTable = SymbolTable("Global Scope")
    _interpreter = Interpreter()

    errors: List[str] = []

    @staticmethod
    def add_class(class_name: str, inherit_name: Optional[str]):
        inherits_scope = None

        # If there is inheritance look for parent class.
        if inherit_name is not None:
            inherits_scope = Compiler._class_directory.search(inherit_name)
            if inherits_scope is None:
                Compiler.errors.append(
                    f"Parent class {inherit_name} does not exist.")
                return

        try:
            class_scope = ClassScope(class_name, inherits_scope)
            Compiler._class_directory.add_symbol(class_scope)
            logger.debug(
                f"Added class: {class_name}, inherits: {inherit_name}")
            Compiler._current_class = class_scope
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def end_class_scope() -> None:
        Compiler._current_class = None

    @staticmethod
    def add_instance_variable(name: str, var_type: str, access_modifier: str) -> None:
        try:
            Compiler._current_class.add_attribute(
                name, var_type, access_modifier)
            logger.debug(
                f"Added attribute: {access_modifier} {name} {var_type}, to class: {Compiler._current_class.name}")
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def add_method(name: str, access_modifier: str) -> None:
        method_scope = MethodScope(
            name, access_modifier, Compiler._current_class.attribute_directory)
        try:
            Compiler._current_class.add_method(method_scope)
            logger.debug(
                f"Added method: {name}, to class: {Compiler._current_class.name}")
            Compiler._current_method = method_scope
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def end_method_scope() -> None:
        Compiler._current_method = Compiler._global_scope
        Compiler._interpreter.add_end_function_quad()

    @staticmethod
    def add_constructor(name: str, access_modifier: str) -> None:
        if Compiler._current_class.name != name:
            Compiler.errors.append(
                f"Constructor {name} must have the same name as the class {Compiler._current_class.name}")

        Compiler.add_method(f"constructor_{name}", access_modifier)

    @staticmethod
    def add_method_argument(name: str, arg_type: str) -> None:
        try:
            Compiler._current_method.add_argument(name, arg_type)
            logger.debug(
                f"Added argument: {name} {arg_type}, in method {Compiler._current_method.name}")
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def add_return_type(return_type: str) -> None:
        Compiler._current_method.add_return_type(return_type)
        logger.debug(
            f"Added return type: {return_type}, in method {Compiler._current_method.name}")

    @staticmethod
    def add_variable(name: str, var_type: str, value: Optional[str] = None) -> None:
        try:
            if Compiler._current_method is not None:
                Compiler._current_method.add_variable(name, Types(var_type), value)
                logger.debug(
                    f"Added var: {name} {var_type} = {value}, in method {Compiler._current_method.name}")
            else:
                # This is a global variable, it will be added as a private attribute
                # To not be used as a public instance variable.
                memory_space = CompilationMemory.next_global_memory_space(
                    var_type)
                Compiler._current_class.add_attribute(
                    name, var_type, "private", memory_space)
                logger.debug(
                    f"Added global var: {name} {var_type} = {value}, in {Compiler._current_class.name}")

        except Exception as error:
            logger.debug(
                f"Error adding var: {name} {var_type} = {value}, in method. {error}")
            Compiler.errors.append(error)

    @staticmethod
    def add_dimension(name: str, size: int):
        variable = Compiler._current_method.variables_directory.search(name)
        variable.add_new_dimension(int(size))

    @staticmethod
    def populate_dimension_attributes(name: str):
        variable = Compiler._current_method.variables_directory.search(name)
        variable.populate_dimension_attributes()

    @staticmethod
    def gen_quad_assign():
        Compiler._interpreter.assign()

    @staticmethod
    def push_op(op):
        Compiler._interpreter.push_operator(op)

    @staticmethod
    def open_par():
        Compiler._interpreter.open_par()

    @staticmethod
    def close_par():
        Compiler._interpreter.close_par()

    @staticmethod
    def push_constant(type_, value):
        memory_space = CompilationMemory.next_const_memory_space(value, type_)
        Compiler._interpreter.push_constant(type_, memory_space)

    @staticmethod
    def push_variable(name):
        if Compiler._current_method is not None:
            current_scope = Compiler._current_method
        else:
            current_scope = Compiler._current_class

        Compiler._interpreter.push_variable(current_scope, name)

    @staticmethod
    def check_pending_sum_sub():
        Compiler._interpreter.check_pending_sum_sub()

    @staticmethod
    def check_pending_div_prod():
        Compiler._interpreter.check_pending_div_prod()

    @staticmethod
    def check_pending_rel_op():
        Compiler._interpreter.check_pending_rel_op()

    @staticmethod
    def check_pending_and_or():
        Compiler._interpreter.check_pending_and_or()

    @staticmethod
    def maybe_gen_not_quad():
        Compiler._interpreter.maybe_gen_not_quad()

    @staticmethod
    def start_condition_quad(isUnless=False):
        Compiler._interpreter.start_condition_quad(isUnless)

    @staticmethod
    def end_condition_quad():
        Compiler._interpreter.end_condition_quad()

    @staticmethod
    def gen_goto_quad():
        Compiler._interpreter.gen_goto_quad()

    @staticmethod
    def push_instruction_address():
        Compiler._interpreter.push_instruction_address()

    @staticmethod
    def end_while_quad():
        Compiler._interpreter.end_while_quad()

    @staticmethod
    def read_quad():
        Compiler._interpreter.read_quad()

    @staticmethod
    def write_quad():
        Compiler._interpreter.write_quad()

    @staticmethod
    def return_quad():
        Compiler._interpreter.return_quad()

    @staticmethod
    def start_for_quad():
        Compiler._interpreter.start_for_quad()

    @staticmethod
    def end_for_quad():
        Compiler._interpreter.end_for_quad()

    @staticmethod
    def debug_quads():
        Compiler._interpreter.debug_quads()

    @staticmethod
    def resolve_dimension_access():
        Compiler._interpreter.resolve_dimension_access()

    @staticmethod
    def complete_dimension_access():
        Compiler._interpreter.complete_dimension_access()

    @staticmethod
    def allocate_mem_quad(instance, method):
        Compiler._interpreter.allocate_mem_quad(instance, method)

    @staticmethod
    def add_method_parameter():
        Compiler._interpreter.add_method_parameter()

    @staticmethod
    def complete_method_call(method):
        Compiler._interpreter.complete_method_call(method)
