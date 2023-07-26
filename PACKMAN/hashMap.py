from linkedList import LinkedList

def hash(key, size):
    if isinstance(key, str):
        index = string_hash(key, size)
    elif isinstance(key, int):
        index = int_hash(key, size)
    else:
        raise TypeError("Key must be a string or an integer.")
    return index

def string_hash(key: str, size: int) -> int:
    total = 0
    for char in key:
        total += ord(char)
    return int_hash(total, size)

def int_hash(key: int, size: int) -> int:
    A = 0.618033988749895  # The golden ratio (a common choice for A)
    scaled = key * A
    fractional_part = scaled - int(scaled)  # Extract the fractional part
    hash_value = int(size * fractional_part)
    return hash_value

class HashMap():
    def __init__(self, size):
        self.__size = size
        self.__map = [LinkedList() for i in range(size)]

    def put(self, key, value):
        index = hash(key, self.__size)
        self.__map[index].append((key, value))

    def get(self, key):
        index = hash(key, self.__size)
        if self.__map[index].isEmpty():
            return None
        else:
            current = self.__map[index].get_head()
            while current != None:
                if current.get_data()[0] == key:
                    return current.get_data()[1]
                current = current.get_next()
            return None

    #TODO: Implement remove method
    def remove(self, key):
        index = hash(key, self.__size)
        self.__map[index].delete_node(key)

    def contains(self, key):
        index = hash(key, self.__size)
        if self.__map[index].isEmpty():
            return False
        else:
            current = self.__map[index].get_head()
            while current != None:
                if current.get_data()[0] == key:
                    return True
                current = current.get_next()
            return False
    
    def clear(self):
        self.__map = [LinkedList() for i in range(self.__size)]

    # Operator Overloading
    def __str__(self):
        fmt = ""
        for i in range(self.__size):
            fmt += f"{i}: {self.__map[i]}\n"
        return fmt
    
    def __getitem__(self, key):
        return self.get(key)