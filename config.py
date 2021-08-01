import pygame
import json
import pathlib
import traceback


class Display:
    fps = 60
    width = 960
    height = 540
    title = "TEMPEST RUN"
    camera_bob = True
    use_player_art = True


class FontSize:
    # These are normalized to a display height of 540 px
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


_default_configs = {
    "Display": {
        "fps": 60,
        "width": 960,
        "height": 540,
        "title": "TEMPEST RUN",
        "camera_bob": True,
        "use_player_art": True
        },

    "FontSize": {
        "title": 64,
        "option": 36,
        "info": 24,
        "score": 30
        },

    "Music": {
        "enabled": True,
        "volume": 0.4
        },

    "Sound": {
        "enabled": True,
        "volume": 0.4
        },

    "Debug": {
        "use_neon": True,
        "testmode": False
        },

    "KeyBinds": {
        "Game": {
            "jump": [pygame.K_w, pygame.K_UP, pygame.K_SPACE],
            "left": [pygame.K_a, pygame.K_LEFT],
            "right": [pygame.K_d, pygame.K_RIGHT],
            "slide": [pygame.K_s, pygame.K_DOWN],
            "reset": [pygame.K_r]
            },

        "Menu": {
            "up": [pygame.K_w, pygame.K_UP],
            "down": [pygame.K_s, pygame.K_DOWN],
            "right" : [pygame.K_d, pygame.K_RIGHT],
            "left" : [pygame.K_a, pygame.K_LEFT],
            "accept": [pygame.K_RETURN, pygame.K_SPACE],
            "cancel": [pygame.K_ESCAPE]
            },

        "Toogle": {
            "neon": [pygame.K_n],
            "profiler": [pygame.K_F1]
            }
        }
    }


def _apply_configs_from_json(configuration):
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


_apply_configs_from_json(_default_configs)  # initialize configs to defaults


def _get_configs_as_json_dict():
    configuration = json.loads(json.dumps(_default_configs))  # making a new copy
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

    return configuration


def load_configs_from_disk():
    _apply_configs_from_json(_default_configs)
    path = pathlib.Path("config.json")
    try:
        if path.exists():
            with open(path, "r") as f:
                _apply_configs_from_json(json.load(f))
            print("INFO: loaded configs from: {}".format(path))
    except Exception:
        print("ERROR: failed to load configs from: {}".format(path))
        traceback.print_exc()


def save_configs_to_disk():
    path = pathlib.Path("config.json")
    try:
        if not path.exists():
            path.touch()
        as_json_dict = _get_configs_as_json_dict()
        with open(path, "w") as f:
            json.dump(as_json_dict, f, indent="  ")
        print("INFO: saved configs to: {}".format(path))
    except Exception:
        print("ERROR: failed to save configs to: {}".format(path))
        traceback.print_exc()
