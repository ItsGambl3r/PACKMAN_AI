class Node():
    # Constructor
    def __init__(self, data):
        self.__data = data 
        self.__next = None

    # Getters and Setters
    def get_data(self):
        return self.__data
    
    def get_next(self):
        return self.__next
    
    def set_data(self, data):
        self.__data = data

    def set_next(self, next_node):
        self.__next = next_node

    # Operator Overloading
    def __str__(self):
        return str(self.__data)