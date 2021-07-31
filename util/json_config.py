import json
import pathlib
import config


_default_config_str = """
{
    "Display": {
        "fps": 60
        "width": 960
        "height": 540
        "title": "TEMPEST RUN"
        "camera_bob": True
        "use_player_art": True
        }

    "FontSize": {
        "title": 64
        "option": 36
        "info": 24
        "score": 30
        }

    "Music": {
        "enabled": False
        "volume": 0.4
        }

    "Sound": {
        "enabled": True
        "volume": 0.2
        }

    "Debug": {
        "use_neon": True
        "testmode": False
        }

    "KeyBinds": {
        "Game": {
            "jump": [pygame.K_w, pygame.K_UP, pygame.K_SPACE]
            "left": [pygame.K_a, pygame.K_LEFT]
            "right": [pygame.K_d, pygame.K_RIGHT]
            "slide": [pygame.K_s, pygame.K_DOWN]
            "reset": [pygame.K_r]
            }

        "Menu": {
            "up": [pygame.K_w, pygame.K_UP]
            "down": [pygame.K_s, pygame.K_DOWN]
            "accept": [pygame.K_RETURN, pygame.K_SPACE]
            "cancel": [pygame.K_ESCAPE]
            }

        "Toogle": {
            "neon": [pygame.K_n]
            "profiler": [pygame.K_F1]
            }
        }
}
"""


class Foo:
    pass


def load_config():
    path = pathlib.Path("config.json")
    if not path.exists():
        path.touch()
    path.write_text(_default_config_str)
    configuration = json.loads(_default_config_str)
    config.Display.fps = configuration["Display"]["fps"]
    config.Display.width = configuration["Display"]["width"]
    config.Display.height = configuration["Display"]["height"]
    config.Display.title = configuration["Display"]["title"]
    config.Display.camera_bob = configuration["Display"]["camera_bob"]
    config.Display.use_player_art = configuration["Display"]["use_player_art"]
    config.FontSize.title = configuration["FontSize"]["title"]
    config.FontSize.option = configuration["FontSize"]["option"]
    config.FontSize.info = configuration["FontSize"]["info"]
    config.FontSize.score = configuration["FontSize"]["score"]
    config.Music.enabled = configuration["Music"]["enabled"]
    config.Music.volume = configuration["Music"]["volume"]
    config.Sound.enabled = configuration["Sound"]["enabled"]
    config.Sound.volume = configuration["Sound"]["volume"]
    config.Debug.use_neon = configuration["Debug"]["use_neon"]
    config.Debug.testmode = configuration["Debug"]["testmode"]
    config.KeyBinds.Game.jump = configuration["KeyBinds"]["Game"]["jump"]
    config.KeyBinds.Game.left = configuration["KeyBinds"]["Game"]["left"]
    config.KeyBinds.Game.right = configuration["KeyBinds"]["Game"]["right"]
    config.KeyBinds.Game.slide = configuration["KeyBinds"]["Game"]["slide"]
    config.KeyBinds.Game.reset = configuration["KeyBinds"]["Game"]["reset"]
    config.KeyBinds.Menu.up = configuration["KeyBinds"]["Menu"]["up"]
    config.KeyBinds.Menu.down = configuration["KeyBinds"]["Menu"]["down"]
    config.KeyBinds.Menu.accept = configuration["KeyBinds"]["Menu"]["accept"]
    config.KeyBinds.Menu.cancel = configuration["KeyBinds"]["Menu"]["cancel"]
    config.KeyBinds.Toogle.neon = configuration["KeyBinds"]["Toogle"]["neon"]
    config.KeyBinds.Toogle.profiler = configuration["KeyBinds"]["Toogle"]["profiler"]


def save_config():
    path = pathlib.Path("config.json")
    if not path.exists():
        path.touch()
    configuration = json.loads(_default_config_str)
    configuration["Display"]["fps"] = config.Display.fps
    configuration["Display"]["width"] = config.Display.width
    configuration["Display"]["height"] = config.Display.height
    configuration["Display"]["title"] = config.Display.title
    configuration["Display"]["camera_bob"] = config.Display.camera_bob
    configuration["Display"]["use_player_art"] = config.Display.use_player_art
    configuration["FontSize"]["title"] = config.FontSize.title
    configuration["FontSize"]["option"] = config.FontSize.option
    configuration["FontSize"]["info"] = config.FontSize.info
    configuration["FontSize"]["score"] = config.FontSize.score
    configuration["Music"]["enabled"] = config.Music.enabled
    configuration["Music"]["volume"] = config.Music.volume
    configuration["Sound"]["enabled"] = config.Sound.enabled
    configuration["Sound"]["volume"] = config.Sound.volume
    configuration["Debug"]["use_neon"] = config.Debug.use_neon
    configuration["Debug"]["testmode"] = config.Debug.testmode
    configuration["KeyBinds"]["Game"]["jump"] = config.KeyBinds.Game.jump
    configuration["KeyBinds"]["Game"]["left"] = config.KeyBinds.Game.left
    configuration["KeyBinds"]["Game"]["right"] = config.KeyBinds.Game.right
    configuration["KeyBinds"]["Game"]["slide"] = config.KeyBinds.Game.slide
    configuration["KeyBinds"]["Game"]["reset"] = config.KeyBinds.Game.reset
    configuration["KeyBinds"]["Menu"]["up"] = config.KeyBinds.Menu.up
    configuration["KeyBinds"]["Menu"]["down"] = config.KeyBinds.Menu.down
    configuration["KeyBinds"]["Menu"]["accept"] = config.KeyBinds.Menu.accept
    configuration["KeyBinds"]["Menu"]["cancel"] = config.KeyBinds.Menu.cancel
    configuration["KeyBinds"]["Toogle"]["neon"] = config.KeyBinds.Toogle.neon
    configuration["KeyBinds"]["Toogle"]["profiler"] = config.KeyBinds.Toogle.profiler
    configuration.dump("config.json")
