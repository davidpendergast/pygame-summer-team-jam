import pygame
import keybinds

import util.utility_functions as utility_functions


class Player:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.lane = 0
        self.speed = 100  # units per second
        self.dy = 0
        self.modes = ['run', 'jump', 'slide']
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
        return self.collided

    def move_left(self):
        # cannot switch lanes while jumping
        # TODO feels pretty bad to not let you move while jumping, might want to change this
        if not self.is_jumping():
            self.lane -= 1
            self.lane %= 6

    def move_right(self):
        # cannot switch lanes while jumping
        # TODO feels pretty bad to not let you move while jumping, might want to change this
        if not self.is_jumping():
            self.lane += 1
            self.lane %= 6

    def move_forward(self, dt):
        # supposed to happen per frame
        self.z += self.speed * dt

    def run(self):
        self.set_mode('run')

    def jump(self):
        if not self.is_jumping():
            self.set_mode('jump')
            self.dy = 10

    def slide(self):
        if not self.is_jumping():
            self.set_mode('slide')

    def handle_events(self, events):
        if events is None:
            return
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
            if e.type == pygame.KEYUP:
                if e.key in keybinds.SLIDE:
                    self.set_mode('run')

    def update(self, dt, events=None):
        self.y += self.dy * dt
        if self.y > 0:
            self.dy -= 25 * dt
        if self.y < 0:
            self.y = 0
            self.dy = 0
            if not self.is_sliding():
                self.set_mode('run')
        self.move_forward(dt)
        self.handle_events(events)

    def draw(self, display):
        # draw info to display
        utility_functions.Text(display, 'X : ' + str(self.x) + ' | OPTIONAL', 50, 150, 25).draw()
        utility_functions.Text(display, 'Y : {:.2f}'.format(self.y), 50, 200, 25).draw()
        utility_functions.Text(display, 'Z : ' + str(int(self.z)), 50, 250, 25).draw()
        utility_functions.Text(display, 'LANE : ' + str(self.lane), 50, 300, 25).draw()
        utility_functions.Text(display, 'MODE : ' + self.current_mode, 550, 50, 25).draw()
        # print(self.collided)
        if self.collided:
            utility_functions.Text(display, 'COLLIDED', 550, 100, 25).draw()
