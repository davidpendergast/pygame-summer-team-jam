import pygame

import main
import gameplay.player2d as player2d


class GameplayMode(main.GameMode):

    def __init__(self, loop):
        super().__init__(loop)
        self.player = player2d.Player()

    def update(self, dt, events):
        pass

    def draw_to_screen(self, screen):
        screen.fill((255, 0, 0))
