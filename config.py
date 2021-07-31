import pygame
import json
import pathlib


class Display:
    fps = 60
    width = 960
    height = 540
    title = "TEMPEST RUN"
    camera_bob = True
    use_player_art = True


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
    testmode = False


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
        right = [pygame.K_d, pygame.K_RIGHT]
        left = [pygame.K_a, pygame.K_LEFT]
        accept = [pygame.K_RETURN, pygame.K_SPACE]
        cancel = [pygame.K_ESCAPE]

    class Toogle:
        neon = [pygame.K_n]
        profiler = [pygame.K_F1]


_default_config_str = f"""
\u007b
    "Display": \u007b
        "fps": 60,
        "width": 960,
        "height": 540,
        "title": "TEMPEST RUN",
        "camera_bob": true,
        "use_player_art": true
        \u007d,

    "FontSize": \u007b
        "title": 64,
        "option": 36,
        "info": 24,
        "score": 30
        \u007d,

    "Music": \u007b
        "enabled": true,
        "volume": 0.4
        \u007d,

    "Sound": \u007b
        "enabled": true,
        "volume": 0.2
        \u007d,

    "Debug": \u007b
        "use_neon": true,
        "testmode": false
        \u007d,

    "KeyBinds": \u007b
        "Game": \u007b
            "jump": [{pygame.K_w}, {pygame.K_UP}, {pygame.K_SPACE}],
            "left": [{pygame.K_a}, {pygame.K_LEFT}],
            "right": [{pygame.K_d}, {pygame.K_RIGHT}],
            "slide": [{pygame.K_s}, {pygame.K_DOWN}],
            "reset": [{pygame.K_r}]
            \u007d,

        "Menu": \u007b
            "up": [{pygame.K_w}, {pygame.K_UP}],
            "down": [{pygame.K_s}, {pygame.K_DOWN}],
            "right" : [{pygame.K_d}, {pygame.K_RIGHT}],
            "left" : [{pygame.K_a}, {pygame.K_LEFT}],
            "accept": [{pygame.K_RETURN}, {pygame.K_SPACE}],
            "cancel": [{pygame.K_ESCAPE}]
            \u007d,

        "Toogle": \u007b
            "neon": [{pygame.K_n}],
            "profiler": [{pygame.K_F1}]
            \u007d
        \u007d
\u007d
"""


def load_config():
    path = pathlib.Path("config.json")
    if not path.exists():
        path.touch()
        path.write_text(_default_config_str)
    configuration = json.load(open(path, "r"))
    Display.fps = configuration["Display"]["fps"]
    Display.width = configuration["Display"]["width"]
    Display.height = configuration["Display"]["height"]
    Display.title = configuration["Display"]["title"]
    Display.camera_bob = configuration["Display"]["camera_bob"]
    Display.use_player_art = configuration["Display"]["use_player_art"]
    FontSize.title = configuration["FontSize"]["title"]
    FontSize.option = configuration["FontSize"]["option"]
    FontSize.info = configuration["FontSize"]["info"]
    FontSize.score = configuration["FontSize"]["score"]
    Music.enabled = configuration["Music"]["enabled"]
    Music.volume = configuration["Music"]["volume"]
    Sound.enabled = configuration["Sound"]["enabled"]
    Sound.volume = configuration["Sound"]["volume"]
    Debug.use_neon = configuration["Debug"]["use_neon"]
    Debug.testmode = configuration["Debug"]["testmode"]
    KeyBinds.Game.jump = configuration["KeyBinds"]["Game"]["jump"]
    KeyBinds.Game.left = configuration["KeyBinds"]["Game"]["left"]
    KeyBinds.Game.right = configuration["KeyBinds"]["Game"]["right"]
    KeyBinds.Game.slide = configuration["KeyBinds"]["Game"]["slide"]
    KeyBinds.Game.reset = configuration["KeyBinds"]["Game"]["reset"]
    KeyBinds.Menu.up = configuration["KeyBinds"]["Menu"]["up"]
    KeyBinds.Menu.down = configuration["KeyBinds"]["Menu"]["down"]
    KeyBinds.Menu.right = configuration["KeyBinds"]["Menu"]["right"]
    KeyBinds.Menu.left = configuration["KeyBinds"]["Menu"]["left"]
    KeyBinds.Menu.accept = configuration["KeyBinds"]["Menu"]["accept"]
    KeyBinds.Menu.cancel = configuration["KeyBinds"]["Menu"]["cancel"]
    KeyBinds.Toogle.neon = configuration["KeyBinds"]["Toogle"]["neon"]
    KeyBinds.Toogle.profiler = configuration["KeyBinds"]["Toogle"]["profiler"]


def save_config():
    path = pathlib.Path("config.json")
    if not path.exists():
        path.touch()
    configuration = json.loads(_default_config_str)
    configuration["Display"]["fps"] = Display.fps
    configuration["Display"]["width"] = Display.width
    configuration["Display"]["height"] = Display.height
    configuration["Display"]["title"] = Display.title
    configuration["Display"]["camera_bob"] = Display.camera_bob
    configuration["Display"]["use_player_art"] = Display.use_player_art
    configuration["FontSize"]["title"] = FontSize.title
    configuration["FontSize"]["option"] = FontSize.option
    configuration["FontSize"]["info"] = FontSize.info
    configuration["FontSize"]["score"] = FontSize.score
    configuration["Music"]["enabled"] = Music.enabled
    configuration["Music"]["volume"] = Music.volume
    configuration["Sound"]["enabled"] = Sound.enabled
    configuration["Sound"]["volume"] = Sound.volume
    configuration["Debug"]["use_neon"] = Debug.use_neon
    configuration["Debug"]["testmode"] = Debug.testmode
    configuration["KeyBinds"]["Game"]["jump"] = KeyBinds.Game.jump
    configuration["KeyBinds"]["Game"]["left"] = KeyBinds.Game.left
    configuration["KeyBinds"]["Game"]["right"] = KeyBinds.Game.right
    configuration["KeyBinds"]["Game"]["slide"] = KeyBinds.Game.slide
    configuration["KeyBinds"]["Game"]["reset"] = KeyBinds.Game.reset
    configuration["KeyBinds"]["Menu"]["up"] = KeyBinds.Menu.up
    configuration["KeyBinds"]["Menu"]["down"] = KeyBinds.Menu.down
    configuration["KeyBinds"]["Menu"]["accept"] = KeyBinds.Menu.accept
    configuration["KeyBinds"]["Menu"]["cancel"] = KeyBinds.Menu.cancel
    configuration["KeyBinds"]["Toogle"]["neon"] = KeyBinds.Toogle.neon
    configuration["KeyBinds"]["Toogle"]["profiler"] = KeyBinds.Toogle.profiler
    json.dump(configuration, open(path, "w"))
