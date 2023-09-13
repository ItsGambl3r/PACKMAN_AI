# Import necessary modules and classes
import math
from typing import List, Tuple

class Vector2D(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.thresh = 1e-6

    def as_tuple(self) -> Tuple[float, float]:
        '''Returns a tuple representation of the vector'''
        return (self.x, self.y)

    def magnitude_squared(self) -> float:
        '''Returns the magnitude squared of the vector'''
        return self.x ** 2 + self.y ** 2

    def magnitude(self) -> float:
        '''Returns the magnitude of the vector'''
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def distance(self, other: 'Vector2D') -> float:
        '''Returns the distance between this vector and another vector'''
        if isinstance(other, Vector2D):
            return (self - other).magnitude()
        raise TypeError(f'Cannot get distance between Vector2D and {type(other)}')
    
    def dot(self, other: 'Vector2D') -> float:
        '''Returns the dot product of this vector and another vector'''
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y
        raise TypeError(f'Cannot dot Vector2D and {type(other)}')
    
    def copy(self) -> 'Vector2D':
        '''Returns a copy of this vector'''
        return Vector2D(self.x, self.y)

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        raise TypeError(f'Cannot add Vector2D and {type(other)}')
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        raise TypeError(f'Cannot subtract Vector2D and {type(other)}')
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise TypeError(f'Cannot multiply Vector2D and {type(scalar)}') 
    
    def __truediv__(self, scalar: float) -> 'Vector2D':
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x / scalar, self.y / scalar)
        raise TypeError(f'Cannot divide Vector2D and {type(scalar)}')
    
    def __neg__(self) -> 'Vector2D':
        return Vector2D(-self.x, -self.y)
    
    def __eq__(self, other: 'Vector2D') -> bool:
        if isinstance(other, Vector2D):
            return abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh
        return False
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'
    
    def __repr__(self) -> str:
        return self.__str__()