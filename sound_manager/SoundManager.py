# not that currently some of the code is exclusively for defender but that part is not omitted yet
# because sometimes we need to have constantly looping sounds, instead of playing only once when events are triggered
# for example in this case ship_movement.ogg needs to constantly play when there is any movement
# but laser.ogg needs to play only once every bullet is launched

import pygame
import util.utility_functions as utils
import os
import traceback
import config
import random


class SoundManager:

    # Class for Sound management
    # stereo sound, but single channel playing [like original arcade machines]

    SOUND_PATHS = {
        'death': 'assets/sounds/death',
        'jump': 'assets/sounds/jump',
        'kill': 'assets/sounds/kill',
        'accept': 'assets/sounds/accept',
        'blip': 'assets/sounds/blip',
        'blip2': 'assets/sounds/blip2'
    }
    PRIORITIES = ['accept', 'death', 'jump', 'kill', 'blip2', 'blip']

    LOADED_SOUNDS = {}

    CURRENT_SOUND_ID: str = None
    CHANNEL: pygame.mixer.Channel = None

    @classmethod
    def init(cls):
        print("INFO: initializing pygame.mixer...")
        pygame.mixer.init()
        print("INFO: done.")

        cls.CHANNEL = pygame.mixer.Channel(1)

        print("INFO: loading sound effects...")
        cnt = 0
        for sound_id in cls.SOUND_PATHS:
            cls.LOADED_SOUNDS[sound_id] = []
            try:
                path_to_sounds = utils.resource_path(cls.SOUND_PATHS[sound_id])
                for filename in os.listdir(path_to_sounds):
                    if filename.endswith(".wav") or filename.endswith(".ogg"):
                        full_path = utils.resource_path(path_to_sounds + "/" + filename)
                        cls.LOADED_SOUNDS[sound_id].append(pygame.mixer.Sound(full_path))
                        cnt += 1
            except Exception:
                print("INFO: error while loading sound effects: {}".format(sound_id))
                traceback.print_exc()
        print("INFO: loaded {} sound effect(s).".format(cnt))

    @classmethod
    def play(cls, sound_id):
        if not config.ENABLE_SOUND_EFFECTS:
            return False

        volume = min(1.0, config.SOUND_EFFECTS_VOLUME * config.MASTER_VOLUME)
        if volume <= 0:
            return False

        if sound_id is None or sound_id not in cls.LOADED_SOUNDS or len(cls.LOADED_SOUNDS[sound_id]) == 0:
            return False
        if cls.CHANNEL.get_busy():
            if cls.should_interrupt(sound_id, cls.CURRENT_SOUND_ID):
                cls.CHANNEL.stop()
            else:
                return False
        sound_to_play = random.choice(cls.LOADED_SOUNDS[sound_id])
        sound_to_play.set_volume(volume)
        cls.CHANNEL.play(sound_to_play, loops=0)
        return True

    @classmethod
    def stop(cls):
        if cls.CHANNEL.get_busy():
            cls.CHANNEL.stop()

    @classmethod
    def should_interrupt(cls, new_sound, old_sound):
        if new_sound is None or new_sound not in cls.PRIORITIES:
            return False
        elif old_sound is None or old_sound not in cls.PRIORITIES:
            return True
        else:
            return cls.PRIORITIES.index(new_sound) <= cls.PRIORITIES.index(old_sound)
