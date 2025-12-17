import pygame

from components.entity import Entity, entities
from components.map import tiles
from core.physics import *
from core.cfg import *
from core.utils import *


class Player(Entity):

    def __init__(self, pos:pygame.math.Vector2=(0,0)):
        super().__init__()
        entities.add(self)
        self.state = "airborne"
        self.velocity = pygame.math.Vector2(0, 0)
        self.collided = False

        self.debug_text = TextBox("", pos=(0,50))
    
    def delete(self):
        # print("I fell off, literally.")
        entities.remove(self)
        del self

    def set_pos(self, npos: pygame.math.Vector2):
        self.pos = npos

    def update(self, keys):
        debug = ""

        if self.state == "standing":
            self.velocity.y = 0
        else:
            self.velocity.y += gravity

        if keys[pygame.K_UP] and self.state != "airborne" and self.velocity.y == 0:
            self.velocity.y = -10

        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0
        
        self.velocity.y = min(self.velocity.y, 10)
        self.pos += self.velocity
        self.rect.topleft = self.pos

        self.collider = None
        self.collided = False
        for tile in tiles:
            collision = check_collision(self, tile)
            if collision in ("left", "right"):
                self.collided = True
                self.velocity.x = 0
                handle_collision(self, tile)
                break
            elif collision == "top":
                self.collided = True
                self.collider = tile
                handle_collision(self, tile)
                if self.state == "airborne":
                    self.velocity.y = 0
                self.state = "standing"
                break
            elif collision == "bottom" and self.velocity.y < 0:
                self.collided = True
                self.velocity.y = 0
                break
            tile.image.fill("blue")


        if not self.collided:
            self.state = "airborne"

        self.debug_text.update(f"{self.state}, {debug}, {collision}")

        if self.pos.y > SCREEN_DIM[1]:
            self.pos.y = -50


        
