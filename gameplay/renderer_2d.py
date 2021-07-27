import random

import pygame

# assumption
# horizontal -> x-axis
# vertical -> y-axis
# into-the-screen-axis -> z-axis
import gameplay.player2d as player2d
import util.utility_functions as utility_functions


class Level:
    def __init__(self, player: player2d.Player, sides=6):
        self.lanes = sides
        self.player = player
        self.length = 1000
        self.craters = [[random.randint(0, 5), random.randint(150, self.length - 200)] for _ in range(10)]  # format -> [lane, z-coordinate]

    def update(self):
        for i in self.craters:
            player_rect = pygame.Rect(100 + self.player.lane * 100 + 25, self.player.z, 50, 50)
            crater_rect = pygame.Rect(100 + i[0] * 100 + 25, i[1], 50, 50)
            if player_rect.colliderect(crater_rect) and self.player.y < 1:
                self.player.collided = True
                break
            else:
                self.player.collided = False


class Renderer:
    def __init__(self, display: pygame.Surface, level: Level):
        self.display = display
        self.level = level

    def update(self, events):
        self.level.update()

    def render_craters(self):
        for i in self.level.craters:
            pygame.draw.rect(self.display, (255, 0, 0), (100 + 25 + i[0] * 100, 600 - 100 - i[1] - 0 + self.level.player.z, 50, 50), 2)
            utility_functions.Text(self.display, 'Z: ' + str(i[1]), 100 + i[0] * 100, 600 - 100 - i[1] + self.level.player.z, 15).draw()

    def render_player(self):
        pygame.draw.rect(self.display, (255, 255, 0), (self.level.player.lane * 100 + 100 + 25, 600 - 100 - 0, 50, 50), 2)

    def render_level(self):
        for i in range(self.level.lanes):
            pygame.draw.rect(self.display, (0, 0, 255), (100 + i * 100, 600 - 100 - self.level.length + self.level.player.z, 100, self.level.length), 2)
        self.render_craters()
        self.render_player()


def preview_code():
    import sys

    pygame.init()

    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

    clock = pygame.time.Clock()

    p = player2d.Player()
    level1 = Level(p)
    r = Renderer(screen, level1)

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)
        screen.fill((0, 0, 0))
        r.update(events)
        p.update(1 / 60, events)
        r.render_level()
        p.draw(screen)
        utility_functions.Text(screen, 'FPS: ' + str(int(clock.get_fps())), 25, 25, 25).draw()
        pygame.display.update()
        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(60)


preview_code()
