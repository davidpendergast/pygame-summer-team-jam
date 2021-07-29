# this is a simple image editor
# takes a pixel art, preferably low resolution
# and allows you to define point-pairs to draw lines
# divides the image wrt to the center to allow rotating objects wrt center using programs
import tkinter
import os
import pygame
from tkinter.filedialog import askopenfilename
import json
from typing import Union

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FPS = 60


class Button:
    def __init__(self, display: pygame.Surface, msg='BUTTON', x=250, y=250, action=None):
        self.display = display
        self.msg = msg
        self.x = x
        self.y = y
        self.active = False
        self.action = action
        self.text_size = 25
        self.rect = pygame.Rect(self.x, self.y, self.text_size * (len(self.msg) + 3), self.text_size * 2)

    def update(self, events):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            self.active = True
        else:
            self.active = False
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self.rect.collidepoint(mx, my):
                        if self.action is not None:
                            self.action()

    def draw(self):
        color = (255, 255, 255) if self.active else (0, 0, 255)
        pygame.draw.rect(self.display, color, self.rect, 5)
        font = pygame.font.Font('EightBit Atari-Ascprin.ttf', self.text_size)
        text = font.render(self.msg, False, color)
        self.display.blit(text, text.get_rect(center=self.rect.center))


class MainEditor:
    def __init__(self, display: pygame.Surface):
        self.display = display
        self.BG_COLOR = (0, 0, 0)
        self.LINE_COLOR = (0, 0, 255)
        self.loop_running = True
        self.clock = pygame.time.Clock()
        self.scale = 1
        self.preview = False
        self.mode = 'pen'  # or 'eraser'
        self.image_name = ''
        self.image: Union[None, pygame.Surface] = None
        self.point_pairs = []  # [[(1, 1), (3, 3)]]
        self.image_offset = pygame.Vector2(50, 50)
        self.selected_point = None
        self.point_history = []
        self.buttons = [Button(display, 'SAVE', 350, 50, action=self.save_img),
                        Button(display, 'UNDO', 350, 150, action=self.undo),
                        Button(display, 'REDO', 350, 250, action=self.redo)]

    def scale_up(self):
        self.scale += 1
        if self.scale > 25:
            self.scale = 25

    def scale_down(self):
        self.scale -= 1
        if self.scale < 1:
            self.scale = 1

    def undo(self):
        if len(self.point_pairs) > 0:
            self.point_history.append(self.point_pairs.pop())

    def redo(self):
        if len(self.point_history) > 0:
            self.point_pairs.append(self.point_history.pop())

    def check_events(self, events):
        keys = pygame.key.get_pressed()
        for e in events:
            if e.type == pygame.QUIT:
                self.loop_running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.loop_running = False
                if e.key == pygame.K_p:
                    self.preview = not self.preview
                if e.key == pygame.K_e:
                    if self.mode == 'pen':
                        self.mode = 'eraser'
                    elif self.mode == 'eraser':
                        self.mode = 'pen'
                if e.key == pygame.K_KP_PLUS:
                    self.scale_up()
                if e.key == pygame.K_KP_MINUS:
                    self.scale_down()
                if e.key == pygame.K_z:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        self.undo()
                if e.key == pygame.K_y:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        self.redo()
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = self.get_mouse_coordinates()
                if pos is None:
                    return
                else:
                    if self.mode == 'pen':
                        if self.selected_point is None:
                            self.selected_point = [(pos[0] - self.image_offset.x) // self.scale, (pos[1] - self.image_offset.y) // self.scale]
                        else:
                            x = (pos[0] - self.image_offset.x) // self.scale
                            y = (pos[1] - self.image_offset.y) // self.scale
                            self.point_pairs.append([self.selected_point, [x, y]])
                            self.selected_point = None
                            self.point_history = []
                    elif self.mode == 'eraser':
                        print(self.point_pairs)
                        for i in range(len(self.point_pairs)):
                            for j in range(len(self.point_pairs[i])):
                                x = (pos[0] - self.image_offset.x) // self.scale
                                y = (pos[1] - self.image_offset.y) // self.scale
                                print(self.point_pairs[i][j], '___', [x, y])
                                if [x, y] == self.point_pairs[i][j]:
                                    self.point_pairs.pop(i)
                                    continue

    def update(self):
        events = pygame.event.get()
        self.check_events(events)
        for i in self.buttons:
            i.update(events)
        pygame.display.set_caption('IMAGE TO POINTS EDITOR FPS = ' + str(int(self.clock.get_fps())))

    def draw_image(self):
        if self.image is not None:
            img = pygame.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
            self.display.blit(img, (self.image_offset.x, self.image_offset.y))

    def draw_lines(self):
        if self.scale // 4 < 1:
            line_width = 1
        else:
            line_width = self.scale // 4
        for i in range(len(self.point_pairs)):
            x1, y1 = self.point_pairs[i][0]
            x2, y2 = self.point_pairs[i][1]
            p1 = (self.image_offset.x + x1 * self.scale + self.scale // 2, self.image_offset.y + y1 * self.scale + self.scale // 2)
            p2 = (self.image_offset.x + x2 * self.scale + self.scale // 2, self.image_offset.y + y2 * self.scale + self.scale // 2)
            pygame.draw.line(screen, self.LINE_COLOR, p1, p2, line_width)

    def check_mouse_over_img(self):
        mx, my = pygame.mouse.get_pos()
        img_rect = pygame.Rect(self.image_offset.x, self.image_offset.y, self.image.get_width() * self.scale, self.image.get_height() * self.scale)
        if img_rect.collidepoint(mx, my):
            return True
        else:
            return False

    def get_mouse_coordinates(self):
        mx, my = pygame.mouse.get_pos()
        if not self.check_mouse_over_img():
            return
        col = (mx - self.image_offset.x) // self.scale
        row = (my - self.image_offset.y) // self.scale
        return self.image_offset.x + col * self.scale, self.image_offset.y + row * self.scale

    def draw_mouse_pointer(self):
        if self.scale // 4 < 1:
            line_width = 1
        else:
            line_width = self.scale // 4
        pos = self.get_mouse_coordinates()
        if pos is None:
            return
        else:
            x, y = pos
        pygame.draw.rect(self.display, self.LINE_COLOR, pygame.Rect(x, y, self.scale, self.scale))
        if self.selected_point is not None:
            x1 = self.selected_point[0] * self.scale + self.image_offset.x + self.scale // 2
            y1 = self.selected_point[1] * self.scale + self.image_offset.x + self.scale // 2
            pygame.draw.line(self.display, self.LINE_COLOR, (x1, y1), (x + self.scale // 2, y + self.scale // 2), line_width)

    def draw(self):
        self.display.fill(self.BG_COLOR)
        for i in self.buttons:
            i.draw()
        if not self.preview:
            self.draw_image()
        self.draw_lines()
        self.draw_mouse_pointer()
        pygame.display.update()
        self.clock.tick(FPS)

    def load_img(self, img_name):
        # needs to have img in the same directory for now
        self.image_name = img_name
        self.image = pygame.image.load(img_name)
        try:
            file_name = self.image_name.split('.')[0] + '_data.json'
            f = open(file_name, 'r')
            self.point_pairs = json.loads(f.read())
            f.close()
        except FileNotFoundError:
            print('Image Data not Found')

    def save_img(self):
        file_name = self.image_name.split('.')[0] + '_data.json'
        f = open(file_name, 'w')
        f.write(json.dumps(self.point_pairs))
        f.close()

    def img_dialog_box(self):
        root = tkinter.Tk()
        root.withdraw()
        file_name = askopenfilename(title='Select an Image File')
        if os.path.exists(file_name):
            self.load_img(file_name)

    def start(self):
        while self.loop_running:
            self.update()
            self.draw()


try:
    editor = MainEditor(screen)
    editor.img_dialog_box()
    # editor.load_img('img6.png')
    editor.start()
except pygame.error as error:
    print('An Error occurred')
    print(error)
