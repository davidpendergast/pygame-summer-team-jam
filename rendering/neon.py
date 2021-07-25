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
WHITE = pygame.Color(220, 220, 255)

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
                 ambient_bloom_kernel=(25, 25),
                 mid_tone_bloom_kernel=(3, 3),
                 highlight_bloom_kernel=None):
        self.ambient_bloom_kernel = ambient_bloom_kernel
        self.mid_tone_bloom_kernel = mid_tone_bloom_kernel
        self.highlight_bloom_kernel = highlight_bloom_kernel

        # post processing
        self.post_processing_darken_factor = 0.9
        self.post_processing_contrast_factor = None  # makes things worse, so disabled

    def draw_lines(self, surface: pygame.Surface, lines: Iterable[NeonLine]):
        array = pygame.surfarray.array3d(surface)

        # Ghast's Neon Line Drawing AlgorithmTM

        # 1st pass, draw large, dark, faint glow around line
        for line in lines:
            cv2.polylines(array, [line.np_points], False, line.color.lerp((0, 0, 0), 0.15), line.width)
        if self.ambient_bloom_kernel is not None:
            array = cv2.blur(array, self.ambient_bloom_kernel)

        # 2nd pass, draw smaller, brighter glow
        for line in lines:
            cv2.polylines(array, [line.np_points], False, line.color, line.inner_width, lineType=cv2.LINE_AA)
        if self.mid_tone_bloom_kernel is not None:
            array = cv2.blur(array, self.mid_tone_bloom_kernel)

        # 3rd pass, draw anti-aliased highlight
        for line in lines:
            cv2.polylines(array, [line.np_points], False, line.inner_color.lerp((255, 255, 255), 0.7), line.inner_width, lineType=cv2.LINE_AA)
        if self.highlight_bloom_kernel is not None:
            array = cv2.blur(array, self.highlight_bloom_kernel)

        # post processing effects
        if self.post_processing_darken_factor is not None:
            array = self._darken(array, self.post_processing_darken_factor)
        if self.post_processing_contrast_factor is not None:
            array = self._contrast(array, self.post_processing_contrast_factor)

        pygame.surfarray.blit_array(surface, array)

    def _darken(self, array, factor):
        hsvImg = cv2.cvtColor(array, cv2.COLOR_RGB2HSV)
        hsvImg[..., 2] = hsvImg[..., 2] * factor
        return cv2.cvtColor(hsvImg, cv2.COLOR_HSV2RGB)

    def _contrast(self, array, factor):
        # yoinked from https://stackoverflow.com/a/41075028
        lab = cv2.cvtColor(array, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(18, 18))
        cl = clahe.apply(l)

        # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl, a, b))

        # -----Converting image from LAB Color model to RGB model--------------------
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


if __name__ == "__main__":
    import random

    W, H = SIZE = (600, 400)
    N = 50

    def rand_pt():
        return pygame.Vector2(random.randint(0, W), random.randint(0, H))

    lines = []
    for _ in range(N):
        lines.append(NeonLine(
            [rand_pt(), rand_pt()],
            random.randint(1, 1),
            random.choice(ALL_COLORS)))

    # values determined empirically
    big_bloom = round(25 * W / 300)
    big_bloom = big_bloom + (1 - big_bloom % 2)  # gotta be odd
    mid_bloom = round(3 * W / 300)
    mid_bloom = mid_bloom + (1 - mid_bloom % 2)  # gotta be odd
    renderer = NeonRenderer(ambient_bloom_kernel=(big_bloom, big_bloom),
                            mid_tone_bloom_kernel=(mid_bloom, mid_bloom))

    pygame.init()
    pygame.display.set_mode((W, H), pygame.SCALED | pygame.RESIZABLE)

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
