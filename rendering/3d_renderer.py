import math
import pygame

import neon


class Renderer:
    # Renderer class to render levels
    def __init__(self):
        self.level = {
            'shape': 6,
        }
        self.zoom1 = 1
        self.zoom2 = 1
        self.angle = 0
        self.angle_k = 5
        self.renderer = neon.NeonRenderer()

    def load_level(self, level):
        self.level = level

    def go_right(self):
        self.angle_k = abs(self.angle_k)
        self.angle += self.angle_k

    def go_left(self):
        self.angle_k = -abs(self.angle_k)
        self.angle += self.angle_k

    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.go_left()
                if e.key == pygame.K_RIGHT:
                    self.go_right()

    def render_level(self, display: pygame.Surface):
        side_length = 50 * self.zoom2 if self.zoom1 > 3 else 50
        n = self.level['shape']
        offset_x = 300
        offset_y = 300 + n * 15
        offset_angle = math.radians((n - 2) * 90 / n + self.angle)
        if self.angle % ((n - 2) * 90 // n) != 0:
            self.angle += self.angle_k
        if self.zoom1 > 3:
            self.zoom2 += 0.1

        color = pygame.Color(255, 0, 0)
        points1 = [pygame.Vector2(offset_x + side_length * math.cos(offset_angle + 2 * math.pi * i / n), offset_y + side_length * math.sin(offset_angle + 2 * math.pi * i / n)) for i in range(n)]
        side_length = 250
        offset_x = 300
        offset_y = 300
        points2 = [pygame.Vector2(offset_x + side_length * math.cos(offset_angle + 2 * math.pi * i / n), offset_y + side_length * math.sin(offset_angle + 2 * math.pi * i / n)) for i in range(n)]
        p1 = [neon.NeonLine(points1 + [points1[0]], 3, color)]
        p2 = [neon.NeonLine(points2 + [points2[0]], 3, color)]
        p3 = []
        for i in range(n):
            p3.append(neon.NeonLine([pygame.Vector2(points1[i][0], points1[i][1]), pygame.Vector2(points2[i][0], points2[i][1])], 3, color))
        self.renderer.draw_lines(display, p1 + p2 + p3)

        
def preview_code():
    # call it to see demo
    import sys

    pygame.init()

    screen = pygame.display.set_mode((600, 600))

    clock = pygame.time.Clock()

    r = Renderer()

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
        r.render_level(screen)
        pygame.display.update()
        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(0)
