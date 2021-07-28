import math
import random

import pygame

import rendering.neon as neon
import keybinds
from main import GameMode, GameLoop


class HelpMenuMode(GameMode):

    def __init__(self, loop: GameLoop):
        super().__init__(loop)

        self.selected_option_idx = 0
        self.options = [
            ("goal", None),
            ("controls", None),
            ("sounds", None),
            ("back", None)
        ]
        self.squares = [[random.randint(0, 600), 300, random.randint(0, 360), random.randint(2, 10) / 2 * random.choice([-1, 1])] for _ in range(25)]  # format -> [x, y, angle, speed]

        self.title_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.option_font = pygame.font.Font(pygame.font.get_default_font(), 24)

    @staticmethod
    def get_square_points(x, y, angle, size=50):
        points = [
            [-size // 2, - size // 2],
            [size // 2, - size // 2],
            [size // 2, size // 2],
            [-size // 2, size // 2]
        ]
        points = [pygame.Vector2(i[0], i[1]).rotate(angle) for i in points]
        points = [[x + i[0], y + i[1]] for i in points]
        return points

    def on_mode_start(self):
        # TODO song
        pass

    def start_pressed(self):
        import gameplay.gamestuff  # shh don't tell pylint about this
        self.loop.set_next_mode(gameplay.gamestuff.GameplayMode(self.loop))

    def help_pressed(self):
        import gameplay.mockgamestuff
        self.loop.set_next_mode(gameplay.mockgamestuff.MockGameplayMode(self.loop))

    def credits_pressed(self):
        # TODO add credits menu
        pass

    def exit_pressed(self):
        self.loop.running = False

    def update(self, dt, events):
        for i in self.squares:
            i[2] += i[3]
            i[1] -= abs(i[3])
            if i[1] < -50:
                i[1] = 350
                i[0] = random.randint(0, 600)
                i[3] = random.randint(2, 10) / 2 * random.choice([-1, 1])
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in keybinds.LEFT:
                    # TODO play menu blip sound
                    self.selected_option_idx = (self.selected_option_idx - 1) % len(self.options)
                elif e.key in keybinds.RIGHT:
                    # TODO play menu blip sound
                    self.selected_option_idx = (self.selected_option_idx + 1) % len(self.options)
                elif e.key in keybinds.MENU_CANCEL:
                    self.exit_pressed()
                    return

    def draw_to_screen(self, screen):
        for i in self.squares:
            pygame.draw.lines(screen, (0, 255, 0), True, self.get_square_points(i[0], i[1], i[2]))
        screen_size = screen.get_size()
        title_surface = self.title_font.render('Help', False, neon.WHITE)

        title_size = title_surface.get_size()
        title_y = screen_size[1] // 4 - title_size[1] // 2
        screen.blit(title_surface, dest=(screen_size[0] // 2 - title_size[0] // 2,
                                         title_y))

        option_y = max(screen_size[1] // 2, title_y + title_size[1])
        msg = ''
        for i in range(len(self.options)):
            option_text = self.options[i][0]
            is_selected = i == self.selected_option_idx
            color = neon.WHITE if not is_selected else neon.RED
            if is_selected:
                if i == 0:
                    msg = 'objectives of the game'
                elif i == 1:
                    msg = 'keyboard controls'
                elif i == 2:
                    msg = 'how to turn sounds on or off'
                elif i == 3:
                    msg = 'Press ESCAPE to Go Back'
            option_surface = self.option_font.render(option_text, False, color)
            option_size = option_surface.get_size()
            screen.blit(option_surface, dest=((screen_size[0] // (len(self.options) + 1)) * (i + 1) - option_size[0] // 2, option_y))
            msg_surf = self.title_font.render(msg, False, neon.WHITE)
            screen.blit(msg_surf, msg_surf.get_rect(center=(screen_size[0] // 2, screen_size[1] * 2 / 3)))
