import pygame

entities = pygame.sprite.Group()

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos:pygame.math.Vector2=(0,0)):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((50,50))
        self.image.fill("red")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = self.pos