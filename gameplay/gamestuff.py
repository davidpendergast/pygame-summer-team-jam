import pygame

import main
import gameplay.player2d as player2d
import gameplay.levels as levels
import rendering.neon as neon
import rendering.threedee as threedee
import rendering.levelbuilder3d as levelbuilder3d


class GameplayMode(main.GameMode):

    def __init__(self, loop):
        super().__init__(loop)
        self.player = player2d.Player()
        self.current_level = levels.InfiniteGeneratingLevel(9)

        self.camera = threedee.Camera3D()
        self.camera.position.y = -3
        self.camera_z_offset = -20
        self.unload_offset = -30

        self.foresight = 150
        self.neon_renderer = neon.NeonRenderer()

    def update(self, dt, events):
        cur_z = self.player.z
        self.player.set_speed(self.current_level.get_player_speed(cur_z))
        self.player.update(dt, events)
        # TODO check for collisions and stuff

        self.camera.position.z = self.player.z + self.camera_z_offset
        self.current_level.unload_obstacles(self.camera.position.z + self.unload_offset)

    def draw_to_screen(self, screen):
        all_lines = []
        cell_length = self.current_level.get_cell_length()
        z = self.camera.position.z
        n_lanes = self.current_level.number_of_lanes()
        radius = self.current_level.get_radius(z)
        rotation = self.current_level.get_rotation(z)
        cell_start = int(z / cell_length)
        cell_end = int((z + self.foresight) / cell_length + 1)

        for i in range(cell_start, cell_end):
            all_lines.extend(levelbuilder3d.build_section(i * cell_length, cell_length, n_lanes, radius, 0))

        for n in range(n_lanes):
            obstacles = self.current_level.get_all_obstacles_between(n, z, z + self.foresight)
            for obs in reversed(obstacles):
                # add them from from back to front so they overlap properly
                all_lines.extend(levelbuilder3d.build_obstacle(obs, n_lanes, radius, rotation))

        all_2d_lines = self.camera.project_to_surface(screen, all_lines)
        neon_lines = neon.NeonLine.convert_line2ds_to_neon_lines(all_2d_lines)

        self.neon_renderer.draw_lines(screen, neon_lines)
