from typing import List, Iterable

import numpy
import pygame

from pygame import Vector3, Vector2


class Line3D:

    def __init__(self, p1: Vector3, p2: Vector3, color=(255, 255, 255), width=1):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.width = width


class Line2D:

    def __init__(self, p1: Vector2, p2: Vector2, color=(255, 255, 255), width=1):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.width = width


class Camera3D:

    def __init__(self, style="ortho"):
        self.position = Vector3(0, 0, 0)
        self.forward: Vector3 = Vector3(0, 0, 1)
        self.up: Vector3 = Vector3(0, -1, 0)
        self.fov: float = 45  # horizontal field of view
        self.style = style

    def xform_pt(self, surface_size, pt: Vector3) -> Vector2:
        if self.style == "test":
            return Vector2(surface_size[0] // 2 + pt.x - self.position[0], surface_size[1] // 2 - pt.y + self.position[1])

    def project_to_surface(self, surface, lines: Iterable[Line3D]) -> List[Line2D]:
        res = []
        dims = surface.get_size()
        for l in lines:
            p1_2d = self.xform_pt(dims, l.p1)
            p2_2d = self.xform_pt(dims, l.p2)
            if p1_2d is not None and p2_2d is not None:
                res.append(Line2D(p1_2d, p2_2d, color=l.color, width=l.width))
        return res


def gen_cube(angle, size, center):
    res = []
    pts = []
    for x in (-1, 1):
        for z in (-1, 1):
            xz = Vector2(x, z)
            xz = xz.rotate(angle)
            for y in (-1, 1):
                pts.append(Vector3(xz[0], y, xz[1]) * (size / 2) + center)

                pt = pts[-1]
                for n in pts[:len(pts)-1]:
                    if abs((pt - n).length() - size) <= 0.1:
                        res.append(Line3D(pt, n))
    return res


if __name__ == "__main__":
    # call it to see demo
    import sys

    pygame.init()

    screen = pygame.display.set_mode((600, 600))

    clock = pygame.time.Clock()

    camera = Camera3D(style="test")
    camera.position = Vector3(0, 0, 0)
    p1 = Vector3(10, 15, 30)
    p2 = Vector3(10, -20, 30)
    p3 = Vector3(-20, 15, 30)
    p4 = Vector3(-20, 15, 50)

    lines = [
        Line3D(p1, p2, color=(255, 125, 125)),
        Line3D(p2, p3, color=(125, 255, 0)),
        Line3D(p3, p4, color=(125, 125, 255)),
        Line3D(Vector3(-300, -300, 30), Vector3(300, 300, 30), color=(255, 255, 255)),
        Line3D(Vector3(300, -300, 30), Vector3(-300, 300, 30), color=(255, 100, 100)),
    ]

    angle = 0
    lines = []

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)
        screen.fill((0, 0, 0))

        angle += 1
        lines = gen_cube(angle, 100, Vector3(0, 0, 300))

        lines_2d = camera.project_to_surface(screen, lines)
        for l in lines_2d:
            pygame.draw.line(screen, l.color, l.p1, l.p2, l.width)

        pygame.display.update()
        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(60)

