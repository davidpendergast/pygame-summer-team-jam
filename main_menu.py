import pygame

import gameplay.levels
import keybinds
import rendering.neon as neon
import config
import util.profiling as profiling
import util.fonts as fonts
from gameplay import player2d
from rendering import levelbuilder3d, threedee
from sound_manager.SoundManager import SoundManager
from util import utility_functions

TARGET_FPS = config.Display.fps if not config.Debug.testmode else -1

# this is only the default size, use pygame.display.get_surface().get_size() to get the current size.
W, H = config.Display.width, config.Display.height


class GameLoop:

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        self.current_mode = MainMenuMode(self)
        self.current_mode.on_mode_start()

    def set_mode(self, next_mode):
        if self.current_mode != next_mode:
            self.current_mode.on_mode_end()
        self.current_mode = next_mode
        self.current_mode.on_mode_start()

    def start(self):
        dt = 0
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

                # global keybinds
                if e.type == pygame.KEYDOWN:
                    if e.key in keybinds.TOGGLE_NEON:
                        config.Debug.use_neon = not config.Debug.use_neon
                        print("INFO: toggling neon to: {}".format(config.Debug.use_neon))
                    if e.key in keybinds.TOGGLE_PROFILER:
                        profiling.get_instance().toggle()
            cur_mode = self.current_mode

            cur_mode.update(dt, events)
            cur_mode.draw_to_screen(self.screen)

            pygame.display.flip()

            if config.Debug.testmode:
                pygame.display.set_caption(f"TEMPEST RUN {int(self.clock.get_fps())} FPS")

            dt = self.clock.tick(TARGET_FPS) / 1000.0


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
        self.song = pygame
        self.selected_option_idx = 0
        self.options = [
            ("start", lambda: self.start_pressed()),
            ("help", lambda: self.help_pressed()),
            ("credits", lambda: self.credits_pressed()),
            ("exit", lambda: self.exit_pressed())
        ]

        self.title_font = fonts.get_font(config.FontSize.title)
        self.option_font = fonts.get_font(config.FontSize.option)
        self.angle = 0
        self.neon_renderer = neon.NeonRenderer()
        self.camera = threedee.Camera3D()
        self.current_level = gameplay.levels.InfiniteGeneratingLevel(10)
        self.foresight = 150
        self.unload_offset = -30
        self.player = player2d.Player()

    def on_mode_start(self):
        SoundManager.play_song("menu_theme", fadein_ms=3000)

    def start_pressed(self):
        import gameplay.gamestuff  # shh don't tell pylint about this
        self.loop.set_mode(gameplay.gamestuff.GameplayMode(self.loop))

    def help_pressed(self):
        import menus.help_menu as help_menu
        self.loop.set_mode(help_menu.HelpMenuMode(self.loop, self))

    def credits_pressed(self):
        # TODO add credits menu
        import menus.credits_menu as credits_menu
        self.loop.set_mode(credits_menu.CreditsMenuMode(self.loop, self))

    def exit_pressed(self):
        self.loop.running = False

    def update(self, dt, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in keybinds.MENU_UP:
                    SoundManager.play("blip")
                    self.selected_option_idx = (self.selected_option_idx - 1) % len(self.options)
                    self.player.lane += 1
                elif e.key in keybinds.MENU_DOWN:
                    SoundManager.play("blip")
                    self.selected_option_idx = (self.selected_option_idx + 1) % len(self.options)
                    self.player.lane -= 1
                elif e.key in keybinds.MENU_ACCEPT:
                    SoundManager.play("accept")
                    self.options[self.selected_option_idx][1]()  # activate the option's lambda
                    return
                elif e.key in keybinds.MENU_CANCEL:
                    SoundManager.play("blip2")
                    self.exit_pressed()
                    return

    def update_level_rotation(self, snap=False):
        z = self.player.z
        ideal_rotation = levelbuilder3d.get_rotation_to_make_lane_at_bottom(z, self.player.lane, self.current_level)
        cur_rotation = self.current_level.get_rotation(z)
        dist, clockwise = utility_functions.abs_angle_between_angles(cur_rotation, ideal_rotation)
        if dist < 0.01 or snap:
            self.current_level.set_rotation(ideal_rotation)
        else:
            target_rots = [ideal_rotation - 360, ideal_rotation, ideal_rotation + 360]
            potential_rotations = [(t - cur_rotation) * 4 * 1 for t in target_rots]
            change_in_rotation = min(potential_rotations, key=abs)
            print(change_in_rotation)
            if abs(change_in_rotation) > dist:
                self.current_level.set_rotation(ideal_rotation)
                print('yo')
            else:
                self.current_level.set_rotation(cur_rotation + change_in_rotation)
                print('yo')

    def draw_to_screen(self, screen: pygame.Surface):
        self.camera.position.z += 1
        self.current_level.unload_obstacles(self.camera.position.z + self.unload_offset)
        self.angle += 0
        self.update_level_rotation(False)
        screen.fill((0, 0, 0))
        screen_size = screen.get_size()
        all_lines = []
        cell_length = 20
        z = self.camera.position.z
        cell_start = int(z / cell_length)
        cell_end = int((z + self.foresight) / cell_length + 1)

        for i in range(cell_start, cell_end):
            all_lines.extend(levelbuilder3d.build_section(i * cell_length, cell_length, self.current_level))

        all_2d_lines = self.camera.project_to_surface(screen, all_lines)
        neon_lines = neon.NeonLine.convert_line2ds_to_neon_lines(all_2d_lines)

        self.neon_renderer.draw_lines(screen, neon_lines, extra_darkness_factor=1)
        title_surface = self.title_font.render('TEMPEST RUN', True, neon.WHITE)

        title_size = title_surface.get_size()
        title_y = screen_size[1] // 3 - title_size[1] // 2
        screen.blit(title_surface, dest=(screen_size[0] // 2 - title_size[0] // 2,
                                         title_y))

        option_y = max(screen_size[1] // 2, title_y + title_size[1])
        for i in range(len(self.options)):
            option_text = self.options[i][0]
            is_selected = i == self.selected_option_idx
            color = neon.WHITE if not is_selected else neon.RED

            option_surface = self.option_font.render(option_text.upper(), True, color)
            option_size = option_surface.get_size()
            screen.blit(option_surface, dest=(screen_size[0] // 2 - option_size[0] // 2, option_y))
            option_y += option_size[1]


if __name__ == "__main__":
    pygame.init()
    SoundManager.init()

    pygame.display.set_mode((W, H), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("TEMPEST RUN")
    loop = GameLoop()
    loop.start()
