import curses
from typing import Generator, TypedDict
from engine.objects.rectangle import Rect
from engine.objects.debug import Debug
from engine.data_types.object import Object
from engine.data_types.vector2 import Vector2
from engine.screen.screen_layer import ScreenLayer
from engine.screen.colors import Colors
from engine.collision.collision_layer import CollisionLayer


class Screen:
    
    wrapper: curses.window = None
    keys: str | None = None
    
    def __init__(self, size: list[int, int] | Vector2, frames_per_second: int = 20, background: TypedDict("background", {"icon": str, "color": Colors, "background_color": Colors}) = {}, initialize: bool = True, get_input: bool = True, borderless: bool = False, no_separator: bool = False) -> None:
        
        """
        size: size of screen
        frames_per_second: how much time to wait after every update of screen, int number of times per second
        background
        """
        
        self.screen_layers = [ScreenLayer()]
        
        if isinstance(size, list):
            size = Vector2(size[0], size[1])
        
        self.width = size.x
        self.height = size.y
        self.LEFT = 0
        self.RIGHT = size.x - 1
        self.TOP = 0
        self.BOTTOM = size.y -1
        self.background = background
        self.background.setdefault("icon", "#")
        self.background.setdefault("color", Colors.WHITE)
        self.background.setdefault("background_color", Colors.BLACK)
        self.screen = [
            [
                (self.background.get("icon")[(len(self.background.get("icon")) + i + (e * (self.width - len(self.background.get("icon"))))) % len(self.background.get("icon"))], self.background.get("color"), self.background.get("background_color")) for i in range(self.width)
            ] for e in range(self.height)
        ]
        
        if initialize:
            self.wrapper = curses.wrapper(lambda w: w)
            self.wrapper.nodelay(True)
            self.wrapper.keypad(True)
            curses.noecho()
            curses.cbreak()
            curses.start_color()
            curses.use_default_colors()
        
        self.frames_per_second = frames_per_second
        
        if get_input:
            self.keys = ""
        
        self.borderless = borderless
        self.no_separator = no_separator
    
    
    def create_screen_string(self) -> Generator[tuple[str, Colors, Colors], None, None]:
        
        debugs = []
        
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
                        try:
                            self.screen[obj.position.y + y][obj.position.x + x] = (elem, obj.sprite_options.get("color"), obj.sprite_options.get("background_color"))
                        except IndexError:
                            raise Exception(f"The object {obj.name or obj.__class__.__name__} is probably out of the screen.")
        
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
    
    
    def __repr__(self) -> str:
        
        string = ""
        for line in self.create_screen_string():
            string += line[0]
        return string
    
    
    def print_screen(self) -> None:
        
        """Adds screen string to curses wrapper."""
        
        for line in self.create_screen_string():
            curses.init_pair((line[1]*8) + line[2] + 1, line[1], line[2])
            self.wrapper.addstr(line[0], curses.color_pair((line[1]*8) + line[2] + 1))
        self.wrapper.refresh()
    
    
    def init(self) -> None:
        
        """Initializes curses wrapper if not initialized in __init__."""
        
        if not self.wrapper:
            self.wrapper = curses.wrapper(lambda w: w)
            self.wrapper.nodelay(True)
            self.wrapper.keypad(True)
            curses.cbreak()
            curses.start_color()
            curses.use_default_colors()
    

    def update(self, frames_per_second: int = None) -> None:
        
        """Updates screen and gets input if specified in __init__."""
        
        for layer in self.screen_layers:
            for obj in layer.objects:
                if hasattr(obj, "gravity"):
                    obj.apply_gravity()
                if hasattr(obj, "path") and obj.path:
                    obj.path.move()
        
        frames_per_second = frames_per_second or self.frames_per_second
        
        if self.keys != None:
            try:
                self.keys = str(self.wrapper.getkey())
            except:
                self.keys = ""
        
        self.wrapper.clear()
        self.print_screen()
        
        curses.napms(int(1000 / frames_per_second))
    

    def close(self, remove_all_objects: bool = True) -> None:

        """Closes curses window."""
        
        if remove_all_objects:
            screen_layers = [ScreenLayer()]
        
        curses.nocbreak()
        self.wrapper.keypad(False)
        curses.echo()
        curses.endwin()

    
    def add_object(self, obj: Object, layer: int) -> None:
        
        """Adds object to screen on a specified screen layer."""
        
        if layer < 0 or layer >= len(self.screen_layers):
            raise Exception(f"Layer [{layer}] does not exist.")
        
        obj.screen_size = Vector2(self.width, self.height)
        self.screen_layers[layer].objects.append(obj)
    
    
    def add_objects(self, layer: int, *objects: Object | CollisionLayer) -> None:
        
        """Adds a list of objects to screen on a specified layer."""
        
        if layer < 0 or layer >= len(self.screen_layers):
            raise Exception(f"Layer [{layer}] does not exist.")
        
        for obj in objects[::-1]:
            if isinstance(obj, CollisionLayer):
                for o in obj.objects:
                    o.screen_size = Vector2(self.width, self.height)
                    self.screen_layers[layer].objects.append(o)
            else:
                obj.screen_size = Vector2(self.width, self.height)
                self.screen_layers[layer].objects.append(obj)
    
    
    def get_keys(self) -> str:
        
        """Gets the keys pressed."""
        
        if self.keys == None:
            raise Exception("get_input is not enabled in screen.")
            
        return self.keys
    
    
    def get_key(self, key: str | int) -> bool:
        
        """Gets if a certain key is pressed."""
        
        if self.keys == None:
            raise Exception("get_input is not enabled in screen.")
            
        if isinstance(key, str):
            return key in self.keys
        else:
            try:
                return curses.keyname(key) in self.keys
            except Exception as e:
                return False

        
        
        
        
        
