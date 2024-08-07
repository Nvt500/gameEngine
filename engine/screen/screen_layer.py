from engine.data_types.object import Object

class ScreenLayer:
    
    def __init__(self, objects: list[Object] = None):
        
        self.objects = objects or []