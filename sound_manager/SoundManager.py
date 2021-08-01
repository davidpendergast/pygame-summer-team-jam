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
import threading
import time


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

    SONG_PATHS = {
        "menu_theme": "assets/songs/menu_theme.ogg",
        "game_theme": "assets/songs/game_theme.ogg"
    }
    CURRENT_SONG_ID: str = None
    IS_FADING = False
    NEXT_SONG_AFTER_FADEOUT = None
    FADEOUT_LOCK = threading.Lock()
    SONG_VOLUME_MULTIPLIER = 1.0

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
        # print("INFO: trying to play: {}".format(sound_id))
        if not config.Sound.enabled:
            return False

        volume = min(1.0, config.Sound.volume)
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
        # print("INFO: played {}".format(sound_id))
        return True

    @classmethod
    def stop(cls):
        if cls.CHANNEL.get_busy():
            cls.CHANNEL.stop()

    @classmethod
    def set_song_volume_multiplier(cls, mult):
        cls.SONG_VOLUME_MULTIPLIER = mult
        cls.update_song_volume()

    @classmethod
    def get_song_volume(cls):
        return max(0, min(1, cls.SONG_VOLUME_MULTIPLIER * config.Music.volume))

    @classmethod
    def update_song_volume(cls):
        pygame.mixer.music.set_volume(cls.get_song_volume())

    @classmethod
    def play_song(cls, song_id, fadeout_ms=1000, fadein_ms=500):
        if not config.Music.enabled:
            return

        if song_id is not None and song_id not in cls.SONG_PATHS:
            print("WARN: unrecognized song id: {}".format(song_id))
            return

        cls.FADEOUT_LOCK.acquire()
        try:
            if cls.CURRENT_SONG_ID is None:
                # Easy case, no song is playing
                cls._play_song_immediately(song_id, fadein_ms)
            else:
                if cls.IS_FADING:
                    # We're alreading fading, just swap in the new song
                    cls.NEXT_SONG_AFTER_FADEOUT = song_id
                elif cls.CURRENT_SONG_ID == song_id:
                    # We're already playing the correct song; do nothing
                    pass
                else:
                    # We're playing a song already, but it's not the right one. Time to fade.
                    cls.IS_FADING = True
                    cls.NEXT_SONG_AFTER_FADEOUT = song_id
                    x = threading.Thread(target=SoundManager._do_async_fadeout, args=(fadeout_ms, fadein_ms))
                    x.start()
        finally:
            cls.FADEOUT_LOCK.release()

    @classmethod
    def _do_async_fadeout(cls, fadeout_ms, fadein_ms):
        # this is some base code from my engine~
        old_time_millis = int(round(time.time() * 1000))
        pygame.mixer.music.fadeout(fadeout_ms)
        cur_time_millis = int(round(time.time() * 1000))

        if cur_time_millis - old_time_millis < fadeout_ms:
            rem_time_millis = fadeout_ms - (cur_time_millis - old_time_millis)
            time.sleep(rem_time_millis / 1000.0)

        cls.FADEOUT_LOCK.acquire()
        try:
            cls.IS_FADING = False
            if cls.NEXT_SONG_AFTER_FADEOUT is None:
                pygame.mixer.music.stop()
                cls.CURRENT_SONG_ID = None
            else:
                cls._play_song_immediately(cls.NEXT_SONG_AFTER_FADEOUT, fadein_ms=fadein_ms)
                cls.NEXT_SONG_AFTER_FADEOUT = None
        finally:
            cls.FADEOUT_LOCK.release()

    @classmethod
    def _play_song_immediately(cls, song_id, fadein_ms):
        try:
            pygame.mixer.music.load(cls.SONG_PATHS[song_id])
            pygame.mixer.music.set_volume(cls.get_song_volume())
            pygame.mixer.music.play(loops=-1, fade_ms=fadein_ms)
            cls.CURRENT_SONG_ID = song_id
        except Exception:
            print("ERROR: failed to play song: {}".format(cls.SONG_PATHS[song_id]))
            cls.CURRENT_SONG_ID = None
            try:
                # if there's another song playing, try to stop it
                pygame.mixer.music.stop()
            except Exception:
                pass

    @classmethod
    def should_interrupt(cls, new_sound, old_sound):
        if new_sound is None or new_sound not in cls.PRIORITIES:
            return False
        elif old_sound is None or old_sound not in cls.PRIORITIES:
            return True
        else:
            return cls.PRIORITIES.index(new_sound) <= cls.PRIORITIES.index(old_sound)
