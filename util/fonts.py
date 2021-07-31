import pygame
import time
import util.utility_functions as utils

_CACHED_FONTS = {}  # (size: int, bold: bool, font_name: str) -> Font

_FONT_PATHS = {
    "lame": "assets/fonts/CONSOLA.TTF",
    "lame_bold": "assets/fonts/CONSOLAB.TTF",
    "cool": "assets/fonts/VectorBattle.ttf",
    "blocky": "assets/fonts/EightBit Atari-Ascprin.ttf"
}


def get_font(size, name="lame", bold=False):
    if bold:
        name = name + "_bold"
    if name not in _FONT_PATHS:
        name = "lame"
    key = (size, name)
    if key not in _CACHED_FONTS:
        raw_path = _FONT_PATHS[name]
        safe_path = utils.resource_path(raw_path)
        _CACHED_FONTS[key] = pygame.font.Font(safe_path, size)
    return _CACHED_FONTS[key]


def get_cool_font(size):
    key = (size, False, "cool")
    if key not in _CACHED_FONTS:
        safe_path = utils.resource_path(_path_to_cool_font)
        _CACHED_FONTS[key] = pygame.font.Font(safe_path, size)
    return _CACHED_FONTS[key]


class Text:
    def __init__(self, display: pygame.Surface, msg, x=250, y=250, size=50, color=(255, 255, 255), font='courier', blink=False, centered=False):
        self.display = display
        self.msg = msg
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.text = get_font(self.size, name="cool").render(self.msg, False, self.color)
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
