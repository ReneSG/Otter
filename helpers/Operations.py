from enum import Enum

class Operations(Enum):

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
    LESS = ">"
    LESS_EQUAL_THAN = ">="

    ASSIGN = "="

    @staticmethod
    def is_add_or_sub_op_(op) -> bool:
        return op == Operations.ADD or op == Operations.SUBS

    @staticmethod
    def is_div_or_prod_op_(op) -> bool:
        return op == Operations.DIV or op == Operations.PROD

    @staticmethod
    def is_add_or_sub_op_(op) -> bool:
        return op == Operations.ADD or op == Operations.SUBS
