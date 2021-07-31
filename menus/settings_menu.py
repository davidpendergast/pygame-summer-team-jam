import pygame

import config
import keybinds
import rendering.neon as neon
import util.fonts as fonts
import main
from sound_manager.SoundManager import SoundManager


config.load_config()


class SettingsMenuMode(main.GameMode):

    def __init__(self, loop: main.GameLoop):
        super().__init__(loop)
        self.selected_option_idx = 0
        self.options = [
            ("music", config.Music.volume, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 5),
            ("sound", config.Sound.volume, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 5),
            ("fps", config.Display.fps, [30, 40, 50, 60, 70, 80, 90, 100, 110, 120], 3),
            ("display", (config.Display.width, config.Display.height), [(480, 270), (960, 540), (1820, 1080)], 2),
            ("exit", lambda: self.exit_pressed())
        ]

        self.title_font = fonts.get_font(config.FontSize.title)
        self.option_font = fonts.get_font(config.FontSize.option)

    def on_mode_start(self):
        SoundManager.play_song("menu_theme", fadein_ms=3000)

    def exit_pressed(self):
        SoundManager.play('blip2')
        config.save_config()
        self.loop.set_mode(main.MainMenuMode(self.loop))

    def update(self, dt, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in keybinds.MENU_UP:
                    SoundManager.play("blip")
                    self.selected_option_idx = (self.selected_option_idx - 1) % len(self.options)
                elif e.key in keybinds.MENU_DOWN:
                    SoundManager.play("blip")
                    self.selected_option_idx = (self.selected_option_idx + 1) % len(self.options)
                elif e.key in keybinds.MENU_ACCEPT:
                    SoundManager.play("accept")
                    if self.selected_option_idx == len(self.options) - 1:
                        self.options[self.selected_option_idx][1]()
                    else:
                        pass
                    return
                elif e.key in keybinds.MENU_CANCEL:
                    SoundManager.play("blip2")
                    self.exit_pressed()
                    return

    def draw_to_screen(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen_size = screen.get_size()
        title_surface = self.title_font.render('SETTINGS', True, neon.WHITE)

        title_size = title_surface.get_size()
        title_y = screen_size[1] // 3 - title_size[1] // 2
        screen.blit(title_surface, dest=(screen_size[0] // 2 - title_size[0] // 2,
                                         title_y))

        option_y = max(screen_size[1] // 2, title_y + title_size[1])
        for i in range(len(self.options)):
            option_text = self.options[i][0]
            is_selected = i == self.selected_option_idx
            color = neon.WHITE if not is_selected else neon.RED
            if i != len(self.options) - 1:
                text = f"{option_text.upper()}: {self.options[i][1]}"
                if self.options[i][1] != self.options[i][2][0]:
                    text = "<  " + text
                if self.options[i][1] != self.options[i][2][-1]:
                    text = text + "  >"
            else:
                text = option_text.upper()
            option_surface = self.option_font.render(text, True, color)
            option_size = option_surface.get_size()
            screen.blit(option_surface, dest=(screen_size[0] // 2 - option_size[0] // 2, option_y))
            option_y += option_size[1]
