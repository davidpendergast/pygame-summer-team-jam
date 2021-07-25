from typing import Sequence, Iterable
import pygame
import cv2


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
                 points: Sequence[pygame.Vector2],
                 width: int,
                 color: pygame.Color,
                 inner_color: pygame.Color = WHITE):
        self.points = points
        self.width = width
        self.inner_color = inner_color
        self.color = color


class NeonRenderer:

    def __init__(self, neon_bloom: float = 3.0, post_processing_bloom: float = 1):
        """
        :param blur: The width of the blurring kernel in pixels.
        """
        self._neon_bloom = neon_bloom
        self._post_processing_bloom = post_processing_bloom

    def draw(self, surface: pygame.Surface, lines: Iterable[NeonLine]):
        for line in lines:
            pygame.draw.lines(surface, line.color, False, line.points, width=line.width)

    def _apply_bloom(self, surface: pygame.Surface, bloom):
        pass


if __name__ == "__main__":
    import random

    W, H = SIZE = (300, 200)
    N = 5

    def rand_pt():
        return pygame.Vector2(random.randint(0, W), random.randint(0, H))

    lines = []
    for _ in range(N):
        lines.append(NeonLine(
            [rand_pt(), rand_pt()],
            random.randint(1, 4),
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
        renderer.draw(screen, lines)

        pygame.display.flip()
        t += 1
        if t % 60 == 59:
            pygame.display.set_caption("FPS: {:.1f}".format(clock.get_fps()))
        clock.tick(60)
