from scope.class_scope import ClassScope
from scope.method_scope import MethodScope
from scope.symbol_table import SymbolTable
from typing import List, Optional
import logging

logging.basicConfig(level=logging.DEBUG)


class Compiler:
    _current_method: MethodScope = None
    _current_class: ClassScope = ClassScope("Global Scope")
    _class_directory: SymbolTable = SymbolTable("Global Scope")

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
            logging.debug(
                f"Added class: {class_name}, inherits: {inherit_name}")
            Compiler._current_class = class_scope
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def add_instance_variable(name: str, var_type: str, access_modifier: str) -> None:
        try:
            Compiler._current_class.add_attribute(
                name, var_type, access_modifier)
            logging.debug(
                f"Added attribute: {access_modifier} {name} {var_type}, to class: {Compiler._current_class.name}")
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def add_method(name: str, access_modifier: str) -> None:
        method_scope = MethodScope(
            name, access_modifier, Compiler._current_class.attribute_directory)
        try:
            Compiler._current_class.add_method(method_scope)
            logging.debug(
                f"Added method: {name}, to class: {Compiler._current_class.name}")
            Compiler._current_method = method_scope
        except Exception as error:
            Compiler.errors.append(error)

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
            logging.debug(
                f"Added argument: {name} {arg_type}, in method {Compiler._current_method.name}")
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def add_return_type(return_type: str) -> None:
        Compiler._current_method.add_return_type(return_type)
        logging.debug(
            f"Added return type: {return_type}, in method {Compiler._current_method.name}")

    @staticmethod
    def add_variable(name: str, var_type: str, value: Optional[str]) -> None:
        try:
            if Compiler._current_method is not None:
                Compiler._current_method.add_variable(name, var_type, value)
                logging.debug(
                    f"Added var: {name} {var_type} = {value}, in method {Compiler._current_method.name}")
            else:
                # This is a global variable, it will be added as a private attribute
                # To not be used as a public instance variable.
                Compiler._current_class.add_attribute(name, var_type, "private", value)
                logging.debug(
                    f"Added global var: {name} {var_type} = {value}, in {Compiler._current_class.name}")
                
        except Exception as error:
            logging.debug(f"Error adding var: {name} {var_type} = {value}, in method ")
            Compiler.errors.append(error)
