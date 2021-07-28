import pygame
import time

import keybinds
import menus.help_menu
import rendering.neon as neon

TARGET_FPS = 60

# this is only the default size, use pygame.display.get_surface().get_size() to get the current size.
W, H = (600, 300)


class GameLoop:

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_mode: GameMode = MainMenuMode(self)
        self.next_mode = None

    def set_next_mode(self, next_mode):
        self.next_mode = next_mode

    def start(self):
        last_tick_time_secs = time.time()

        while self.running:
            events = []
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    print("INFO: quitting game")
                    self.running = False
                    return
                else:
                    # collect all the events so we can pass them into the current game mode.
                    events.append(e)

            if self.next_mode is not None:
                self.current_mode.on_mode_end()
                self.current_mode = self.next_mode
                self.current_mode.on_mode_start()

            cur_time = time.time()
            dt = cur_time - last_tick_time_secs

            self.current_mode.update(dt, events)
            last_tick_time_secs = cur_time

            screen = pygame.display.get_surface()
            screen.fill((0, 0, 0))
            self.current_mode.draw_to_screen(screen)

            pygame.display.flip()
            pygame.time.Clock().tick(TARGET_FPS)


class GameMode:

    def __init__(self, loop: GameLoop):
        self.loop: GameLoop = loop

    def on_mode_start(self):
        """Called when mode becomes active"""
        pass

    def on_mode_end(self):
        """Called when mode becomes inactive"""
        pass

    def update(self, dt, events):
        pass

    def draw_to_screen(self, screen):
        pass


class MainMenuMode(GameMode):

    def __init__(self, loop: GameLoop):
        super().__init__(loop)

        self.selected_option_idx = 0
        self.options = [
            ("start", lambda: self.start_pressed()),
            ("help", lambda: self.help_pressed()),
            ("credits", lambda: self.credits_pressed()),
            ("exit", lambda: self.exit_pressed())
        ]

        self.title_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.option_font = pygame.font.Font(pygame.font.get_default_font(), 24)

    def on_mode_start(self):
        # TODO song
        pass

    def start_pressed(self):
        import gameplay.gamestuff  # shh don't tell pylint about this
        self.loop.set_next_mode(gameplay.gamestuff.GameplayMode(self.loop))

    def help_pressed(self):
        import gameplay.mockgamestuff
        self.loop.set_next_mode(menus.help_menu.HelpMenuMode(self.loop))
        # self.loop.set_next_mode(gameplay.mockgamestuff.MockGameplayMode(self.loop))

    def credits_pressed(self):
        # TODO add credits menu
        pass

    def exit_pressed(self):
        self.loop.running = False

    def update(self, dt, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in keybinds.MENU_UP:
                    # TODO play menu blip sound
                    self.selected_option_idx = (self.selected_option_idx - 1) % len(self.options)
                elif e.key in keybinds.MENU_DOWN:
                    # TODO play menu blip sound
                    self.selected_option_idx = (self.selected_option_idx + 1) % len(self.options)
                elif e.key in keybinds.MENU_ACCEPT:
                    self.options[self.selected_option_idx][1]()  # activate the option's lambda
                    return
                elif e.key in keybinds.MENU_CANCEL:
                    self.exit_pressed()
                    return

    def draw_to_screen(self, screen):
        screen_size = screen.get_size()
        title_surface = self.title_font.render('Tempest Run', True, neon.WHITE)

        title_size = title_surface.get_size()
        title_y = screen_size[1] // 3 - title_size[1] // 2
        screen.blit(title_surface, dest=(screen_size[0] // 2 - title_size[0] // 2,
                                         title_y))

        option_y = max(screen_size[1] // 2, title_y + title_size[1])
        for i in range(len(self.options)):
            option_text = self.options[i][0]
            is_selected = i == self.selected_option_idx
            color = neon.WHITE if not is_selected else neon.RED

            option_surface = self.option_font.render(option_text, True, color)
            option_size = option_surface.get_size()
            screen.blit(option_surface, dest=(screen_size[0] // 2 - option_size[0] // 2, option_y))
            option_y += option_size[1]


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((W, H), pygame.SCALED)

    loop = GameLoop()
    loop.start()
