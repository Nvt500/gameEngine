from __future__ import annotations
from engine.data_types.object import Object

class CollisionLayer:
    
    def __init__(self, name: str, objects: list[Object] = None, masks: list[CollisionLayer | Object] = None, collide_with_self: bool = False):
        
        self.name = name
        self.masks: list[self.__class__] = masks or []
        for i, mask in enumerate(self.masks):
            if isinstance(mask, Object):
                self.masks[i] = self.__class__(f"{mask.name or mask.__class__.__name__}_cl", [mask])
        if collide_with_self:
            self.masks.append(self)
        self.objects = objects[::-1] or []
        for obj in self.objects:
            obj.add_collision_layer(self)
    
    
    def create_masks(self, *layers: CollisionLayer | Object, give_mask_self: bool = True):
        
        """Adds CollisionLayers to collide/interact with."""
        
        for layer in layers:
            if isinstance(layer, Object):
                layer = self.__class__(f"{layer.name or layer.__class__.__name__}_cl", [layer])
                self.masks.append(layer)
            else:
                self.masks.append(layer)
            if give_mask_self:
                layer.masks.append(self)
    
    
    def add_object(self, obj: Object):
        
        """Adds an object to CollisionLayer."""
        
        obj.add_collision_layer(self)
        self.objects.append(obj)
    
    
    
    def add_objects(self, *objects: Object):
        
        """Adds objects to CollisionLayer."""
        
        for obj in objects:
            obj.add_collision_layer(self)
            self.objects.append(obj)