import pygame
from modules.module import Module

entities = pygame.sprite.Group()

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos:pygame.math.Vector2=pygame.math.Vector2(0,0), *modules:Module):
        super().__init__()
        entities.add(self)    
        self.image = pygame.Surface((50,50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)
        self.modules = {}
        self.pos = self.rect.topleft

        for module in modules:
            self.attach(module)

    def attach(self, module:Module):
        if module not in list(self.modules.values()):
            module.parent = self
            self.modules[type(module).__name__] = module
        else: return

    def detach(self, *module:Module):
        if module in list(self.modules.values()):
            module.on_detach()
            del self.modules[module.__name__]
        else: return

    def update(self):
        self.pos = self.rect.topleft

        for module in self.modules:
            module.update()

    def on_collide(self):
        pass