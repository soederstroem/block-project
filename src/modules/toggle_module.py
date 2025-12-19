import pygame

from modules.module import Module

toggles = {}

class ToggleModule(Module):

    def __init__(self, group:str="default", role="s"):
        self.group = group
        self.timed = False
        self.timer = 0
        self.role = role

        if self.group not in toggles.keys():
            toggles[f"{self.group}"] = {}
            toggles[f"{self.group}"]["targets"] = pygame.sprite.Group()
            toggles[f"{self.group}"]["toggled"] = False
        pass

    def is_toggled(self):
        return toggles[f"{self.group}"]["toggled"]

    def add_target(self):
        toggles[f"{self.group}"]["targets"].add(self.parent)

    def toggle(self):
        toggles[f"{self.group}"]["toggled"] = True

    def on_toggled(self):
        self.parent.toggled = toggles[f"{self.group}"]["toggled"]

    def on_attach(self):
        self.parent.toggled = False

    def on_detach(self):
        del self.parent.toggled

    def update(self):
        pass