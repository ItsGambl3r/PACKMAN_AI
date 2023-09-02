import math

class Vector2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.thresh = 1e-6

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        raise TypeError(f'Cannot add Vector2D and {type(other)}')
    
    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        raise TypeError(f'Cannot subtract Vector2D and {type(other)}')
    
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise TypeError(f'Cannot multiply Vector2D and {type(scalar)}')
    
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ZeroDivisionError('Cannot divide by zero')
            return Vector2D(self.x / scalar, self.y / scalar)
        raise TypeError(f'Cannot divide Vector2D and {type(scalar)}')
    
    def __floordiv__(self, scalar):
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ZeroDivisionError('Cannot divide by zero')
            return Vector2D(self.x // scalar, self.y // scalar)
        raise TypeError(f'Cannot divide Vector2D and {type(scalar)}')
    
    def __neg__(self):
        return Vector2D(-self.x, -self.y)
    
    def __eq__(self, other):
        if isinstance(other, Vector2D):
            return abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh
        
    def magnitudeSquared(self):
        return self.x**2 + self.y**2
    
    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())
    
    def distance(self, other):
        if isinstance(other, Vector2D):
            return (self - other).magnitude()
        raise TypeError(f'Cannot calculate distance between Vector2D and {type(other)}')
    
    def dot(self, other):
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y
        raise TypeError(f'Cannot calculate dot product between Vector2D and {type(other)}')
    
    def copy(self):
        return Vector2D(self.x, self.y)
    
    def asTuple(self):
        return (self.x, self.y)
    
    def __str__(self):
        return f'<{self.x}, {self.y}>'
    
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    node_a = Vector2D(16, 64)
    node_b = Vector2D(96, 64)
    distance = node_a.distance(node_b)
    print(distance)