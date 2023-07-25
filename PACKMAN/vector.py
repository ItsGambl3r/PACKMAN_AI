import math

class DivideByZeroError(Exception):
    def __init__(self, message = "Cannot divide by zero"):
        super().__init__(message) # calls the parent class constructor

class Vector2(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__threshold = 0.000001

    # Getters and Setters
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    # Methods
    def magnitude(self):
        # Returns the magnitude of the vector
        # sqrt(x^2 + y^2)
        return math.sqrt(self.__x ** 2 + self.__y ** 2)
    
    def copy(self):
        # Returns a copy of the vector
        return Vector2(self.__x, self.__y)
    
    def asTuple(self):
        # Returns a tuple representation containing the exact `x` and `y components
        return (self.__x, self.__y)
    
    def asInt(self):
        # Returns a tuple contaning the integer representation of `x` and `y components
        return Vector2(int(self.__x), int(self.__y))

    # Operator Overloading
    def __str__(self):
        fmt = f"<{self.__x}, {self.__y}>"
        return fmt
    
    def __add__(self, other):
        # Adding vector components together
        if isinstance(other, Vector2):
            new_x = self.__x + other.get_x()
            new_y = self.__y + other.get_y()
            return Vector2(new_x, new_y) 
        else:
            raise TypeError("Cannot add Vector2 and + " + str(type(other)))
        
    def __sub__(self, other):
        # Subtracting vector components
        if isinstance(self, Vector2):
            new_x = self.__x - other.get_x()
            new_y = self.__y - other.get_y()
            return Vector2(new_x, new_y)
        else:
            raise TypeError("Cannot add Vector2 and + " + str(type(other)))
        
    def __neg__(self):
        # Negating vector components
        new_x = -self.__x
        new_y = -self.__y
        return Vector2(new_x, new_y)
    
    def __mul__(self, scalar):
        # Multiplying vector components by a scalar
        if isinstance(scalar, (int, float)):
            new_x = self.__x * scalar
            new_y = self.__y * scalar
            return Vector2(new_x, new_y)
        else:
            raise TypeError("Cannot multiply Vector2 and " + str(type(scalar)))
        
    def __truediv__(self, scalar):
        # Dividing vector components by a scalar
        if scalar == 0:
            raise DivideByZeroError()
        elif isinstance(scalar, (int, float)):
            new_x = self.__x / scalar
            new_y = self.__y / scalar
            return Vector2(new_x, new_y)
        else:
            raise TypeError("Cannot divide Vector2 and " + str(type(scalar)))
        
    def __floordiv__(self, scalar):
        # Dividing vector components by a scalar
        if scalar == 0:
            raise DivideByZeroError()
        elif isinstance(scalar, (int, float)):
            new_x = self.__x // scalar
            new_y = self.__y // scalar
            return Vector2(new_x, new_y)
        else:
            raise TypeError("Cannot divide Vector2 and " + str(type(scalar)))
        
    def __eq__(self, other):
        # Comparing vector components
        if isinstance(other, Vector2):
            x_equal = abs(self.__x - other.get_x()) < self.__threshold
            y_equal = abs(self.__y - other.get_y()) < self.__threshold
            return x_equal and y_equal
        else:
            raise TypeError("Cannot compare Vector2 and " + str(type(other)))
        
    def __ne__(self, other):
        return not self.__eq__(other)

if __name__ == "__main__":
    Vector_1 = Vector2(1, 2)
    Vector_2 = Vector2(2, 3)
    print(Vector_1 + Vector_2)

