from helpers.operations import Operations
from helpers.types import Types
from helpers.operations_cube import OperationsCube
from helpers.custom_stack import Stack
from scope.variable import Variable
from memory.compilation_memory import CompilationMemory
import logging


logger = logging.getLogger(__name__)


class Interpreter:
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

    def push_operator(self, operator):
        self.__operators.push(Operations(operator))

    def push_constant(self, type_, memory_space):
        new_variable = Variable(memory_space, type_, memory_space)
        self.__operands.push(new_variable)

    def push_variable(self, current_scope, name):
        variable = current_scope.variables_directory.search(name)
        if variable == None:
            raise ValueError(f'Variable {name} is not defined in program.')
        if variable.has_multiple_dimensions():
            self.__dim_operands.push((variable, 0))
        else:
            self.__operands.push(variable)

    def assign(self) -> bool:
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
        if not self.__operands.isEmpty() and Operations.is_add_or_sub_op_(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_div_prod(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_div_or_prod_op_(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_rel_op(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_rel_op(self.__operators.top()):
            self.gen_quad_for_next_op()

    def check_pending_and_or(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_and_or_op(self.__operators.top()):
            self.gen_quad_for_next_op()

    def maybe_gen_not_quad(self) -> bool:
        if not self.__operators.isEmpty() and Operations.is_not_op(self.__operators.top()):
            op = self.__operators.pop()
            operand = self.__operands.pop()

            memory_address = CompilationMemory.next_temp_memory_space(operand)
            self.__quads.append((op, operand, memory_address))
            self.__operands.push(Variable(memory_address, operand.var_type, memory_address))

    def gen_quad_for_next_op(self) -> bool:
        r_op = self.__operands.pop()
        l_op = self.__operands.pop()
        op = self.__operators.pop()

        # TODO: Add type to variables.
        result = OperationsCube.verify(r_op.var_type, l_op.var_type, op)
        if result == Types.ERROR:
            raise ValueError(
                f'Cannot perform {op} operation with {r_op.var_type} {l_op.var_type} operands.')

        memory_address = CompilationMemory.next_temp_memory_space(result)
        self.__quads.append((op, l_op, r_op, memory_address))
        self.__operands.push(Variable(memory_address, result, memory_address))

    def open_par(self):
        self.__operators.push(Operations.FAKE_BOTTOM)

    def close_par(self):
        self.__operators.pop()

    def start_condition_quad(self, isUnless=False):
        # TODO: Get last temporal.
        condVar = self.__operands.pop()
        self.__jumps.push(self.getNextInstructionAddr())
        self.__quads.append(
            (Operations.GOTOT if isUnless else Operations.GOTOF, condVar, None))

    def end_condition_quad(self):
        condJumpAddr = self.__jumps.pop()
        goToFQuad = self.__quads[condJumpAddr]
        self.__quads[condJumpAddr] = (
            goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def gen_goto_quad(self):
        self.__quads.append((Operations.GOTO, None))
        self.end_condition_quad()
        self.__jumps.push(self.getCurrentInstructionAddr())

    def end_while_quad(self):
        goToFAddress = self.__jumps.pop()
        goToFQuad = self.__quads[goToFAddress]
        self.gen_goto_quad_to(self.__jumps.pop())
        self.__quads[goToFAddress] = (
            goToFQuad[0], goToFQuad[1], self.getNextInstructionAddr())

    def gen_goto_quad_to(self, address):
        self.__quads.append((Operations.GOTO, None, address))

    def push_instruction_address(self):
        self.__jumps.push(self.getCurrentInstructionAddr())

    def push_next_instruction_address(self):
        self.__jumps.push(self.getNextInstructionAddr())

    def getNextInstructionAddr(self):
        return len(self.__quads)

    def getCurrentInstructionAddr(self):
        return len(self.__quads) - 1

    def read_quad(self):
        memory_address = CompilationMemory.next_temp_memory_space(
            Types.STRING)
        self.__quads.append((Operations.READ, Variable(
            memory_address, Types.STRING, memory_address)))

    def write_quad(self):
        operand = self.__operands.pop()
        self.__quads.append((Operations.WRITE, operand))

    def return_quad(self, method_scope):
        operand = self.__operands.pop()

        self.__quads.append((Operations.ASSIGN, method_scope.return_memory_address, operand))
        self.__quads.append((Operations.RETURN,))

    def start_for_quad(self):
        self.push_instruction_address()
        self.start_condition_quad()

    def end_for_quad(self):
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
        dim_tuple = self.__dim_operands.pop()
        dim_variable = dim_tuple[0]
        dimension = dim_variable.getDimensionNumber(dim_tuple[1])

        index = self.__operands.top()
        self.__quads.append((Operations.VER_ACCS, index, 0, dimension.size))

        self.maybe_multiply_for_m(dim_tuple)
        self.__dim_operands.push((dim_tuple[0], dim_tuple[1] + 1))

    def maybe_multiply_for_m(self, dim_tuple):
        # Only compute mn*sn for second and higher dimensions.
        variable = dim_tuple[0]

        index = self.__operands.pop()
        memory_address = CompilationMemory.next_temp_memory_space(
            Types.INT)
        new_temp = Variable(memory_address, Types.INT, memory_address)
        self.__quads.append(
                (Operations.PROD_LIT, index, variable.getDimensionNumber(dim_tuple[1]).m, new_temp))
        self.__operands.push(new_temp)

    def complete_dimension_access(self):
        dim_variable = self.__dim_operands.pop()[0]
        index = self.__operands.pop()
        memory_address = CompilationMemory.next_temp_memory_space(
            Types.ARRAY_POINTER)
        var_pointer = Variable(memory_address, Types.ARRAY_POINTER, memory_address)
        self.__quads.append((Operations.ADD_LIT, index, dim_variable.memory_space, var_pointer))
        self.__operands.push(var_pointer)

    def allocate_mem_quad(self, instance, method):
        self.__quads.append((Operations.ERA, instance, method))

    def add_method_parameter(self, method_scope):
        # TODO: Get param address once memory is implemented.
        print(method_scope.name)
        print(method_scope.ordered_arguments)
        to_variable = method_scope.ordered_arguments[self.__current_param_index]
        self.__quads.append((Operations.PARAM, self.__operands.pop(), to_variable))
        self.__current_param_index += 1

    def complete_method_call(self, method_scope, instance):
        # Handle weird case when the instance is detected as an operand.
        if instance != None and instance != "self":
            self.__operands.pop()
        self.__quads.append((Operations.GOSUB, method_scope.name, method_scope.instruction_pointer))

        if method_scope.return_type != "void":
            next_address = CompilationMemory.next_temp_memory_space(method_scope.return_type)
            temp = Variable(next_address, method_scope.return_type, next_address)
            self.__quads.append((Operations.ASSIGN, temp, method_scope.return_memory_address))
            self.__operands.push(temp)
        self.__current_param_index = 0

    def add_end_function_quad(self):
        self.__quads.append((Operations.END_FUNC,))

    def get_lower_bound(self, dim_variable):
        # We are indexing always from 0, C-like style.
        return 0

    def gen_start_quad(self):
        self.__quads[0] = (Operations.GOTO, None, self.getNextInstructionAddr())

    def allocate_memory_for_array(self, variable):
        CompilationMemory.next_memory_chunk(variable.var_type, variable.size)

    def get_quads(self):
        return self.__quads

    def debug_quads(self):
        logger.debug("===========================================QUADS===========================================")
        for i in range(0, len(self.__quads)):
            logger.debug(f"{i}, {self.__quads[i]}")
