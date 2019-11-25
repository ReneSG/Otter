from enum import Enum

class Operations(Enum):
    """ Operations is an enumerator that defined all the posible operations in the
        Otter programming language.
    """

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
    def is_add_or_sub_op_(op: "Operations") -> bool:
        """ Checks if the operator is an addition or substraction.

            Arguments:
                - op [Operations]: The operation to be checked.

            Returns:
                - [bool]: Whether op is add or subs.
        """
        return op == Operations.ADD or op == Operations.SUBS

    @staticmethod
    def is_div_or_prod_op_(op: "Operations") -> bool:
        """ Checks if the operator is a division or product.

            Arguments:
                - op [Operations]: The operation to be checked.

            Returns:
                - [bool]: Whether op is div or prod.
        """
        return op == Operations.DIV or op == Operations.PROD

    @staticmethod
    def is_rel_op(op: "Operations") -> bool:
        """ Checks if the operator is a relational operation.

            Arguments:
                - op [Operations]: The operation to be checked.

            Returns:
                - [bool]: Whether op is a relational operation.
        """
        return op in [Operations.EQUAL, Operations.GREATER, Operations.GREATER_EQUAL_THAN, Operations.LESS, Operations.LESS_EQUAL_THAN, Operations.NOT_EQUAL]

    @staticmethod
    def is_and_or_op(op: "Operations") -> bool:
        """ Checks if the operator is an and or or.

            Arguments:
                - op [Operations]: The operation to be checked.

            Returns:
                - [bool]: Whether op is an and or or.
        """
        return op == Operations.AND or op == Operations.OR

    @staticmethod
    def is_not_op(op: "Operations") -> bool:
        """ Checks if the operator is a not.

            Arguments:
                - op [Operations]: The operation to be checked.

            Returns:
                - [bool]: Whether op is a not.
        """
        return op == Operations.NOT
