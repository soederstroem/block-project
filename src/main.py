import pygame
from components.player import *
from components.entity import entities
from core.cfg import *
from components.map import *
from core.utils import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("BLOCK")
clk = pygame.time.Clock()
done = False

map = Map("test2")
map.load_tiles()
player = Player(map.plr_spawn_pos)
bkg = pygame.transform.scale(pygame.image.load(map.bkg), SCREEN_DIM)

text = TextBox("Hello!")

while not done:
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if keys[pygame.K_ESCAPE]:
            player.image.fill("black")
        if event.type == pygame.QUIT:
            done = True

    entities.update(keys)
    tiles.update()

    text.update(f"{player.state}, {player.velocity}, {player.pos}")
    
    screen.fill("white")
    screen.blit(bkg,(0,0))

    tiles.draw(screen)
    entities.draw(screen)
    text.draw(screen)
    player.debug_text.draw(screen)

    pygame.display.flip()
    clk.tick(60)

pygame.quit()