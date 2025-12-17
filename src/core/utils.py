import pygame

pygame.font.init()
fonts = {
    "regular": pygame.font.SysFont("malgungothic", 30),
}

class TextBox:

    def __init__(self, content: str, font:pygame.font.Font=fonts["regular"], pos=pygame.math.Vector2(0,0)):
        self.content = content
        self.font = font
        self.pos = pos
        self.text = self.font.render(self.content, False, "black","white")
        self.rect = self.text.get_rect()
        
    def update(self, newcontent=None):
        if newcontent == None:
            newcontent = self.content
        
        self.text = self.font.render(newcontent, False, "black","white")
        self.rect = self.text.get_rect()
        self.rect.topleft = self.pos

    def draw(self, surface):
        surface.blit(self.text, self.rect)