from .types import Types
from .operations import Operations

class OperationsCube:

    cube = {
            # =============== INT ==========================
            (Types.INT, Types.INT, Operations.ASSIGN): Types.INT,

            (Types.INT, Types.INT, Operations.ADD): Types.INT,
            (Types.INT, Types.FLOAT, Operations.ADD): Types.FLOAT,

            (Types.INT, Types.INT, Operations.DIV): Types.FLOAT,
            (Types.INT, Types.FLOAT, Operations.DIV): Types.FLOAT,

            (Types.INT, Types.INT, Operations.PROD): Types.INT,
            (Types.INT, Types.FLOAT, Operations.PROD): Types.FLOAT,

            (Types.INT, Types.INT, Operations.SUBS): Types.INT,
            (Types.INT, Types.FLOAT, Operations.SUBS): Types.FLOAT,

            # =============== FLOAT ==========================
            (Types.FLOAT, Types.FLOAT, Operations.ASSIGN): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.ADD): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.ADD): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.DIV): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.DIV): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.PROD): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.PROD): Types.FLOAT,

            (Types.FLOAT, Types.INT, Operations.SUBS): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.SUBS): Types.FLOAT,

            # =============== BOOL ==========================
            (Types.BOOL, Types.BOOL, Operations.ASSIGN): Types.BOOL,

            # =============== STRING ==========================
            (Types.STRING, Types.STRING, Operations.ASSIGN): Types.STRING,
            }

    @staticmethod
    def verify(left_op: Types, right_op: Types, op: Operations) -> Types:
        return OperationsCube.cube.get((left_op, right_op, op), Types.ERROR)
