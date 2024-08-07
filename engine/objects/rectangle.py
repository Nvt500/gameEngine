from __future__ import annotations
from itertools import cycle
from typing import TypedDict
from engine.data_types.vector2 import Vector2
from engine.data_types.path import Path
from engine.data_types.object import Object
from engine.collision.collision_layer import CollisionLayer
from engine.screen.colors import Colors

class Rect(Object):
    
    collision_layer: CollisionLayer = None
    is_on_floor: bool = False
        
    def __init__(self, size: list[int, int] | Vector2, position: list[int, int] | Vector2, screen_size: list[int, int] | Vector2 = None, name: str = None, path: Path = None, update_every_x_frames: int = 1, blink_every_x_frames: int = None, gravity: TypedDict("gravity", {"units_to_fall": int, "update_every_x_frames": int, "automatically_apply_gravity": bool}, frozen=False) = None, sprite: TypedDict("sprite", {"icon": str, "color": Colors, "background_color": Colors}) = {}, static: bool = True, sticky: bool = False, visible: bool = True) -> None:
        
        """
        size: size of rect
        position: position on screen
        screen_size: size of screen rect is on so it can do check_collision_with_screen function
        name: name of rect
        path: path for rect to follow
        update_every_x_frames: how many frames to wait before updating so rect doesn't move across the screen in an instant
        gravity: {units_to_fall: how many units to go down, update_every_x_frames: how many frames to wait before going down}
        sprite: {icon: what will show up to represent rect, color: what color is rect, background_color: the color of the background of rect}
        static: can it be pushed or moved around
        sticky: will objects stick to it when on it (above) (also helpful for moving platforms)
        """
        
        if isinstance(size, list):
            size = Vector2(size)
        
        self.width = size.x
        self.height = size.y
        
        self.sprite_options = sprite
        self.sprite_options.setdefault("icon", "⌷")
        self.sprite_options.setdefault("color", Colors.WHITE)
        self.sprite_options.setdefault("background_color", Colors.BLACK)
        self.sprite = [
            [
                self.sprite_options.get("icon")[(len(self.sprite_options.get("icon")) + i + (e * (self.width - len(self.sprite_options.get("icon"))))) % len(self.sprite_options.get("icon"))] for i in range(self.width)
            ] for e in range(self.height)
        ]
        
        if isinstance(position, list):
            position = Vector2(position)
        
        self.last_position = position
        self.position = position
        
        if isinstance(screen_size, list):
            screen_size = Vector2(screen_size)
        
        self.screen_size = screen_size
        
        self.name = name
        
        self.path = path
        if self.path:
            self.path.rect = self
        
        self.update_every_x_frames = cycle([(int(i / update_every_x_frames) == 1) for i in range(1, update_every_x_frames + 1)])
        
        self.length_of_blink = blink_every_x_frames
        self.blink_every_x_frames = blink_every_x_frames
        if self.blink_every_x_frames:
            self.blink_every_x_frames = cycle([(int(i / blink_every_x_frames) == 1) for i in range(1, blink_every_x_frames + 1)])
        
        self.gravity = gravity
        if self.gravity is not None:
            self.gravity.setdefault("units_to_fall", 1)
            self.gravity.setdefault("update_every_x_frames", 1)
            self.gravity.setdefault("automatically_apply_gravity", True)
            
            self.gravity["update_every_x_frames"] = cycle([(int(i / self.gravity.get("update_every_x_frames")) == 1) for i in range(1, self.gravity.get("update_every_x_frames") + 1)])
            
        self.static = static
        self.sticky = sticky
        self.visible = visible
    
    
    def set_position(self, position: list[int, int] | Vector2) -> None:
        
        """Sets position and makes sure the new position is not out of the screen."""
        
        if isinstance(position, list):
            position = Vector2(position[0], position[1])
        
        if self.screen_size == Vector2.ZERO or not self.check_collision_with_screen(position):
            self.last_position = self.position
            self.position = position
    
    
    def change_position(self, change: list[int, int] | Vector2, with_gravity: bool = False, do_not_do_static: bool = False) -> None:
        
        """Changes position and makes sure the new position is not out of the screen."""
                
        if not next(self.update_every_x_frames):
            return
        
        if isinstance(change, list):
            change = Vector2(change[0], change[1])
         
        if with_gravity and self.gravity:
            if next(self.gravity.get("update_every_x_frames")):
                change.y += self.gravity.get("units_to_fall")
            self.is_on_floor = False
            if self.collision_layer:
                for mask in self.collision_layer.masks:
                    for obj in mask.objects:
                        if self.check_collision_with_rect(rect=obj, new_position=self.position + Vector2.DOWN):
                            self.is_on_floor = True
                            break
                    if self.is_on_floor:
                        break
        
        if self.screen_size != Vector2.ZERO and self.check_collision_with_screen(self.position + change):
            return
        
        try:
        
            objects_to_move = []
            if self.collision_layer:
                for mask in self.collision_layer.masks:
                    for obj in mask.objects:
                        if obj is self:
                            continue                        
                        if self.check_collision_with_rect(rect=obj, new_position=self.position + change):
                            if do_not_do_static:
                                continue
                            elif not obj.static:
                                obj.change_position(change)
                                if not self.check_collision_with_rect(rect=obj, new_position=self.position + change):
                                    continue
                                else:
                                    return
                            else:
                                return
                        if self.sticky and self.check_collision_with_rect(rect=obj, new_position=self.position + Vector2.UP):
                            objects_to_move.append(obj)

            """
            take my object move up one, check with objects, if do then move them by my change
            """

            for obj in objects_to_move:
                obj.change_position(change, do_not_do_static=True)
            
            self.last_position = self.position
            self.position += change
            
        except RecursionError:
            
            self.position = Vector2(self.last_position)
        
    
    def apply_gravity(self) -> None:
        
        """Applies gravity to Rect."""
        
        if self.gravity and self.gravity.get("automatically_apply_gravity"):
            if next(self.gravity.get("update_every_x_frames")):
                self.change_position(Vector2(0, self.gravity.get("units_to_fall")))
            self.is_on_floor = False
            if self.collision_layer:
                for mask in self.collision_layer.masks:
                    for obj in mask.objects:
                        if self.check_collision_with_rect(rect=obj, new_position=self.position + Vector2.DOWN):
                            self.is_on_floor = True
                            break
                    if self.is_on_floor:
                        break
        
        
    def check_if_on_floor(self) -> bool:
        
        """Checks if the there is a object with collision below Rect."""
        
        if self.collision_layer:
            for mask in self.collision_layer.masks:
                for obj in mask.objects:
                    if self.check_collision_with_rect(rect=obj, new_position=self.position + Vector2.DOWN):
                        return True
        
        return False
        
    
    def change_sprite_icon(self, sprite_icon: "str"):
        
        """Changes sprite_icon and updates sprite."""
        
        self.sprite_options["icon"] = sprite_icon
        self.sprite = [
            [
                sprite_icon for i in range(self.width)
            ] for i in range(self.height)
        ]
    
    
    def check_collision_with_screen(self, position: Vector2) -> bool:
        
        """Checks if any part of itself is out of Screen object."""
        
        if not self.screen_size:
            raise Exception("screen_size is not defined.")
        
        if position.x < 0 or position.y < 0 or position.x + self.width > self.screen_size.x or position.y + self.height > self.screen_size.y:
            return True
        
        return False
    
    
    def check_collision_with_rect(self, rect: Rect, new_position: list[int, int] | Vector2 = None) -> bool:
        
        """Checks if Rect object has collision with another Rect object."""
        
        new_position = new_position or self.position
        
        if isinstance(new_position, list):
            new_position = Vector2(new_position)
        
        def check(position: Vector2) -> bool:
            if position.x >= rect.position.x and position.x < rect.position.x + rect.width and position.y >= rect.position.y and position.y < rect.position.y + rect.height:
                return True

            return False
        
        for y in range(self.height):
            for x in range(self.width):
                if check(Vector2(new_position.x + x, new_position.y + y)):
                    return True
        
        return False
    
    
    def check_if_inside_rect(self, rect: Rect) -> bool:
        
        """Checks if Rect object is inside another Rect object."""
        
        if self.position.x >= rect.position.x and self.position.x + self.width <= rect.position.x + rect.width and self.position.y >= rect.position.y and self.position.y + self.height <= rect.position.y + rect.height:
            return True
        
        return False
    
    
    def add_collision_layer(self, layer: CollisionLayer):
        
        """Adds a CollisionLayer to Rect. Is used when adding object to CollisionLayer so only use if you know what you are doing."""
        
        self.collision_layer = layer
        
        
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
            
            
    def change_update_every_x_frames(self, update_every_x_frames: int) -> None:
        
        """Changes the attribute update_every_x_frames while making the cycle."""
        
        self.update_every_x_frames = cycle([(int(i / update_every_x_frames) == 1) for i in range(1, update_every_x_frames + 1)])
    
