import pygame


class Display:
    fps = 60
    width = 960
    height = 540
    title = "TEMPEST RUN"
    camera_bob = True


class FontSize:
    title = 64
    option = 36
    info = 24
    score = 30


class Music:
    enabled = True
    volume = 0.4


class Sound:
    enabled = True
    volume = 0.2


class Debug:
    use_neon = True
    testmode = True


class KeyBinds:
    class Game:
        jump = [pygame.K_w, pygame.K_UP, pygame.K_SPACE]
        left = [pygame.K_a, pygame.K_LEFT]
        right = [pygame.K_d, pygame.K_RIGHT]
        slide = [pygame.K_s, pygame.K_DOWN]
        reset = [pygame.K_r]

    class Menu:
        up = [pygame.K_w, pygame.K_UP]
        down = [pygame.K_s, pygame.K_DOWN]
        accept = [pygame.K_RETURN, pygame.K_SPACE]
        cancel = [pygame.K_ESCAPE]

    class Toogle:
        neon = [pygame.K_n]
        profiler = [pygame.K_F1]
