import pygame
import keybinds
from typing import List
from sound_manager.SoundManager import SoundManager

import util.fonts as fonts


class Player:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.length = 1  # how long the player is (affects collisions)
        self.lane = 0
        self.speed = 0  # units per second, this is mainly controlled
        self.dy = 0
        self.modes = ['run', 'jump', 'slide', 'dead']
        self.current_mode = self.modes[0]
        self.collided = False

    def set_mode(self, mode):
        if mode in self.modes:
            self.current_mode = mode

    def is_sliding(self):
        return self.current_mode == 'slide'

    def is_jumping(self):
        return self.current_mode == 'jump'

    def is_running(self):
        return self.current_mode == 'run'

    def is_dead(self):
        return self.current_mode == 'dead'

    def get_mode(self):
        return self.current_mode

    def move_left(self):
        if not self.is_jumping() and not self.is_dead():
            SoundManager.play('blip')
            self.lane -= 1

    def move_right(self):
        if not self.is_jumping() and not self.is_dead():
            SoundManager.play('blip')
            self.lane += 1

    def move_forward(self, dt):
        self.z += self.speed * dt

    def get_lane(self, total_lanes):
        return self.lane % total_lanes

    def run(self):
        self.set_mode('run')

    def jump(self):
        if not self.is_jumping():
            SoundManager.play('jump')
            self.set_mode('jump')
            self.dy = 10

    def max_jump_height(self):
        return 2.5  # TODO calulate this for real

    def slide(self):
        if self.is_running():
            self.set_mode('slide')

    def set_speed(self, speed):
        self.speed = speed

    def get_score(self):
        return int(self.z / 10) * 10

    def update(self, dt, level, events):
        self._handle_inputs(events)
        self._handle_collisions(level)
        if not self.is_dead():
            self.set_speed(level.get_player_speed(self.z))
            self._handle_movement(dt)

    def _handle_inputs(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in keybinds.JUMP:
                    self.jump()
                if e.key in keybinds.LEFT:
                    self.move_left()
                if e.key in keybinds.RIGHT:
                    self.move_right()
                if e.key in keybinds.SLIDE:
                    self.slide()
            elif e.type == pygame.KEYUP:
                if e.key in keybinds.SLIDE and self.is_sliding():
                    self.run()

    def _handle_movement(self, dt):
        self.y += self.dy * dt
        if self.y > 0:
            self.dy -= 25 * dt
        if self.y < 0:
            self.y = 0
            self.dy = 0
            if not self.is_sliding():
                self.set_mode('run')
        self.move_forward(dt)

    def _handle_collisions(self, level):
        if self.is_dead():
            return
        else:
            lane_n = self.get_lane(level.number_of_lanes())
            obstacles = level.get_all_obstacles_between(lane_n, self.z, self.z + self.length)
            for obs in obstacles:
                if obs.handle_potential_collision(self):
                    self.set_mode('dead')
                    SoundManager.play('death')
                    return

    def draw(self, display):
        # draw info to display
        fonts.Text(display, 'X : ' + str(self.x) + ' | OPTIONAL', 50, 150, 25).draw()
        fonts.Text(display, 'Y : {:.2f}'.format(self.y), 50, 200, 25).draw()
        fonts.Text(display, 'Z : ' + str(int(self.z)), 50, 250, 25).draw()
        fonts.Text(display, 'LANE : ' + str(self.lane), 50, 300, 25).draw()
        fonts.Text(display, 'MODE : ' + self.current_mode, 550, 50, 25).draw()
        # print(self.collided)
        if self.collided:
            fonts.Text(display, 'COLLIDED', 550, 100, 25).draw()


