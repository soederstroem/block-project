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

        self.debug_text = TextBox(font="debug",content="", pos=(0,0))
        self.rect.topleft = position

        self.standing = False
        self.velocity = pygame.math.Vector2(0,0)

        self.collided = False
        self.collisions = []
        
    def delete(self):
        # print("I fell off, literally.")
        entities.remove(self)
        del self

    def set_pos(self, npos: pygame.math.Vector2):
        self.rect.topleft = npos

    def update(self, keys):
        debug = ""

        if not self.standing:
            self.velocity.y += GRAVITY

        if keys[pygame.K_UP] and self.standing:
            self.velocity.y = -T_VELOCITY

        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0
        
        if self.standing and abs(self.velocity.y) < .01: self.velocity.y = 0
        self.velocity.y = min(self.velocity.y, T_VELOCITY)
        
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.handle_collision()

        debug_content = [
            f"Position: {self.rect.topleft}",
            f"Velocity: {self.velocity}",
            f"Standing? {self.standing}",
            f"Modules loaded: {list(self.modules.keys())}",
            f"Collisions: {len(self.collisions)}"
        ]
        self.debug_text.update("\n".join(debug_content))

        if self.rect.top > SCREEN_DIM[1]:
            self.rect.bottom = -TILE_SIZE

    def check_collision(self):
        self.collided = False
        collisions = []
        grounded = False
        for tile in tiles:
            proximity = self.rect.right in range(tile.rect.left, tile.rect.right + tile.rect.width - 1) and \
               self.rect.left in range(tile.rect.left - tile.rect.width + 1, tile.rect.right) and \
               tile.rect.top in range(self.rect.bottom - int(self.velocity.y/5), self.rect.bottom + 1) and \
               tile.neighbors["up"] is None

            if self.rect.colliderect(tile.rect):
                tile.on_collide()
                collisions.append(tile)
            if proximity and not grounded:
                grounded = True
        
        if grounded: self.velocity.y = 0
        self.standing = grounded
        self.collisions = collisions
        
    def handle_collision(self):
        self.check_collision()
        tiles = self.collisions
        for tile in tiles:
            if tile.collidable == False:
                continue
            offset_y = min(abs(tile.rect.top - self.rect.bottom), abs(tile.rect.bottom - self.rect.top))
            offset_x = min(abs(tile.rect.left - self.rect.right), abs(tile.rect.right - self.rect.left))
            plr_over_tile = tile.rect.top > self.rect.top
            if self.velocity.y > 0 and tile.neighbors["up"] is None and offset_y < TILE_SIZE/5 and plr_over_tile:
                self.rect.y -= offset_y
                self.rect.bottom = tile.rect.top
                self.velocity.y = 0
            elif self.velocity.y < 0 and tile.neighbors["down"] is None and offset_y < max(TILE_SIZE/5,self.velocity.y/5) and not plr_over_tile:
                self.rect.top = tile.rect.bottom
                self.velocity.y = 0
            
            if self.velocity.x > 0 and tile.neighbors["left"] is None:
                self.rect.right -= offset_x
                self.velocity.x = 0
            elif self.velocity.x < 0 and tile.neighbors["right"] is None:
                self.rect.left += offset_x
                self.velocity.x = 0
