from typing import List
from pygame import Vector3
import rendering.threedee as threedee
import rendering.neon as neon


class PlayerState:

    def __init__(self, z, lane_n, height_from_floor, animation, color, x_in_lane=0):
        self.z = z
        self.x_in_lane = x_in_lane
        self.n = lane_n
        self.height_from_floor = height_from_floor
        self.animation = animation
        self.color = color


def get_ring_points(z, n, radius, rotation) -> List[Vector3]:
    res = []
    for i in range(n):
        p = Vector3(radius, 0, z)
        p.rotate_ip(i * 360 / n + rotation, Vector3(0, 0, 1))
        res.append(p)
    return res


def build_section(z, length, n, radius, rotation) -> List[threedee.Line3D]:
    ground_lines = []
    near_ring = get_ring_points(z, n, radius, rotation)
    far_ring = get_ring_points(z + length, n, radius, rotation)

    for i in range(n):
        ground_lines.append(threedee.Line3D(near_ring[i], far_ring[i], color=neon.BLUE))
        ground_lines.append(threedee.Line3D(far_ring[i], far_ring[i - 1], color=neon.BLUE))

    return ground_lines


def build_obstacle(obs, n, radius, rotation) -> List[threedee.Line3D]:
    # TODO get real model from obstacle and xform it
    return build_rect(obs.z, obs.length, n, radius, rotation, obs.lane, radius / 20, obs.color, 1,
                      with_x=not obs.can_slide_through())


def build_rect(z_start, length, n, radius, rotation, lane_n, hover_height, color, width, with_x=False) -> List[threedee.Line3D]:
    near_ring = get_ring_points(z_start, n, radius, rotation)
    far_ring = get_ring_points(z_start + length, n, radius, rotation)
    corners = [near_ring[lane_n], near_ring[lane_n - 1], far_ring[lane_n - 1], far_ring[lane_n]]

    # make the rect hover a bit
    inset_corners = []
    for c in corners:
        hover_offset = Vector3(-c[0], -c[1], 0)
        hover_offset.scale_to_length(hover_height)
        inset_corners.append(c + hover_offset)

    res = []
    res.append(threedee.Line3D(inset_corners[0], inset_corners[1], color=color, width=width))
    res.append(threedee.Line3D(inset_corners[1], inset_corners[2], color=color, width=width))
    res.append(threedee.Line3D(inset_corners[2], inset_corners[3], color=color, width=width))
    res.append(threedee.Line3D(inset_corners[3], inset_corners[0], color=color, width=width))

    if with_x:
        res.append(threedee.Line3D(inset_corners[0], inset_corners[2], color=color, width=width))
        res.append(threedee.Line3D(inset_corners[1], inset_corners[3], color=color, width=width))

    return res


