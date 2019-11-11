class Stack:
    def __init__(self):
        self.__elements = []

    def push(self, item):
        self.__elements.append(item)

    def pop(self):
        return self.__elements.pop()

    def isEmpty(self):
        return len(self.__elements) == 0

    def top(self):
        if self.isEmpty():
            return None
        return self.__elements[len(self.__elements) - 1]

    def size(self):
        return len(self.__elements)
