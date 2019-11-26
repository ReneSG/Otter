from .types import Types
from .operations import Operations

class OperationsCube:
    """ The OperationsCube is a static class that defines all the valid operations
        in the Otter language.
    """

    cube = {
            # =============== INT ==========================
            (Types.INT, Types.INT, Operations.ASSIGN): Types.INT,

            (Types.INT, Types.INT, Operations.NOT_EQUAL): Types.BOOL,

            (Types.INT, Types.INT, Operations.ADD): Types.INT,
            (Types.INT, Types.FLOAT, Operations.ADD): Types.FLOAT,

            (Types.INT, Types.INT, Operations.DIV): Types.FLOAT,
            (Types.INT, Types.FLOAT, Operations.DIV): Types.FLOAT,

            (Types.INT, Types.INT, Operations.PROD): Types.INT,
            (Types.INT, Types.FLOAT, Operations.PROD): Types.FLOAT,

            (Types.INT, Types.INT, Operations.SUBS): Types.INT,
            (Types.INT, Types.FLOAT, Operations.SUBS): Types.FLOAT,

            (Types.INT, Types.INT, Operations.EQUAL): Types.BOOL,
            (Types.INT, Types.FLOAT, Operations.EQUAL): Types.BOOL,

            (Types.INT, Types.INT, Operations.GREATER): Types.BOOL,
            (Types.INT, Types.FLOAT, Operations.GREATER): Types.BOOL,

            (Types.INT, Types.INT, Operations.GREATER_EQUAL_THAN): Types.BOOL,
            (Types.INT, Types.FLOAT, Operations.GREATER_EQUAL_THAN): Types.BOOL,

            (Types.INT, Types.INT, Operations.LESS): Types.BOOL,
            (Types.INT, Types.FLOAT, Operations.LESS): Types.BOOL,

            (Types.INT, Types.INT, Operations.LESS_EQUAL_THAN): Types.BOOL,
            (Types.INT, Types.FLOAT, Operations.LESS_EQUAL_THAN): Types.BOOL,

            # =============== FLOAT ==========================
            (Types.FLOAT, Types.FLOAT, Operations.ASSIGN): Types.FLOAT,

            (Types.FLOAT, Types.FLOAT, Operations.NOT_EQUAL): Types.BOOL,

            (Types.FLOAT, Types.INT, Operations.ADD): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.ADD): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.DIV): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.DIV): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.PROD): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.PROD): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.SUBS): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.SUBS): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.EQUAL): Types.BOOL,
            (Types.FLOAT, Types.FLOAT, Operations.EQUAL): Types.BOOL,

            (Types.FLOAT, Types.INT, Operations.GREATER): Types.BOOL,
            (Types.FLOAT, Types.FLOAT, Operations.GREATER): Types.BOOL,

            (Types.FLOAT, Types.INT, Operations.GREATER_EQUAL_THAN): Types.BOOL,
            (Types.FLOAT, Types.FLOAT, Operations.GREATER_EQUAL_THAN): Types.BOOL,

            (Types.FLOAT, Types.INT, Operations.LESS): Types.BOOL,
            (Types.FLOAT, Types.FLOAT, Operations.LESS): Types.BOOL,

            (Types.FLOAT, Types.INT, Operations.LESS_EQUAL_THAN): Types.BOOL,
            (Types.FLOAT, Types.FLOAT, Operations.LESS_EQUAL_THAN): Types.BOOL,

            # =============== BOOL ==========================
            (Types.BOOL, Types.BOOL, Operations.ASSIGN): Types.BOOL,
            (Types.BOOL, Types.BOOL, Operations.NOT_EQUAL): Types.BOOL,
            (Types.BOOL, Types.BOOL, Operations.AND): Types.BOOL,
            (Types.BOOL, Types.BOOL, Operations.OR): Types.BOOL,
            (Types.BOOL, Types.BOOL, Operations.EQUAL): Types.BOOL,
            (Types.BOOL, None, Operations.NOT): Types.BOOL,
            (None, Types.BOOL, Operations.NOT): Types.BOOL,

            # =============== STRING ==========================
            (Types.STRING, Types.STRING, Operations.ASSIGN): Types.STRING,
            (Types.STRING, Types.STRING, Operations.NOT_EQUAL): Types.BOOL,
            (Types.STRING, Types.STRING, Operations.EQUAL): Types.BOOL,
            }

    @staticmethod
    def verify(left_op: Types, right_op: Types, op: Operations) -> Types:
        """ Verifies that the provided operators are type valid for the provided operation.

            Arguments:
                - left_op [Types]: The type of the left operator.
                - right_op [Types]: The type of the right operator.
                - op [Operations]: The operation to be performed.

            Returns:
                - [Types]: The result type of the operation or Types.ERROR if it is not valid.
        """
        return OperationsCube.cube.get((left_op, right_op, op), Types.ERROR)
