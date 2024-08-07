import curses

class Keyboard:
    
    keys: str = ""
    wrapper: curses.window = None
    
    def __init__(self, wrapper: curses.window):
        
        self.wrapper = wrapper
    
    
    def get_input(self, wrapper: curses.window = None) -> None:
        
        """Gets input through curses wrapper."""
        
        self.wrapper = wrapper or self.wrapper
        
        self.wrapper.nodelay(True)
        self.wrapper.keypad(True)
        
        try:
            self.keys = str(self.wrapper.getkey())
        except:
            self.keys = ""
    
    
    def get_keys(self) -> str:
        
        """Gets the keys pressed."""
        
        return self.keys
    
    
    def get_key(self, key: str | int) -> bool | None:
        
        """Gets if a certain key is pressed."""
        
        if isinstance(key, str):
            return key in self.keys
        else:
            try:
                return curses.keyname(key) in self.keys
            except Exception as e:
                return None
