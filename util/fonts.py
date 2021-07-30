import pygame
import time
import util.utility_functions as utils

_CACHED_FONTS = {}  # (size: int, bold: bool, font_name: str) -> Font

_path_to_lame_font = "assets/fonts/CONSOLA.TTF"
_path_to_lame_font_bold = "assets/fonts/CONSOLAB.TTF"
_path_to_cool_font = "assets/fonts/VectorBattle-e9XO.ttf"


def get_font(size, bold=False):
    key = (size, bold, "lame")
    if key not in _CACHED_FONTS:
        raw_path = _path_to_lame_font_bold if bold else _path_to_lame_font
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
        self.text = get_cool_font(self.size).render(self.msg, False, self.color)
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
