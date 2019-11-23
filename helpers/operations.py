from enum import Enum

class Operations(Enum):

    FAKE_BOTTOM = "("

    # Arithmethic
    ADD = "+"
    SUBS = "-"
    PROD = "*"
    DIV = "/"

    # Relational
    AND = "and"
    OR = "or"
    EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL_THAN = ">="
    LESS = "<"
    LESS_EQUAL_THAN = "<="
    NOT_EQUAL = "!="

    ASSIGN = "="
    NOT = "not"
    GOTOF = "GOTOF"
    GOTOT = "GOTOT"
    GOTO = "GOTO"
    READ = "READ"
    WRITE = "WRITE"
    RETURN = "RETURN"
    VER_ACCS = "VER_ACCS"
    ERA = "ERA"
    PARAM = "PARAM"
    GOSUB = "GOSUB"
    END_FUNC = "END_FUNC"
    PROD_LIT = "PROD_LIT"
    ADD_LIT = "ADD_LIT"

    @staticmethod
    def is_add_or_sub_op_(op) -> bool:
        return op == Operations.ADD or op == Operations.SUBS

    @staticmethod
    def is_div_or_prod_op_(op) -> bool:
        return op == Operations.DIV or op == Operations.PROD

    @staticmethod
    def is_rel_op(op) -> bool:
        return op in [Operations.EQUAL, Operations.GREATER, Operations.GREATER_EQUAL_THAN, Operations.LESS, Operations.LESS_EQUAL_THAN, Operations.NOT_EQUAL]

    @staticmethod
    def is_and_or_op(op) -> bool:
        return op == Operations.AND or op == Operations.OR

    @staticmethod
    def is_not_op(op) -> bool:
        return op == Operations.NOT
