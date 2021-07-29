import math
from typing import Union
import pygame
import time
import sys, os, pathlib
# import config

pygame.init()


def distance(p1: Union[tuple, list], p2: Union[tuple, list]) -> float:
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def get_display_resolution():# -> tuple[int, int]:
    display_width: int = pygame.display.Info().current_w
    display_height: int = pygame.display.Info().current_h
    return display_width, display_height


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, str(pathlib.Path(relative_path)))


def lerp(a, v1, v2):
    """Linearly interpolates between v1 and v2 based on a's value (from 0 to 1)"""
    if a <= 0:
        return v1
    elif a >= 1:
        return v2
    else:
        return a * (v2 - v1) + v1


class SpriteSheet:
    def __init__(self, img_file_name: Union[str, pygame.Surface], sprite_qty, row, col, color_key=None, flipped=False, scale_factor=1):
        self.scale_factor = scale_factor
        self.is_flipped = flipped
        self.sheet = pygame.image.load(img_file_name) if type(img_file_name) is str else img_file_name
        self.row = row
        self.col = col
        self.w = self.sheet.get_width() // self.col
        self.h = self.sheet.get_height() // self.row
        self.color_key = color_key
        self.sprite_qty = sprite_qty
        self.sprites = []

    def get_sprite_at_pos(self, x, y):
        img = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        img.blit(self.sheet, (0, 0), pygame.Rect(x, y, self.w, self.h))
        img = pygame.transform.scale(img, (img.get_width() * self.scale_factor, img.get_height() * self.scale_factor))
        if self.color_key is not None:
            img.set_colorkey(self.color_key)
        if self.is_flipped:
            return pygame.transform.flip(img, True, False)
        else:
            return img

    def get_images(self):
        c = 0
        images = []
        for i in range(self.row * self.col):
            c += 1
            if c > self.sprite_qty:
                break
            sprite = self.get_sprite_at_pos((i % self.col) * self.w, i % self.row * self.h)
            images.append(sprite)
        return images


class Text:
    def __init__(self, display: pygame.Surface, msg, x=250, y=250, size=50, color=(255, 255, 255), font='courier', blink=False, centered=False):
        self.display = display
        self.msg = msg
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        text_font = pygame.font.Font(resource_path('assets/VectorBattle-e9XO.ttf'), self.size)
        self.text = text_font.render(self.msg, False, self.color)
        self.blink = blink
        self.blink_timer = time.time()
        self.visible = True
        self.centered = centered

    def draw(self):
        if self.blink:
            if time.time() - self.blink_timer >= 0.5:
                self.blink_timer = time.time()
                self.visible = not self.visible
        if self.visible:
            if self.centered:
                self.display.blit(self.text, self.text.get_rect(center=(self.x, self.y)))
            else:
                self.display.blit(self.text, self.text.get_rect(topleft=(self.x, self.y)))
