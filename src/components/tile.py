import pygame

from components.entity import entities, Entity
from modules.module import Module

tiles = pygame.sprite.Group()

class Tile(Entity):

    def __init__(self, pos:pygame.math.Vector2, *modules:Module):
        super().__init__()
        entities.remove(self)
        tiles.add(self)

        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = self.rect.topleft
        self.neighbors = {"up":None,"down":None,"left":None,"right":None}
        self.collidable = True

        for module in modules:
            self.attach(module)

        if "ToggleModule" in self.modules.keys():
            toggle = self.modules["ToggleModule"]
            if toggle.role == "t":
                toggle.add_target()

    def update(self):
        self.pos = self.rect.topleft

        if "ToggleModule" in self.modules.keys():
            toggle = self.modules["ToggleModule"]
            if toggle.is_toggled():
                self.image.fill((0,150,0))
    
    def on_collide(self):
        if "ToggleModule" in self.modules.keys():
            toggle = self.modules["ToggleModule"]
            if toggle.role == "s":
                toggle.toggle()


            
        
        
