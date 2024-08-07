from typing import Any, TypedDict
from engine.data_types.object import Object
from engine.screen.colors import Colors

class Debug(Object):
    
    def __init__(self, text: str = "", color: TypedDict("color", {"color": Colors, "background_color": Colors}) = {}):
        
        self.text = text
        self.color = color
        self.color.setdefault("color", Colors.WHITE)
        self.color.setdefault("background_color", Colors.BLACK)

        
    def print(self, text: Any):
        
        self.text = str(text)