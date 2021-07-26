import pygame
import time

import utility_functions


class Player:
    def __init__(self, level_data=None, x=0, y=0, z=-500):
        self.x = x
        self.y = y
        self.z = z
        # self.display = display
        self.lane = 0
        self.speed = 1
        self.level_data = level_data  # to be used when checking for collisions
        self.dy = 0
        self.modes = ['run', 'jump', 'slide']
        self.current_mode = self.modes[0]
        self.jumping = False
        self.sliding = False
        self.collided = False

    def set_mode(self, mode):
        if mode in self.modes:
            self.current_mode = mode

    def move_left(self):
        # cannot switch lanes while jumping
        if self.jumping:
            return
        self.lane -= 1
        self.lane %= 6

    def move_right(self):
        # cannot switch lanes while jumping
        if self.jumping:
            return
        self.lane += 1
        self.lane %= 6

    def move_forward(self):
        # supposed to happen per frame
        self.z += self.speed

    def run(self):
        self.set_mode('run')

    def jump(self):
        if self.jumping:
            return
        self.set_mode('jump')
        self.jumping = True
        self.dy = 10

    def slide(self):
        if self.jumping:
            return
        self.set_mode('slide')

    def handle_events(self, events):
        if events is None:
            return
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE or e.key == pygame.K_UP:
                    self.jump()
                if e.key == pygame.K_LEFT:
                    self.move_left()
                if e.key == pygame.K_RIGHT:
                    self.move_right()
                if e.key == pygame.K_DOWN:
                    self.slide()
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_DOWN:
                    self.sliding = False
                    self.set_mode('run')

    def update(self, events=None):
        self.y += self.dy
        if self.y > 0:
            self.dy -= 0.5
        if self.y < 0:
            self.y = 0
            self.dy = 0
            self.jumping = False
            if not self.current_mode == 'slide':
                self.set_mode('run')
        self.move_forward()
        self.handle_events(events)

    def draw(self, display):
        # draw info to display
        utility_functions.Text(display, 'X : ' + str(self.x) + ' | OPTIONAL', 50, 150, 25).draw()
        utility_functions.Text(display, 'Y : ' + str(self.y), 50, 200, 25).draw()
        utility_functions.Text(display, 'Z : ' + str(int(self.z)), 50, 250, 25).draw()
        utility_functions.Text(display, 'LANE : ' + str(self.lane), 50, 300, 25).draw()
        utility_functions.Text(display, 'MODE : ' + self.current_mode, 550, 50, 25).draw()
        # print(self.collided)
        if self.collided:
            utility_functions.Text(display, 'COLLIDED', 550, 100, 25).draw()
