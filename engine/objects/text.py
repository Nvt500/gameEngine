from typing import Any, TypedDict
from itertools import cycle
from engine.data_types.vector2 import Vector2
from engine.data_types.object import Object
from engine.screen.colors import Colors


class Text(Object):
    
    def __init__(self, text: str, position: list[int, int] | Vector2, blink_every_x_frames: int = None, name: str = None, visible: bool = True, color: TypedDict("color", {"color": Colors, "background_color": Colors}) = {}):
        
        self.text= text
        self.sprite = [list(i) for i in text.split("\n")]
        self.sprite_options = color
        self.sprite_options.setdefault("color", Colors.WHITE)
        self.sprite_options.setdefault("background_color", Colors.BLACK)
        
        if isinstance(position, list):
            position = Vector2(position[0], position[1])
        
        self.position = position
        
        self.length_of_blink = blink_every_x_frames
        self.blink_every_x_frames = blink_every_x_frames
        if self.blink_every_x_frames:
            self.blink_every_x_frames = cycle([(int(i / blink_every_x_frames) == 1) for i in range(1, blink_every_x_frames + 1)])
        
        self.name = name
        self.visible = visible
        
    
    def change_text(self, text: Any):
        
        """Change text of Text object."""
        
        text = str(text)
        self.text = text
        self.sprite = [list(i) for i in text.split("\n")]
        
        
    def switch_visibility(self) -> None:
        
        """Switch's the object visibility."""
        
        if self.visible:
            self.visible = False
        else:
            self.visible = True
            
            
    def blink(self, blink_every_x_frames: int = None) -> None:
        
        """Make object blink."""
        
        if not self.blink_every_x_frames and blink_every_x_frames:
            self.blink_every_x_frames = cycle([(int(i / blink_every_x_frames) == 1) for i in range(1, blink_every_x_frames + 1)])
            self.length_of_blink = blink_every_x_frames
        elif self.blink_every_x_frames and not blink_every_x_frames:
            pass
        elif not self.blink_every_x_frames and not blink_every_x_frames:
            return
        elif self.blink_every_x_frames and blink_every_x_frames:
            if self.length_of_blink != blink_every_x_frames:
                self.blink_every_x_frames = cycle([(int(i / blink_every_x_frames) == 1) for i in range(1, blink_every_x_frames + 1)])
                self.length_of_blink = blink_every_x_frames
        
        if not next(self.blink_every_x_frames):
            return
        
        self.switch_visibility()