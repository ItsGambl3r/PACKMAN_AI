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
    
class LinkedList():
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    # Getters and Setters
    def get_head(self):
        return self.__head
    
    def get_tail(self):
        return self.__tail
    
    def get_size(self):
        return self.__size
    
    def set_head(self, head):
        self.__head = head

    def set_tail(self, tail):
        self.__tail = tail

    def set_size(self, size):
        self.__size = size

    # Methods
    def isEmpty(self):
        return self.__head == None
    
    def append(self, data):
        # Adds a node to the end of the linked list
        node = Node(data)
        if self.__head == None:
            self.__head = node
            self.__tail = node
        else:
            self.__tail.set_next(node)
            self.__tail = node

    def prepend(self, data):
        # Adds a node to the beginning of the linked list
        node = Node(data)
        if self.__head == None:
            self.__head = node
            self.__tail = node
        else:
            node.set_next(self.__head)
            self.__head = node

    def find_node(self, data):
        current = self.__head
        while current is not None:
            if current.get_data() == data:
                return current
            current = current.get_next()
        return None

    # Operator Overloading
    def __len__(self):
        return self.__size
    
    def __str__(self):
        if self.isEmpty():
            return "Empty"

        fmt = ""
        current_node = self.__head

        while current_node is not None:
            fmt += str(current_node.get_data())
            if current_node.get_next() is not None:  # If the current node is not the last node
                fmt += " -> "
            current_node = current_node.get_next()

        return fmt
