##############################################
# Stack.py
# Purpose: Stack class
# Description: Last in, first out data structure (LIFO)
# ##############################################

class Stack():
    # Constructor
    def __init__(self):
        self.__stack = []

    # Methods
    def push(self, data):
        self.__stack.append(data)

    def pop(self):
        if not self.isEmpty():
            return self.__stack.pop()
        else:
            raise IndexError("Stack is empty. Cannot pop from an empty stack.")

    def peek(self):
        if not self.isEmpty():
            return self.__stack[-1]
        else:
            raise IndexError("Stack is empty. Cannot peek from an empty stack.")

    def isEmpty(self):
        return self.__stack == []

    def size(self):
        return len(self.stack)

    def clear(self):
        self.__stack = []

    def __str__(self):
        fmt = f"Stack: {self.__stack}"
        return fmt
    