from helpers.operations import Operations
from helpers.types import Types
from helpers.operations_cube import OperationsCube
from helpers.custom_stack import Stack
from scope.variable import Variable
from memory.compilation_memory import CompilationMemory
from scope.method_scope import MethodScope

from typing import List, Optional, Tuple
import logging


logger = logging.getLogger(__name__)


class Interpreter:
    """ The Interpretes is a class responsible for taking action based on the instructions
        from the class that instantiated it (usually the static Compiler class). It is in charge
        of eveyrthing related to generating quads, such as keeping the stack of operands or
        computing the dimensions in  multidimensional variables, among other taks.

        The main parts of the Interpreter are:
         __operands [Stack]: Keeps track of all the operands in an expression.
         __dim_operands [Stack]: Keeps track of all the operands with multiple
            dimensions and the current dimension that is being solved. Tuples with
            the form (Variable, int) will be stored in this Stack.
        __operators [Stack]: Keeps track of the operations in an expression.
        __jumps [Stack]: Keeps track of all the jumps happening when the quads are being
            generated.
        __quads [List[(Operations, Variable, Variable, Optional(Variable))]]: Stores all
            the quads for the program.
        __current_param_index [int]: Keeps track of the parameter index that is being
            supplied in a function call.
    """
    def __init__(self):
        self.__operands = Stack()
        self.__dim_operands = Stack()
        self.__operators = Stack()
        self.__jumps = Stack()
        # DO NOT REMOVE None, its replaced by the initial goto to main.
        self.__quads = [None]
        self.__current_param_index = 0

    @property
    def quads(self):
        return self.__quads

    def push_operator(self, operator: str):
        """Adds an operator to the operators stack.

        Arguments:
            - operators [str]: The operator to be pushed.
        """
        self.__operators.push(Operations(operator))

    def push_constant(self, type_: str, memory_space: int):
        """Adds a constant to the operands stack.

        Arguments:
            - type_ [str]: The type of the constant.
            - memory_space [int]: The memory address for the constant.
        """
        new_variable = Variable(memory_space, type_, memory_space)
        self.__operands.push(new_variable)

    def push_variable(self, current_scope: MethodScope, name: str):
        """Adds a variable to the operands stack.

        Arguments:
            - current_scope [MethodScope]: The scope that is currently active.
            - name [str]: The name of the variable.
        """
        variable = current_scope.variables_directory.search(name)
        if variable == None:
            raise ValueError(f'Variable {name} is not defined in program.')
        if variable.has_multiple_dimensions():
            self.__dim_operands.push((variable, 0))
        else:
            self.__operands.push(variable)

    def assign(self) -> bool:
        """Perform the type check for the two next operands and creates the assign quad.

            Raises:
                - Exception: If the two operands are not type compatible.
        """
        op = self.__operators.pop()
        r_op = self.__operands.pop()
        l_op = self.__operands.pop()
        logger.debug(f"Assigning {r_op} {l_op}")

        result = OperationsCube.verify(r_op.var_type, l_op.var_type, op)
        if r_op.var_type != l_op.var_type and result == Types.ERROR:
            raise ValueError(
                f'Cannot perform {op} operation with {r_op.var_type} {l_op.var_type} operands.')

        self.__quads.append((Operations.ASSIGN, l_op, r_op, l_op.memory_space))

    def check_pending_sum_sub(self) -> bool:
        """ Check if there is a pending sum or substraction operation in the operators stack.
        """
        if not self.__operands.isEmpty() and Operations.is_add_or_sub_op_(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_div_prod(self) -> bool:
        """ Check if there is a pending division or product operation in the operators stack.
        """
        if not self.__operators.isEmpty() and Operations.is_div_or_prod_op_(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_rel_op(self) -> bool:
        """ Check if there is a pending relational operation in the operators stack.
        """
        if not self.__operators.isEmpty() and Operations.is_rel_op(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_and_or(self) -> bool:
        """ Check if there is a pending and or or operation in the operators stack.
        """
        if not self.__operators.isEmpty() and Operations.is_and_or_op(self.__operators.top()):
            self.gen_quad_for_next_op()

    def maybe_gen_not_quad(self) -> bool:
        """ Check if there is a pending not operation in the operators stack.
        """
        if not self.__operators.isEmpty() and Operations.is_not_op(self.__operators.top()):
            op = self.__operators.pop()
            operand = self.__operands.pop()

            memory_address = CompilationMemory.next_temp_memory_space(operand)
            self.__quads.append((op, operand, memory_address))
            self.__operands.push(Variable(memory_address, operand.var_type, memory_address))

    def gen_quad_for_next_op(self) -> bool:
        """ Perform the type check for the two next operands and creates the quads corresponding to
            the next operand.

            Raises:
                - Exception: If the two operands are not type compatible.
        """
        r_op = self.__operands.pop()
        l_op = self.__operands.pop()
        op = self.__operators.pop()

        result = OperationsCube.verify(r_op.var_type, l_op.var_type, op)
        if result == Types.ERROR:
            raise ValueError(
                f'Cannot perform {op} operation with {r_op.var_type} {l_op.var_type} operands.')

        memory_address = CompilationMemory.next_temp_memory_space(result)
        self.__quads.append((op, l_op, r_op, memory_address))
        self.__operands.push(Variable(memory_address, result, memory_address))

    def open_par(self):
        """ Pushes a fake bottom to the operators stack.
        """
        self.__operators.push(Operations.FAKE_BOTTOM)

    def close_par(self):
        """ Removes a fake bottom from the operators stack.
        """
        self.__operators.pop()

    def start_condition_quad(self, is_unless=False):
        """ Creates the GOTOF/GOTOF quad based on the previosly solved condition variable, and leaves the
            jump address as None for now. The actuall jump address will be updated later.

            Arguments:
                - is_unless [bool]: Wether the condition is an unless stament or a regular condition.
        """
        cond_var = self.__operands.pop()
        self.__jumps.push(self.getNextInstructionAddr())
        self.__quads.append(
            (Operations.GOTOT if is_unless else Operations.GOTOF, cond_var, None))

    def end_condition_quad(self):
        """ Takes the top element in the jump stack and completes the previously created
            GOTOF/GOTOT quad.
        """
        condJumpAddr = self.__jumps.pop()
        goToFQuad = self.__quads[condJumpAddr]
        self.__quads[condJumpAddr] = (
            goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def gen_goto_quad(self):
        """ Creates a GOTO quad without a jump address, and calls end_condition_quad to complete a
            previosly created GOTOF quad.
        """
        self.__quads.append((Operations.GOTO, None))
        self.end_condition_quad()
        self.__jumps.push(self.getCurrentInstructionAddr())

    def end_while_quad(self):
        """ Completes the quads previously generated when parsing a loop statement. Adds the
            jump address to the GOTOF quad, and generates a GOTO quad to the start of the 
            loop.
        """
        goToFAddress = self.__jumps.pop()
        goToFQuad = self.__quads[goToFAddress]
        self.gen_goto_quad_to(self.__jumps.pop())
        self.__quads[goToFAddress] = (
            goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def gen_goto_quad_to(self, address: int):
        """ Creates a GOTO quad to the provided jump address.

            Arguments:
                - address: [int]: The jump address for the GOTO.
        """
        self.__quads.append((Operations.GOTO, None, address))

    def push_instruction_address(self):
        """ Pushes the current instruction address to the jump stack.
        """
        self.__jumps.push(self.getCurrentInstructionAddr())

    def push_next_instruction_address(self):
        """ Pushes the next instruction address to the jump stack.
        """
        self.__jumps.push(self.getNextInstructionAddr())

    def getNextInstructionAddr(self):
        """ Computes the next instruction address.

            Returns:
                - [int]: The next instruction address.
        """
        return len(self.__quads)

    def getCurrentInstructionAddr(self):
        """ Computes the current instruction address.

            Returns:
                - [int]: The current instruction address.
        """
        return len(self.__quads) - 1

    def read_quad(self):
        """ Generates a quad for the read operation.
        """
        memory_address = CompilationMemory.next_temp_memory_space(
            Types.STRING)
        temp = Variable(memory_address, Types.STRING, memory_address)
        self.__quads.append((Operations.READ, temp))
        self.__operands.push(temp)

    def write_quad(self):
        """ Generates a quad for the write operation.
        """
        operand = self.__operands.pop()
        self.__quads.append((Operations.WRITE, operand))

    def return_quad(self, method_scope):
        """ Generates a quad for the write operation. Aditionally an assign quad is created
            to store the return value in the global memory address for the function.

            Arguments:
                - method_scope [MethodScope]: The active method scope.
        """
        operand = self.__operands.pop()

        self.__quads.append((Operations.ASSIGN, method_scope.return_memory_address, operand))
        self.__quads.append((Operations.RETURN,))

    def start_for_quad(self):
        """ Creates a GOTOF for the loop statement. Pushing twice the current instruction
            address is needed to complete the GOTOF later on, and to generate the GOTO
            quad to the start of the loop.
        """
        self.start_condition_quad()

    def end_for_quad(self):
        """ [Hacky method to make for work, please be careful when editing]
            Previously two instruction addresses were pushed indicating the start and end
            of the expression to increment iterator, we use these values to know which quads
            have to be moved after the quads for the block statement. This hack is needed
            since the expression for the iterator is parsed before the block, therefore
            its quads end up first on the quad list.

            Aditionally a quad to add to the iterator is created.
        """
        upperBoundBy = self.__jumps.pop()
        lowerBoundBy = self.__jumps.pop()

        for _ in range(lowerBoundBy, upperBoundBy):
            self.__quads.append(self.__quads.pop(lowerBoundBy + 1))

        r_op = self.__operands.pop()
        l_op = self.__operands.pop()

        self.__quads.append((Operations.ADD, l_op, r_op, l_op.memory_space))
        self.gen_goto_quad_to(self.__jumps.pop())
        goToFAddress = lowerBoundBy
        goToFQuad = self.__quads[goToFAddress]
        self.__quads[goToFAddress] = (
            goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def resolve_dimension_access(self):
        """ Creates a quad to verify that the index is within the bounds
            of the dimension variable. Aditionally creates a quad to
            multiply the index by the correct m. After doing all the processing
            pushes back the variable to the dimension variable stack updating
            the index that is being solved.
        """
        dim_tuple = self.__dim_operands.pop()
        dim_variable = dim_tuple[0]
        dimension = dim_variable.getDimensionNumber(dim_tuple[1])

        index = self.__operands.top()
        self.__quads.append((Operations.VER_ACCS, index, 0, dimension.size))

        self.maybe_multiply_for_m(dim_tuple)
        self.__dim_operands.push((dim_tuple[0], dim_tuple[1] + 1))

    def maybe_multiply_for_m(self, dim_tuple: Tuple[Variable, int]):
        """ Generate a quad to multipluy the current index to the corresponding
            dimensional variable.

            Arguments:
                - dim_tuple [Tuple[Variable, int]]: The tuple with the dimension variable.
        """
        variable = dim_tuple[0]

        index = self.__operands.pop()
        memory_address = CompilationMemory.next_temp_memory_space(
            Types.INT)
        new_temp = Variable(memory_address, Types.INT, memory_address)
        self.__quads.append(
                (Operations.PROD_LIT, index, variable.getDimensionNumber(dim_tuple[1]).m, new_temp))
        self.__operands.push(new_temp)

    def complete_dimension_access(self):
        """ Generates the quad to add the base memory of the dimensional address.
        """
        dim_variable, dimension = self.__dim_operands.pop()
        memory_address = CompilationMemory.next_temp_memory_space(
            Types.ARRAY_POINTER)
        var_pointer = Variable(memory_address, Types.ARRAY_POINTER, memory_address)
        var_pointer.pointer_type = dim_variable.var_type

        if dimension > 1:
            index = self.__operands.pop()
            add_memory_address = CompilationMemory.next_temp_memory_space(Types.INT)
            self.__quads.append((Operations.ADD, index, self.__operands.pop(), add_memory_address))
            self.__operands.push(Variable(add_memory_address, Types.INT, add_memory_address))

        var = self.__operands.pop()
        self.__quads.append((Operations.ADD_LIT, var, dim_variable.memory_space, var_pointer))
        self.__operands.push(var_pointer)

    def allocate_mem_quad(self, instance: str, method: str):
        """ Creates a ERA quad.

            Arguments:
                - instance [str]: The instance name of the method to be allocated..
                - method [str]: The method name to be allocated.
        """
        if instance != "constructor" and instance != "self":
            operand = self.__operands.top()
        else:
            operand = instance

        self.__quads.append((Operations.ERA, operand, method))

    def add_method_parameter(self, method_scope: MethodScope):
        """ Creates a quad to assing the variable from the current memory, to the
            memory of the function to be called.

            - method_scope [MethodScope]: The method scope from the function
                that is being called.
        """
        if len(method_scope.ordered_arguments) <= self.__current_param_index:
            raise Exception(f"{method_scope.name} only takes {len(method_scope.ordered_arguments)} parameters")

        to_variable = method_scope.ordered_arguments[self.__current_param_index]

        if to_variable.has_multiple_dimensions():
            operand, _ = self.__dim_operands.pop()
        else:
            operand = self.__operands.pop()

        self.__quads.append((Operations.PARAM, operand, to_variable))
        self.__current_param_index += 1

    def complete_method_call(self, method_scope: MethodScope, instance: str):
        """ Creates a GOSUB quad to the instruction address of the method to be
            called. Aditionally if the method has a return type generates quads
            to take the return value of the method from the global memory and
            store it in a temporal. Finally set the __current_param_index to
            0 since by this point we are done assigning the parameters of
            the method.

            Arguments:
                - method_scope [MethodScope]: The method scope of the function
                    to be called.
                - instance [str]: The name of the instance of the method to be called.
        """
        # Handle weird case when the instance is detected as an operand.
        if instance != None and instance != "self":
            self.__operands.pop()
        self.__quads.append((Operations.GOSUB, method_scope.name, method_scope.instruction_pointer))

        if method_scope.return_type != "void":
            next_address = CompilationMemory.next_temp_memory_space(method_scope.return_type)
            temp = Variable(next_address, method_scope.return_type, next_address)
            self.__quads.append((Operations.ASSIGN, temp, method_scope.return_memory_address))
            self.__operands.push(temp)

        if len(method_scope.ordered_arguments) != self.__current_param_index:
            raise Exception(f"Number of parameters do not match on {method_scope.name}")
        self.__current_param_index = 0

    def add_end_function_quad(self, method_scope: MethodScope):
        """ Creates a quad to indicate the end of a function.
        """
        if method_scope.return_type == "void":
            self.__quads.append((Operations.RETURN,))

        self.__quads.append((Operations.END_FUNC,))

    def add_end_constructor_quad(self, method_scope: MethodScope):
        self.__quads.append((Operations.RETURN, "constructor", method_scope.return_memory_address))

    def gen_start_quad(self):
        """ Generates the GOTO quad to the main function and stores in the
            first element of the quad list.
        """
        self.__quads[0] = (Operations.GOTO, None, self.getNextInstructionAddr())

    def allocate_memory_for_array(self, variable: Variable):
        """ Allocates the memory chunk for a dimensional variable.

            Arguments:
                - variable [Variable]: The dimensional variable to be allocated.
        """
        CompilationMemory.next_memory_chunk(variable.var_type, variable.size)

    def get_quads(self):
        """ Returns the quad list.

            Returns:
                - list [Tuple[Operations, Variable, Variable, int]]: The quad list
        """
        return self.__quads

    def debug_quads(self):
        """ Prints the quads in a pretty way.
        """
        logger.debug("===========================================QUADS===========================================")
        for i in range(0, len(self.__quads)):
            logger.debug(f"{i}, {self.__quads[i]}")
