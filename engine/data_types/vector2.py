from __future__ import annotations
from dataclasses import dataclass


class Meta(type):
    
    def __new__(cls, name, bases, dct):
        
        instance = super().__new__(cls, name, bases, dct)
        return instance
    
    
    @property
    def ONE(self):
        
        return Vector2(1, 1)
    
    
    @property
    def ZERO(self):
        
        return Vector2(0, 0)
    
    
    @property
    def UP(self):
        
        return Vector2(0, -1)
    
    
    @property
    def DOWN(self):
        
        return Vector2(0, 1)
    
    
    @property
    def LEFT(self):
        
        return Vector2(-1, 0)
    
    
    @property
    def RIGHT(self):
        
        return Vector2(1, 0)
    
    
    @property
    def UPLEFT(self):
        
        return Vector2(-1, -1)
    
    
    @property
    def UPRIGHT(self):
        
        return Vector2(1, -1)
    
    
    @property
    def DOWNLEFT(self):
        
        return Vector2(-1, 1)
    
    
    @property
    def DOWNRIGHT(self):
        
        return Vector2(1, 1)


@dataclass
class Vector2(metaclass=Meta):
    
    x: int = 0
    y: int = 0
    
    
    def __init__(self, x: int | Vector2 | list[int, int] = 0, y: int = 0):
        
        if isinstance(x, Vector2):
            self.x = x.x
            self.y = x.y
        elif isinstance(x, list):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y
    
    
    def __repr__(self):
        
        return f"({self.x}, {self.y})"
    
    
    def __add__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"{self.__class__.__name__} __add__ {other.__class__.__name__}")
        
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x, y)
    
    
    def __sub__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"{self.__class__.__name__} __sub__ {other.__class__.__name__}")
        
        x = self.x - other.x
        y = self.y - other.y
        return Vector2(x, y)
    
    
    def __mul__(self, other):
        
        if isinstance(other, self.__class__):
            x = self.x * other.x
            y = self.y * other.y
        elif isinstance(other, int):
            x = self.x * other
            y = self.y * other
        else:
            raise NotImplementedError(f"{self.__class__.__name__} __mul__ {other.__class__.__name__}")
        
        return Vector2(x, y)
    
    
    def __rmul__(self, other):
        
        return self * other
    
    
    def __mod__(self, other):
        
        if isinstance(other, self.__class__):
            if other.x == 0:
                x = 0
            else:
                x = self.x % other.x
            if other.y == 0:
                y = self.y % other.y
            else:
                y = 0
        elif isinstance(other, int):
            if other.x == 0:
                x = 0
            else:
                x = self.x % other
            if other.y == 0:
                y = self.y % other
            else:
                y = 0
        else:
            raise NotImplementedError(f"{self.__class__.__name__} __mod__ {other.__class__.__name__}")
        
        return Vector2(x, y)
    
    
    def __rmod__(self, other):
        
        return self % other
    
    
    def __eq__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"{self.__class__.__name__} __eq__ {other.__class__.__name__}")
        
        return self.x == other.x and self.y == other.y    
    
    
    def __ne__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"{self.__class__.__name__} __ne__ {other.__class__.__name__}")
        
        return self.x != other.x or self.y != other.y    
    
    
    """
    def __gt__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplemented
        
        return self.x > other.x or self.y > other.y
    
    
    def __ge__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplemented
    
    
    def __lt__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplemented
    
    
    def __le__(self, other):
        
        if not isinstance(other, self.__class__):
            raise NotImplemented
    """




