import pygame

import main
import rendering.threedee as threedee
import rendering.levelbuilder3d as levelbuilder3d
import rendering.neon as neon


class MockGameplayMode(main.GameMode):

    def __init__(self, loop):
        super().__init__(loop)
        self.z = 0
        self.zspeed = 70  # per second
        self.camera = threedee.Camera3D()
        self.camera.position.y = -3
        self.camera_z_offset = -20

        self.section_length = 20
        self.n = 8
        self.radius = 10
        self.foresight = 15
        self.neon_renderer = neon.NeonRenderer()

    def update(self, dt, events):
        # if pygame.key.get_pressed()[pygame.K_UP]:
        self.z += dt * self.zspeed
        # elif pygame.key.get_pressed()[pygame.K_DOWN]:
        #   self.z -= dt * self.zspeed

        self.camera.position.z = self.z + self.camera_z_offset

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = -1

    def draw_to_screen(self, screen):
        screen.fill((0, 0, 0))
        all_lines = []
        z_i = self.z // self.section_length
        for i in range(self.foresight):
            all_lines.extend(levelbuilder3d.build_section((i + z_i) * self.section_length, self.section_length, self.n,
                                                          self.radius, 0))

        for i in range(self.foresight):
            for lane_n in range(self.n):
                if (z_i + i + lane_n) % 7 == 0:
                    all_lines.extend(levelbuilder3d.build_rect((i + z_i) * self.section_length, self.section_length, self.n,
                                                               self.radius, 0, lane_n, 0.5, neon.RED, 1, with_x=True))
        all_2d_lines = self.camera.project_to_surface(screen, all_lines)
        neon_lines = neon.NeonLine.convert_line2ds_to_neon_lines(all_2d_lines)

        self.neon_renderer.draw_lines(screen, neon_lines)
