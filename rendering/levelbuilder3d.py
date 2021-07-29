from typing import List
from pygame import Vector3
import rendering.threedee as threedee
import rendering.neon as neon
import util.utility_functions as utility_functions


def get_ring_points(z, level) -> List[Vector3]:
    n = level.number_of_lanes()
    radius = level.get_radius(z)
    rotation = level.get_rotation(z)
    res = []
    for i in range(n):
        p = Vector3(radius, 0, z)
        p.rotate_ip(i * 360 / n + rotation, Vector3(0, 0, 1))
        res.append(p)
    return res


def build_section(z, length, level) -> List[threedee.Line3D]:
    ground_lines = []
    near_ring = get_ring_points(z, level)
    far_ring = get_ring_points(z + length, level)

    for i in range(level.number_of_lanes()):
        ground_lines.append(threedee.Line3D(near_ring[i], far_ring[i], color=neon.BLUE))
        ground_lines.append(threedee.Line3D(far_ring[i], far_ring[i - 1], color=neon.BLUE))

    return ground_lines


def build_obstacle(obs, level) -> List[threedee.Line3D]:
    return align_shape_to_level_surface(obs.get_model(),
                                        obs.z,
                                        obs.z + obs.length,
                                        obs.lane,
                                        level,
                                        obs.should_squeeze())


def build_rect(z_start, length, level, lane_n, hover_height, color, width, with_x=False) -> List[threedee.Line3D]:
    """Builds a 3D rectangle lying flat against the surface of the level."""
    near_ring = get_ring_points(z_start, level)
    far_ring = get_ring_points(z_start + length, level)
    corners = [near_ring[lane_n % level.number_of_lanes()],
               near_ring[(lane_n - 1) % level.number_of_lanes()],
               far_ring[(lane_n - 1) % level.number_of_lanes()],
               far_ring[lane_n % level.number_of_lanes()]]

    # make the rect hover a bit
    inset_corners = []
    for c in corners:
        hover_offset = Vector3(-c[0], -c[1], 0)
        hover_offset.scale_to_length(hover_height)
        inset_corners.append(c + hover_offset)

    res = [
        threedee.Line3D(inset_corners[0], inset_corners[1], color=color, width=width),
        threedee.Line3D(inset_corners[1], inset_corners[2], color=color, width=width),
        threedee.Line3D(inset_corners[2], inset_corners[3], color=color, width=width),
        threedee.Line3D(inset_corners[3], inset_corners[0], color=color, width=width)
    ]

    if with_x:
        res.append(threedee.Line3D(inset_corners[0], inset_corners[2], color=color, width=width))
        res.append(threedee.Line3D(inset_corners[1], inset_corners[3], color=color, width=width))

    return res


def get_player_shape_at_origin(player) -> List[threedee.Line3D]:
    # TODO add cool outline graphic
    # for now it's just a square
    width = 0.5 if not player.is_sliding() else 0.6
    height = 0.4 if not player.is_sliding() else 0.2
    dist_from_ground = 0.3 * player.y / player.max_jump_height()
    color = neon.YELLOW if not player.is_dead() else neon.RED
    top_left = Vector3(-width / 2.0, height + dist_from_ground, 0)
    top_right = Vector3(width / 2.0, height + dist_from_ground, 0)
    bot_left = Vector3(-width / 2.0, dist_from_ground, 0)
    bot_right = Vector3(width / 2.0, dist_from_ground, 0)

    return [threedee.Line3D(top_left, top_right, color=color, width=2),
            threedee.Line3D(top_right, bot_right, color=color, width=2),
            threedee.Line3D(bot_right, bot_left, color=color, width=2),
            threedee.Line3D(bot_left, top_left, color=color, width=2)]


def get_player_shape(player, level) -> List[threedee.Line3D]:
    shape_2d = get_player_shape_at_origin(player)
    return align_shape_to_level_surface(shape_2d, player.z, player.z, player.lane, level, squeeze=False)


def align_shape_to_level_surface(lines_to_xform: List[threedee.Line3D], z_start: float, z_end: float, lane_n: int, level, squeeze=False) -> List[threedee.Line3D]:
    """
    :param lines_to_xform: the shape to transform
    :param z_start: z position of the object in the level
    :param z_end: end z position of the object in the level
    :param lane_n: lane the object is in
    :param squeeze: whether the object should be "squeezed" inward as it approaches the center of the level
                    (this is needed for things like walls that should meet each other cleanly at their boundaries).
    :return: a new set of Line3Ds, aligned to the level
    """
    if z_start == z_end:
        z_end += 0.001

    near_ring_pts = get_ring_points(z_start, level)
    far_ring_pts = get_ring_points(z_end, level)

    near_left = near_ring_pts[(lane_n - 1) % level.number_of_lanes()]
    near_right = near_ring_pts[lane_n % level.number_of_lanes()]
    near_top = Vector3(0, 0, z_start)
    near_bottom = (near_left + near_right) / 2

    near_normal_vec = near_top - near_bottom
    near_normal_vec.scale_to_length(1)

    far_left = far_ring_pts[(lane_n - 1) % level.number_of_lanes()]
    far_right = far_ring_pts[lane_n % level.number_of_lanes()]
    far_top = Vector3(0, 0, z_end)
    far_bottom = (far_left + far_right) / 2

    far_normal_vec = far_top - far_bottom
    far_normal_vec.scale_to_length(1)

    res = []

    def convert_pt(pt):
        z_factor = utility_functions.map_from_interval_to_interval(pt.z, [-1, 1], [0, 1])
        vert_factor = pt.y
        horz_factor = utility_functions.map_from_interval_to_interval(pt.x, [-1, 1], [0, 1])

        if not squeeze:
            near_pt = near_left + horz_factor * (near_right - near_left) + vert_factor * (near_top - near_bottom)
            far_pt = far_left + horz_factor * (far_right - far_left) + vert_factor * (far_top - far_bottom)
            return utility_functions.lerp(z_factor, near_pt, far_pt)
        else:
            near_pt = utility_functions.lerp(vert_factor, near_left + horz_factor * (near_right - near_left), near_top)
            far_pt = utility_functions.lerp(vert_factor, far_left + horz_factor * (far_right - far_left), far_top)
            return utility_functions.lerp(z_factor, near_pt, far_pt)

    for l in lines_to_xform:
        new_p1 = convert_pt(l.p1)
        new_p2 = convert_pt(l.p2)
        res.append(threedee.Line3D(new_p1, new_p2, color=l.color, width=l.width))

    return res
