from typing import Any, List

class Stack:
    """ Simple implementatin of a stack.
    """
    def __init__(self):
        self.__elements = []

    def push(self, item: Any):
        """ Pushes an item to the stack.

            Arguments:
                - item [Any]: The element to be pushed to the stack.
        """
        self.__elements.append(item)

    def pop(self) -> Any:
        """ Returns the top element in the stack and removes it from the stack.

            Returns:
                - [Any]: The top element of the stack.
        """
        return self.__elements.pop()

    def isEmpty(self) -> bool:
        """ Wether the stack is empty or not.

            Returns:
                - [bool]: Indicates if the stack is empty.
        """
        return len(self.__elements) == 0

    def top(self) -> Any:
        """ Returns the top element in the stack or None if the stack is empty.

            Returns:
                - [Any]: The top element of the stack.
        """
        if self.isEmpty():
            return None
        return self.__elements[len(self.__elements) - 1]

    def size(self) -> int:
        """ Returns the size of the stack.

            Returns:
                - [int]: The size of the stack.
        """
        return len(self.__elements)

    @property
    def elements(self) -> List[Any]:
        """ Returns all the elements in the stack as a list.

            Returns:
                - [List[Any]]: Elements in the stack a list.
        """
        return self.__elements
