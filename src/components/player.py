import pygame

from components.entity import Entity, entities
from components.map import tiles
# from modules.physics import *
from core.cfg import *
from core.utils import *


class Player(Entity):

    Vec2 = pygame.math.Vector2
    def __init__(self, position:Vec2=Vec2(0,0)):
        super().__init__()
        entities.add(self)

        self.modules = {}
        self.debug_text = TextBox(font="debug",content="", pos=(0,0))
        self.rect.topleft = position

        self.state = "airborne"
        self.velocity = pygame.math.Vector2(0,0)

        self.collided = False
        self.collisions = []
        
    def delete(self):
        # print("I fell off, literally.")
        entities.remove(self)
        del self

    def set_pos(self, npos: pygame.math.Vector2):
        self.rect = npos

    def update(self, keys):
        debug = ""

        if self.state == "standing":
            self.velocity.y = 0
        else:
            self.velocity.y += GRAVITY

        if keys[pygame.K_UP] and self.state == "standing":
            self.velocity.y = -10

        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0
        
        if abs(self.velocity.y) < .01: self.velocity.y = 0
        self.velocity.y = min(self.velocity.y, T_VELOCITY)
        
        self.rect.topleft += self.velocity

        self.handle_collision()

        self.debug_text.update(f"Position: (POS:{self.rect.topleft}\nVelocity: {self.velocity}\nState: {self.state}\nModules: {list(self.modules.keys())}\nCollisions: {self.collisions}")

        if self.rect.top > SCREEN_DIM[1]:
            self.rect.bottom = -50

    def check_collision(self):
        self.collided = False
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                collisions.append(tile)

        self.collisions = collisions
        
    def handle_collision(self):

        self.check_collision()
        tiles = self.collisions
        for tile in tiles:
            offset_y = tile.rect.top - self.rect.bottom

            if self.velocity.y > 0 and tile.neighbors["up"] is None:
                self.rect.y -= offset_y
                self.rect.bottom = tile.rect.top
                self.velocity.y = 0
                self.state == "standing"
            elif self.velocity.y < 0:
                self.rect.top = tile.rect.top
                self.velocity.y = 0
                self.state == "airborne"

        self.check_collision()
        tiles = self.collisions
        for tile in tiles:
            offset_x = min(abs(tile.rect.left - self.rect.right), abs(tile.rect.right - self.rect.left))
            if self.velocity.x > 0 and tile.neighbors["left"] is None:
                self.rect.right -= offset_x
                self.velocity.x = 0
                self.state == "airborne"
            elif self.velocity.x < 0 and tile.neighbors["right"] is None:
                self.rect.left += offset_x
                self.velocity.x = 0
                self.state == "airborne"
