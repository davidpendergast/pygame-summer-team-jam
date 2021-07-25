from typing import List, Iterable

import numpy
import pygame

from pygame import Vector3, Vector2
import math


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


# base code~
def ortho_matrix(left, right, bottom, top, near_val, far_val):
    res = numpy.identity(4, dtype=numpy.float32)
    res.itemset((0, 0), float(2 / (right - left)))
    res.itemset((1, 1), float(2 / (top - bottom)))
    res.itemset((2, 2), float(-2 / (far_val - near_val)))

    t_x = -(right + left) / (right - left)
    t_y = -(top + bottom) / (top - bottom)
    t_z = -(far_val + near_val) / (far_val - near_val)
    res.itemset((0, 3), float(t_x))
    res.itemset((1, 3), float(t_y))
    res.itemset((2, 3), float(t_z))

    return res


# base code~
def perspective_matrix(fovy, aspect, z_near, z_far):
    f = 1 / math.tan(fovy / 2)
    res = numpy.identity(4, dtype=numpy.float32)
    res.itemset((0, 0), f / aspect)
    res.itemset((1, 1), f)
    res.itemset((2, 2), (z_far + z_near) / (z_near - z_far))
    res.itemset((3, 2), (2 * z_far * z_near) / (z_near - z_far))
    res.itemset((2, 3), -1)
    res.itemset((3, 3), 0)
    return res


# base code~
def get_matrix_looking_at(eye_xyz, target_xyz, up_vec):
    n = eye_xyz - target_xyz
    n.scale_to_length(1)
    u = up_vec.cross(n)
    v = n.cross(u)
    res = numpy.array([[u[0], u[1], u[2], (-u).dot(eye_xyz)],
                       [v[0], v[1], v[2], (-v).dot(eye_xyz)],
                       [n[0], n[1], n[2], (-n).dot(eye_xyz)],
                       [0, 0, 0, 1]], dtype=numpy.float32)
    return res


class Camera3D:

    def __init__(self):
        self.position = Vector3(0, 0, 0)
        self.direction: Vector3 = Vector3(0, 0, 1)
        self.up: Vector3 = Vector3(0, -1, 0)
        self.fov_degrees: float = 45  # vertical field of view

    def __repr__(self):
        return "{}(pos={}, dir={})".format(type(self).__name__, self.position, self.direction)

    def xform_pt(self, surface_size, pt: Vector3) -> Vector2:
        view_mat = get_matrix_looking_at(self.position, self.position + self.direction, self.up)
        proj_mat = perspective_matrix(self.fov_degrees / 180 * math.pi, surface_size[0] / surface_size[1], 0.5, 100000)
        world_v = numpy.array([pt[0], pt[1], pt[2], 1], dtype=numpy.float32)
        screen_v = proj_mat @ view_mat @ world_v

        if screen_v[3] == 0:
            # not sure what this means, but it's not good
            return None
        x = screen_v[0] / screen_v[3]
        y = screen_v[1] / screen_v[3]
        z = screen_v[2] / screen_v[3]
        if z < 0:
            # means point is "behind" the camera
            return None
        else:
            return Vector2(surface_size[0] // 2 + surface_size[0] * x,
                           surface_size[1] // 2 + surface_size[1] * y)

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

    screen = pygame.display.set_mode((600, 300), pygame.RESIZABLE)

    clock = pygame.time.Clock()

    camera = Camera3D()
    camera.position = Vector3(0, 0, -50)
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
                elif e.key == pygame.K_i:
                    print("camera = " + str(camera))

        keys_held = pygame.key.get_pressed()
        if keys_held[pygame.K_LEFT] or keys_held[pygame.K_RIGHT]:
            xz = Vector2(camera.direction.x, camera.direction.z)
            xz = xz.rotate(1 * (1 if keys_held[pygame.K_LEFT] else -1))
            camera.direction.x = xz[0]
            camera.direction.z = xz[1]
            camera.direction.scale_to_length(1)

        if keys_held[pygame.K_UP] or keys_held[pygame.K_DOWN]:
            camera.direction.y += 0.01 * (1 if keys_held[pygame.K_UP] else -1)
            camera.direction.scale_to_length(1)

        ms = 0.25
        xz = Vector2(camera.position.x, camera.position.z)
        view_xz = Vector2(camera.direction.x, camera.direction.z)
        view_xz.scale_to_length(1)

        if keys_held[pygame.K_a]:
            xz = xz + ms * view_xz.rotate(90)
        if keys_held[pygame.K_d]:
            xz = xz + ms * view_xz.rotate(-90)
        if keys_held[pygame.K_w]:
            xz = xz + ms * view_xz
        if keys_held[pygame.K_s]:
            xz = xz + ms * view_xz.rotate(180)
        camera.position.x = xz[0]
        camera.position.z = xz[1]

        screen.fill((0, 0, 0))

        angle += 1
        lines = gen_cube(angle, 10, Vector3(0, 0, 20))

        lines_2d = camera.project_to_surface(screen, lines)
        for l in lines_2d:
            pygame.draw.line(screen, l.color, l.p1, l.p2, l.width)

        pygame.display.update()
        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(60)

