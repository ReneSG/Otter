from types import Types
from operations import Operations

class OperationsCube:

    cube = {
            # =============== INT ==========================
            (Types.INT, Types.INT, Operations.ADD): Types.INT,
            (Types.INT, Types.FLOAT, Operations.ADD): Types.FLOAT,
            (Types.INT, Types.BOOL, Operations.ADD): Types.ERROR,
            (Types.INT, Types.STRING, Operations.ADD): Types.ERROR,

            (Types.INT, Types.INT, Operations.DIV): Types.FLOAT,
            (Types.INT, Types.FLOAT, Operations.DIV): Types.FLOAT,
            (Types.INT, Types.BOOL, Operations.DIV): Types.ERROR,
            (Types.INT, Types.STRING, Operations.DIV): Types.ERROR,

            (Types.INT, Types.INT, Operations.PROD): Types.INT,
            (Types.INT, Types.FLOAT, Operations.PROD): Types.FLOAT,
            (Types.INT, Types.BOOL, Operations.PROD): Types.ERROR,
            (Types.INT, Types.STRING, Operations.PROD): Types.ERROR,

            (Types.INT, Types.INT, Operations.SUBS): Types.INT,
            (Types.INT, Types.FLOAT, Operations.SUBS): Types.FLOAT,
            (Types.INT, Types.BOOL, Operations.SUBS): Types.ERROR,
            (Types.INT, Types.STRING, Operations.SUBS): Types.ERROR,

            # =============== FLOAT ==========================
            (Types.FLOAT, Types.INT, Operations.ADD): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.ADD): Types.FLOAT,
            (Types.FLOAT, Types.BOOL, Operations.ADD): Types.ERROR,
            (Types.FLOAT, Types.STRING, Operations.ADD): Types.ERROR,

            (Types.FLOAT, Types.INT, Operations.DIV): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.DIV): Types.FLOAT,
            (Types.FLOAT, Types.BOOL, Operations.DIV): Types.ERROR,
            (Types.FLOAT, Types.STRING, Operations.DIV): Types.ERROR,

            (Types.FLOAT, Types.INT, Operations.PROD): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.PROD): Types.FLOAT,
            (Types.FLOAT, Types.BOOL, Operations.PROD): Types.ERROR,
            (Types.FLOAT, Types.STRING, Operations.PROD): Types.ERROR,

            (Types.FLOAT, Types.INT, Operations.SUBS): Types.FLOAT,
            (Types.FLOAT, Types.FLOAT, Operations.SUBS): Types.FLOAT,
            (Types.FLOAT, Types.BOOL, Operations.SUBS): Types.ERROR,
            (Types.FLOAT, Types.STRING, Operations.SUBS): Types.ERROR,

            # =============== BOOL ==========================
            (Types.BOOL, Types.INT, Operations.ADD): Types.ERROR,
            (Types.BOOL, Types.FLOAT, Operations.ADD): Types.ERROR,
            (Types.BOOL, Types.BOOL, Operations.ADD): Types.ERROR,
            (Types.BOOL, Types.STRING, Operations.ADD): Types.ERROR,

            (Types.BOOL, Types.INT, Operations.DIV): Types.ERROR,
            (Types.BOOL, Types.FLOAT, Operations.DIV): Types.ERROR,
            (Types.BOOL, Types.BOOL, Operations.DIV): Types.ERROR,
            (Types.BOOL, Types.STRING, Operations.DIV): Types.ERROR,

            (Types.BOOL, Types.INT, Operations.PROD): Types.ERROR,
            (Types.BOOL, Types.FLOAT, Operations.PROD): Types.ERROR,
            (Types.BOOL, Types.BOOL, Operations.PROD): Types.ERROR,
            (Types.BOOL, Types.STRING, Operations.PROD): Types.ERROR,

            (Types.BOOL, Types.INT, Operations.SUBS): Types.ERROR,
            (Types.BOOL, Types.FLOAT, Operations.SUBS): Types.ERROR,
            (Types.BOOL, Types.BOOL, Operations.SUBS): Types.ERROR,
            (Types.BOOL, Types.STRING, Operations.SUBS): Types.ERROR,

            # =============== BOOL ==========================
            (Types.STRING, Types.INT, Operations.ADD): Types.ERROR,
            (Types.STRING, Types.FLOAT, Operations.ADD): Types.ERROR,
            (Types.STRING, Types.BOOL, Operations.ADD): Types.ERROR,
            (Types.STRING, Types.STRING, Operations.ADD): Types.ERROR,

            (Types.STRING, Types.INT, Operations.DIV): Types.ERROR,
            (Types.STRING, Types.FLOAT, Operations.DIV): Types.ERROR,
            (Types.STRING, Types.BOOL, Operations.DIV): Types.ERROR,
            (Types.STRING, Types.STRING, Operations.DIV): Types.ERROR,

            (Types.STRING, Types.INT, Operations.PROD): Types.ERROR,
            (Types.STRING, Types.FLOAT, Operations.PROD): Types.ERROR,
            (Types.STRING, Types.BOOL, Operations.PROD): Types.ERROR,
            (Types.STRING, Types.STRING, Operations.PROD): Types.ERROR,

            (Types.STRING, Types.INT, Operations.SUBS): Types.ERROR,
            (Types.STRING, Types.FLOAT, Operations.SUBS): Types.ERROR,
            (Types.STRING, Types.BOOL, Operations.SUBS): Types.ERROR,
            (Types.STRING, Types.STRING, Operations.SUBS): Types.ERROR,
            }

    @staticmethod
    def verify(left_op: Types, right_op: Types, op: Operations) -> Types:
        return OperationsCube.cube.get((left_op, right_op, op), Types.ERROR)
