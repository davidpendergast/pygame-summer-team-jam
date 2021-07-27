# not that currently some of the code is exclusively for defender but that part is not omitted yet
# because sometimes we need to have constantly looping sounds, instead of playing only once when events are triggered
# for example in this case ship_movement.ogg needs to constantly play when there is any movement
# but laser.ogg needs to play only once every bullet is launched

class SoundManager:
    # Class for Sound management
    # stereo sound, but single channel playing [like original arcade machines]
    # uses only the pygame.mixer main channel

    # CONSTANTS [in order of priority]
    sounds = {
        'ship': 'assets/sounds/ship_movement.ogg',
        'shoot': 'assets/sounds/laser.ogg',
    }

    CURRENT_SOUND = 'ship'

    @classmethod
    def load(cls, sound=None):
        if SoundManager.get_priority_override(sound):
            cls.CURRENT_SOUND = sound
            pygame.mixer.music.load(cls.sounds[sound])
            return True
        else:
            return False

    @staticmethod
    def play(sound=None):
        if sound is not None and sounds_status == 'ON':
            if SoundManager.load(sound):
                pygame.mixer.music.play()

    @classmethod
    def get_priority_override(cls, sound):
        sound_list = list(cls.sounds.keys())

        def compare(item1, item2, compare_type='greater_than'):
            if compare_type == 'greater_than':
                if item1 > item2:
                    return True
            else:
                if item1 >= item2:
                    return True
            return False

        comparison_type = 'greater_than' if sound == 'ship' else 'greater_than_or_equal_to'

        if compare(sound_list.index(sound), sound_list.index(cls.CURRENT_SOUND), comparison_type):
            return True
        else:
            if pygame.mixer.music.get_busy():
                return False
            else:
                return True
