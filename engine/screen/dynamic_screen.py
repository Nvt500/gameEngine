import curses
from typing import Generator, TypedDict
from engine.objects.rectangle import Rect
from engine.objects.debug import Debug
from engine.data_types.object import Object
from engine.data_types.vector2 import Vector2
from engine.screen.screen import Screen
from engine.screen.screen_layer import ScreenLayer
from engine.screen.colors import Colors
from engine.collision.collision_layer import CollisionLayer


class DynamicScreen(Screen):
    
    def __init__(self, size: list[int, int] | Vector2, center: Rect | Vector2, offset: Vector2 = None, frames_per_second: int = 20, background: TypedDict("background", {"icon": str, "color": Colors, "background_color": Colors}) = {}, initialize: bool = False, get_input: bool = False, borderless: bool = False, no_separator: bool = False) -> None:
        
        super().__init__(size, frames_per_second, background, initialize, get_input, borderless, no_separator)
        
        self.center = center
        self.offset = offset or Vector2.ZERO
        
        if isinstance(size, list):
            size = Vector2(size[0], size[1])
            
        self.size = size
        
        self.LEFT = self.center.position.x - int(self.size.x / 2 - 0.5)
        self.RIGHT = self.center.position.x + int(self.size.x / 2)
        self.TOP = self.center.position.y - int(self.size.y / 2 - 0.5)
        self.BOTTOM = self.center.position.y + int(self.size.y / 2)
        
    
    def create_screen_string(self) -> Generator[tuple[str, Colors, Colors], None, None]:
        
        debugs = []
        
        self.LEFT = self.center.position.x - self.offset.x - int(self.size.x / 2 - 0.5)
        self.RIGHT = self.center.position.x - self.offset.x + int(self.size.x / 2)
        self.TOP = self.center.position.y - self.offset.y - int(self.size.y / 2 - 0.5)
        self.BOTTOM = self.center.position.y - self.offset.y + int(self.size.y / 2)
        
        self.screen = [
            [
                (self.background.get("icon")[(len(self.background.get("icon")) + i + (e * (self.width - len(self.background.get("icon"))))) % len(self.background.get("icon"))], self.background.get("color"), self.background.get("background_color")) for i in range(self.width)
            ] for e in range(self.height)
        ]
        
        
        for layer in self.screen_layers:
            for obj in layer.objects:
                if isinstance(obj, Debug):
                    debugs.append(obj)
                    continue
                if not obj.visible:
                    continue
                for y, row in enumerate(obj.sprite):
                    for x, elem in enumerate(row):
                        if obj.position.x + x >= self.LEFT and obj.position.x + x <= self.RIGHT and obj.position.y + y >= self.TOP and obj.position.y + y <= self.BOTTOM:
                            self.screen[obj.position.y + y - self.TOP][obj.position.x + x - self.LEFT] = (elem, obj.sprite_options.get("color"), obj.sprite_options.get("background_color"))
        
        for row in self.screen:
            if not self.borderless:
                yield (" |", Colors.WHITE, Colors.BLACK)
            for elem in row:
                if not self.no_separator:
                    yield (f" {elem[0]}", elem[1], elem[2])
                else:
                    yield (elem[0], elem[1], elem[2])
            if not self.borderless:
                if not self.no_separator:
                    yield (" |", Colors.WHITE, Colors.BLACK)
                else:
                    yield ("|", Colors.WHITE, Colors.BLACK)
            yield ("\n", Colors.WHITE, Colors.BLACK)
        if not self.borderless:
            if not self.no_separator:
                yield (f" |{self.width * ' _'} |\n", Colors.WHITE, Colors.BLACK)
            else:
                yield (f" |{self.width * '_'}|\n", Colors.WHITE, Colors.BLACK)
        
        for obj in debugs:
            yield (f"{obj.text}\n", obj.color.get("color"), obj.color.get("background_color"))
    
    
    def add_object(self, obj: Object, layer: int) -> None:
        
        """Adds object to screen on a specified screen layer."""
        
        if layer < 0 or layer >= len(self.screen_layers):
            raise Exception(f"Layer [{layer}] does not exist.")
        
        obj.screen_size = Vector2.ZERO
        self.screen_layers[layer].objects.append(obj)
    
    
    def add_objects(self, layer: int, *objects: Object | CollisionLayer) -> None:
        
        """Adds a list of objects to screen on a specified layer."""
        
        if layer < 0 or layer >= len(self.screen_layers):
            raise Exception(f"Layer [{layer}] does not exist.")
        
        for obj in objects[::-1]:
            if isinstance(obj, CollisionLayer):
                for o in obj.objects:
                    o.screen_size = Vector2.ZERO
                    self.screen_layers[layer].objects.append(o)
            else:
                obj.screen_size = Vector2.ZERO
                self.screen_layers[layer].objects.append(obj)
        