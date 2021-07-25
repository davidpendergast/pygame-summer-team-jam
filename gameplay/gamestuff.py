import pygame

import main


class GameplayMode(main.GameMode):

    def __init__(self, loop):
        super().__init__(loop)

    def update(self, dt, events):
        pass

    def draw_to_screen(self, screen):
        screen.fill((255, 0, 0))
