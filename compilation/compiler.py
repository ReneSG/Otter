from .interpreter import Interpreter
from scope.class_scope import ClassScope
from scope.method_scope import MethodScope
from scope.symbol_table import SymbolTable
from typing import List, Optional
from memory.compilation_memory import CompilationMemory
from helpers.types import Types
import logging


FORMAT = "%(name)-25s %(message)s"
# logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logger = logging.getLogger('compiler.Compiler')


class Compiler:
    """The compiler is a static class responsible for taking all the input from the 
       Parser/Lexer and adding it to the correct places (Interpreter, Scopes, Directories), 
       as well as handling errors.

       The main parts of the Compiler are:
         _global_scope [MethodScope] = Keeps track of all the global variables in our program.
         _current_method [MethodScope] = Keeps track of the current method being parsed, this allows
            us to add all the parameters, return type, and adding the variables to the correct
            method.
         _current_class [ClassScope] = Keeps track of the current class being parsed, this allows us
           to add all the methods and attributes to the correct class.
         _interpreter [Interpreter] = Responsible for generating all the quadruples based on input from
           the parser.
         errors [List[str]]: Responsible for keeping track of all errors in Otter.
    """
    _global_scope: MethodScope = MethodScope("Global Scope", "private")
    _current_method: MethodScope = _global_scope
    _current_class: ClassScope = None
    _class_directory: SymbolTable = SymbolTable("Global Scope")
    _interpreter = Interpreter()

    errors: List[str] = []

    @staticmethod
    def get_quads():
        return Compiler._interpreter.get_quads()

    @staticmethod
    def add_class(class_name: str, inherit_name: Optional[str]) -> None:
        """Adds a class to the class directory. Makes it the _current_class.

        Arguments:
            - class_name [str]: The class name.
            - inherit_name [str]: Optional. The name of the parent class it inherits from.
        """
        inherits_scope = None

        # If there is inheritance look for parent class.
        if inherit_name is not None:
            inherits_scope = Compiler._class_directory.search(inherit_name)
            if inherits_scope is None:
                Compiler.errors.append(
                    f"Parent class {inherit_name} does not exist.")
                return

        try:
            class_scope = ClassScope(class_name, inherits_scope, Compiler._global_scope.variables_directory)
            Compiler._class_directory.add_symbol(class_scope)
            logger.debug(
                f"Added class: {class_name}, inherits: {inherit_name}")
            Compiler._current_class = class_scope
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def end_class_scope() -> None:
        """Sets the _current_class to None. This is done when it finishes parsing a Class."""
        Compiler._current_class = None

    @staticmethod
    def end_class_constructor() -> None:
        Compiler._interpreter.add_end_constructor_quad(Compiler._current_method)

    @staticmethod
    def add_instance_variable(name: str, var_type: str, access_modifier: str) -> None:
        """Adds an instance variable to _current_class attribute table.

        Arguments:
            - name [str]: The name of the variable.
            - var_type [str]: The type of the variable.
            - access_modifier [str]: Either 'public' or 'private'.
        """
        try:
            Compiler._current_class.add_attribute(
                name, var_type, access_modifier)
            logger.debug(
                f"Added attribute: {access_modifier} {name} {var_type}, to class: {Compiler._current_class.name}")
        except Exception as error:
            logger.debug(
                f"Error adding instance var: {name} {var_type}, in method {Compiler._current_method.name}. {error}")
            Compiler.errors.append(error)

    @staticmethod
    def add_method(name: str, access_modifier: str) -> None:
        """Adds a method to _current_class method table.

        Arguments:
            - name [str]: The name of the method.
            - access_modifier [str]: Either 'public' or 'private'.
        """
        try:
            # Clear temporary when starting new method.
            CompilationMemory.clear_temp_memory()

            method_scope = Compiler._current_class.add_method(
                name, access_modifier)
            logger.debug(
                f"Added method: {name}, to class: {Compiler._current_class.name}")
            Compiler._current_method = method_scope

        except Exception as error:
            raise error
            Compiler.errors.append(error)

    @staticmethod
    def end_method_scope() -> None:
        """Ends the scope of _current_method. Sets it back to the global scope."""
        logger.debug(f"Ended method {Compiler._current_method.name} scope.")
        Compiler._interpreter.add_end_function_quad(Compiler._current_method)
        Compiler._current_method = Compiler._global_scope

    @staticmethod
    def add_constructor(name: str, access_modifier: str) -> None:
        """Adds a constructor to _current_class. 
        
        The constructor is treated as any other method, the only difference it its return value is always
        the name of the object. It is stored as 'constructor_' + the class name in the method table.

        Arguments:
            - name [str]: The name of the constructor.
            - access_modifier [str]: Either 'public' or 'private'.
        """
        if Compiler._current_class.name != name:
            Compiler.errors.append(
                f"Constructor {name} must have the same name as the class {Compiler._current_class.name}")

        Compiler.add_method(f"constructor_{name}", access_modifier)
        Compiler.add_return_type(name)
        if name == "Main":
            Compiler._interpreter.gen_start_quad()

    @staticmethod
    def add_method_argument(name: str, arg_type: str) -> None:
        """Adds an argument to _current_method.

        Arguments:
            - name [str]: The name of the argument.
            - arg_type [str]: The type of the argument.
        """
        try:
            Compiler._current_method.add_argument(name, arg_type)
            logger.debug(
                f"Added argument: {name} {arg_type}, in method {Compiler._current_method.name}")
        except Exception as error:
            Compiler.errors.append(error)

    @staticmethod
    def add_return_type(return_type: str) -> None:
        """Adds the return type to _current_method.

        Arguments:
            - return_type [str]: The return type.
        """
        Compiler._current_method.add_return_type(return_type)
        Compiler._current_method.instruction_pointer = Compiler._interpreter.getNextInstructionAddr()
        logger.debug(
            f"Added return type: {return_type}, in method {Compiler._current_method.name}")

    @staticmethod
    def add_variable(name: str, var_type: str) -> None:
        """Adds a variable to the _current_method variable table.

        Arguments:
            - name [str]: The name of the variable.
            - var_type [str]: The type of the variable.
        """
        try:
            Compiler._current_method.add_variable(name, var_type)
            logger.debug(
                f"Added var: {name} {var_type}, in method {Compiler._current_method.name}")

        except Exception as error:
            logger.debug(
                f"Error adding var: {name} {var_type}, in method {Compiler._current_method.name}. {error}")
            Compiler.errors.append(error)

    @staticmethod
    def add_dimension(name: str, size: int):
        """ Adds the dimension to a multi dimensional variable.

            Arguments:
                - name [str]: The name of the variable
                - size [str]: The size of the dimension.
        """
        variable = Compiler._current_method.variables_directory.search(name)
        variable.add_new_dimension(int(size))

    @staticmethod
    def populate_dimension_attributes(name: str):
        """ Handler to compute the dimension of a variable.

            Arguments:
                - name [str]: The name of the variable.
        """
        variable = Compiler._current_method.variables_directory.search(name)
        variable.populate_dimension_attributes()
        Compiler._current_method.allocate_memory_chunk(variable)

    @staticmethod
    def gen_quad_assign():
        """ Compiler handler for assign quad.
        """
        Compiler._interpreter.assign()

    @staticmethod
    def push_op(op):
        """ Compiler handler for pushing an operator.
        """
        Compiler._interpreter.push_operator(op)

    @staticmethod
    def open_par():
        """ Compiler handler for open_par.
        """
        Compiler._interpreter.open_par()

    @staticmethod
    def close_par():
        """ Compiler handler for close_par.
        """
        Compiler._interpreter.close_par()

    @staticmethod
    def push_constant(type_: str, value: int):
        """ Compiler handler for pushing a constant.

            Arguments:
                - type_ [str]: Type of constant.
                - value [str]: Value of constant.
        """
        memory_space = CompilationMemory.next_const_memory_space(value, type_)
        Compiler._interpreter.push_constant(type_, memory_space)

    @staticmethod
    def push_variable(name):
        """ Compiler handler for pushing a variable.

            Arguments:
                - name [str]: Name of variable.
        """
        current_scope = Compiler._current_method
        # logger.debug(current_scope.variables_directory)

        Compiler._interpreter.push_variable(current_scope, name)

    @staticmethod
    def check_pending_sum_sub():
        """ Compiler handler to check pending sum or substractions.
        """
        Compiler._interpreter.check_pending_sum_sub()

    @staticmethod
    def check_pending_div_prod():
        """ Compiler handler to check pending division or products..
        """
        Compiler._interpreter.check_pending_div_prod()

    @staticmethod
    def check_pending_rel_op():
        """ Compiler handler to check pending relational operations.
        """
        Compiler._interpreter.check_pending_rel_op()

    @staticmethod
    def check_pending_and_or():
        """ Compiler handler to check pending boolean operations.
        """
        Compiler._interpreter.check_pending_and_or()

    @staticmethod
    def maybe_gen_not_quad():
        """ Compiler handler to check pending not operations..
        """
        Compiler._interpreter.maybe_gen_not_quad()

    @staticmethod
    def start_condition_quad(isUnless: bool = False):
        """ Compiler handler to start a condition.

            Arguments:
                - is_unless [bool]: Wether is an unless statement
        """
        Compiler._interpreter.start_condition_quad(isUnless)

    @staticmethod
    def end_condition_quad():
        """ Compiler handler to end a condition.
        """
        Compiler._interpreter.end_condition_quad()

    @staticmethod
    def gen_goto_quad():
        """ Compiler handler to generate a GOTO quad.
        """
        Compiler._interpreter.gen_goto_quad()

    @staticmethod
    def push_instruction_address():
        """ Compiler handler to push a instrution address.
        """
        Compiler._interpreter.push_instruction_address()

    @staticmethod
    def push_next_instruction_address():
        """ Compiler handler to push the next instrution address.
        """
        Compiler._interpreter.push_next_instruction_address()

    @staticmethod
    def end_while_quad():
        """ Compiler handler to end a loop.
        """
        Compiler._interpreter.end_while_quad()

    @staticmethod
    def read_quad():
        """ Compiler handler generate a read quad.
        """
        Compiler._interpreter.read_quad()

    @staticmethod
    def write_quad():
        """ Compiler handler generate a write quad.
        """
        Compiler._interpreter.write_quad()

    @staticmethod
    def return_quad():
        """ Compiler handler generate a return quad.
        """
        if "constructor" in Compiler._current_method.name:
            raise Exception("Constructor cannot have a return statement.")
        Compiler._interpreter.return_quad(Compiler._current_method)

    @staticmethod
    def start_for_quad():
        """ Compiler handler start a loop.
        """
        Compiler._interpreter.start_for_quad()

    @staticmethod
    def end_for_quad():
        """ Compiler handler end a loop.
        """
        Compiler._interpreter.end_for_quad()
    
    @staticmethod
    def gen_goto_main():
        Compiler._interpreter.gen_goto_main()

    @staticmethod
    def debug_quads():
        """ Compiler handler to debug quads.
        """
        Compiler._interpreter.debug_quads()

    @staticmethod
    def resolve_dimension_access():
        """ Compiler handler resolve the access to a dimensional variable.
        """
        Compiler._interpreter.resolve_dimension_access()

    @staticmethod
    def complete_dimension_access():
        """ Compiler handler complete the access to a dimensional variable.
        """
        Compiler._interpreter.complete_dimension_access()

    @staticmethod
    def allocate_mem_quad(instance, method):
        """ Compiler handler to generate a ERA quad.
        """
        Compiler._interpreter.allocate_mem_quad(instance, method)

    @staticmethod
    def add_method_parameter(method: str, instance: str = None):
        """ Compiler handler to add a parameter to a method call.

            Arguments:
                - method [str]: The method being called.
                - instance [str]: The name of the instance calling the method.
        """
        Compiler._interpreter.add_method_parameter(Compiler.get_method_scope(method, instance))

    @staticmethod
    def complete_method_call(method, instance: str = None):
        """ Compiler handler to complete a method call.

            Arguments:
                - method [str]: The method being called.
                - instance [str]: The name of the instance calling the method.
        """
        Compiler._interpreter.complete_method_call(Compiler.get_method_scope(method, instance), instance)

    @staticmethod
    def check_access_modifier(instance, method):
        method_scope = Compiler.get_method_scope(method, instance)
        if method_scope is not None and method_scope.access_modifier == "private" and instance != "self":
            raise Exception(f"Method {method} is a private method, unable to call it.")


    @staticmethod
    def get_method_scope(method: str, instance: str):
        """ Computes the method scope based on the method name and the instance provided.

            Arguments:
                - method [str]: The method being called.
                - instance [str]: The name of the instance calling the method.

            Returns:
                - [MethodScope]: The method scope associated to the provieded
                    method name and instance.
        """

        if instance == None:
            # Case when method is the constructor
            class_name = method
            method_name = f"constructor_{method}"
        elif "[" in instance:
            variable_name = instance.partition("[")[0]
            class_name = Compiler._current_method.variables_directory.search(variable_name).var_type
            method_name = method
        elif instance == "self":
            class_name = Compiler._current_class.name
            method_name = method
        else:
            # Case for regular methods
            class_name = Compiler._current_method.variables_directory.search(instance).var_type
            method_name = method
        return Compiler._class_directory.search(class_name).method_directory.search(method_name)
