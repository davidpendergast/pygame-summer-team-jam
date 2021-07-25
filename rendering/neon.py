from typing import List, Iterable, Tuple
import pygame
import cv2
import numpy


# taken from https://www.coolneon.com/wp-content/uploads/2014/11/color-chart.png
CYAN = pygame.Color(0, 255, 255)
BLUE = pygame.Color(0, 84, 247)
TEAL = pygame.Color(0, 161, 115)
LIME = pygame.Color(123, 255, 0)
YELLOW = pygame.Color(251, 208, 0)
ORANGE = pygame.Color(255, 70, 0)
RED = pygame.Color(231, 0, 0)
PURPLE = pygame.Color(154, 0, 154)
PINK = pygame.Color(253, 17, 96)
WHITE = pygame.Color(200, 200, 255)

ALL_COLORS = [CYAN, BLUE, TEAL, LIME, YELLOW, ORANGE, RED, PURPLE, PINK, WHITE]


class NeonLine:
    """
    Represents a line NeonRenderer can draw.
    """
    def __init__(self,
                 points: List[pygame.Vector2],
                 width: int,
                 color: pygame.Color,
                 inner_color: pygame.Color = None,
                 inner_width: int = None):

        self.vector_points = points
        # x and y are flipped intentionally... this is what cv2 understands, don't ask me~
        self.np_points = numpy.array([[round(p.y), round(p.x)] for p in points], numpy.int32).reshape((-1, 1, 2))
        self.width = width
        self.inner_width = inner_width or 1
        self.inner_color = inner_color or color.lerp(WHITE, 0.5)
        self.color = color


class NeonRenderer:

    def __init__(self,
                 neon_bloom: float = (25, 25),
                 post_processing_bloom: float = (3, 3)):
        self._neon_bloom = neon_bloom
        self._post_processing_bloom = post_processing_bloom

    def draw_lines(self, surface: pygame.Surface, lines: Iterable[NeonLine]):
        array = pygame.surfarray.array3d(surface)

        # Ghast's Neon Line Drawing AlgorithmTM

        # 1st pass, draw large, dark, faint glow around line
        for line in lines:
            cv2.polylines(array, [line.np_points], False, line.color.lerp((0, 0, 0), 0.25), line.width)
        array = cv2.blur(array, self._neon_bloom)

        # 2nd pass, draw smaller, brighter glow
        for line in lines:
            cv2.polylines(array, [line.np_points], False, line.inner_color, line.inner_width, lineType=cv2.LINE_AA)
        array = cv2.blur(array, self._post_processing_bloom)

        # 3rd pass, draw anti-aliased highlight, don't blur
        for line in lines:
            cv2.polylines(array, [line.np_points], False, line.inner_color.lerp((255, 255, 255), 0.75), line.inner_width, lineType=cv2.LINE_AA)

        pygame.surfarray.blit_array(surface, array)


if __name__ == "__main__":
    import random

    W, H = SIZE = (300, 200)
    N = 50

    def rand_pt():
        return pygame.Vector2(random.randint(0, W), random.randint(0, H))

    lines = []
    for _ in range(N):
        lines.append(NeonLine(
            [rand_pt(), rand_pt()],
            random.randint(1, 1),
            random.choice(ALL_COLORS)))

    renderer = NeonRenderer()

    pygame.init()
    pygame.display.set_mode((300, 200), pygame.SCALED | pygame.RESIZABLE)

    clock = pygame.time.Clock()
    t = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit

        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        renderer.draw_lines(screen, lines)

        pygame.display.flip()
        t += 1
        if t % 60 == 59:
            pygame.display.set_caption("FPS: {:.1f}".format(clock.get_fps()))
        clock.tick(60)
