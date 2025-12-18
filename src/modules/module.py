import pygame

class Module:

    def __init__(self):
        self.parent = None

        self.on_attach()

    def update(self):
        pass

    def on_attach(self):
        pass

    def on_detach(self):
        pass