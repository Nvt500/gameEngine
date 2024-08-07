from itertools import cycle
from engine.data_types.vector2 import Vector2


class Path:
    
    def __init__(self, start: Vector2, end: Vector2, *midpoints: Vector2, step: int = 1):
        
        """
        This should only be used for vertical, horizontal, or perfectly diagonal lines (y=x).
        start: start of path
        end: end of path
        step: how many units to move for each call of move()
        *midpoints: points between start and end
        """
        
        self.index = 0
        self.start = start
        self.end = end
        
        self.step = step
        self.change = None
        
        self.points = [start]
        if midpoints:
            self.points.extend(midpoints)
        self.points.append(end)
                            
        self.rect = None
        
    
    def find_change(self, point1: Vector2, point2: Vector2) -> None:
        
        self.change = Vector2.ZERO
        
        if point1.x < point2.x:
            self.change.x = 1
        elif point1.x == point2.x:
            self.change.x = 0
        else:
            self.change.x = -1
        if point1.y < point2.y:
            self.change.y = 1
        elif point1.y == point2.y:
            self.change.y = 0
        else:
            self.change.y = -1
        
        self.change *= self.step
    
    
    def move(self) -> None:
        
        """Changes position of Rect along the path."""
        
        # Don't know why but importing not working so this will do.
        if not self.rect and self.rect.__class__.__name__ == "Rect":
            return
            
        #"""
        if self.rect.position == self.points[self.index + 1]:
            self.index += 1
            if self.index == len(self.points) - 1:
                self.index = 0
                self.points = self.points[::-1]
            self.find_change(self.points[self.index], self.points[self.index + 1])
        #"""
        
        """
        if self.rect.position == self.points[-1]:
            self.find_change(self.points[-1], self.points[0]) 
        if self.rect.position == self.points[0]:
            self.find_change(self.points[0], self.points[-1]) 
        """
        
        if not self.change:
            self.find_change(self.points[self.index], self.points[self.index + 1])
        
        self.rect.change_position(self.change)

