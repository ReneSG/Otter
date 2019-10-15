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
