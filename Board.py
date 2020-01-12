# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import math
from pic2array import *
import tkinter as tk

def new_window(result):
    root = tk.Tk()
    root.title("识别结果")

    root.geometry("300x120") 
    theLabel = tk.Label(root, text="识别结果>>>{}".format(result),font=("幼圆", 20),fg="white",bg="green")

    theLabel.pack(side=tk.TOP,pady=40)
    root.mainloop()

class Brush:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 10
        self.drawing = False
        self.last_pos = None
        self.style = True
        self.brush = pygame.image.load("images/brush.png").convert_alpha()
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))

    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def set_brush_style(self, style):
        print("* set brush style to", style)
        self.style = style

    def get_brush_style(self):
        return self.style

    def get_current_brush(self):
        return self.brush_now

    def set_size(self, size):
        if size < 1:
            size = 1
        elif size > 32:
            size = 32
        print("* set brush size to", size)
        self.size = size
        self.brush_now = self.brush.subsurface((0, 0), (size*2, size*2))

    def get_size(self):
        return self.size

    def set_color(self, color):
        self.color = color
        for i in range(self.brush.get_width()):
            for j in range(self.brush.get_height()):
                self.brush.set_at((i, j),
                                  color + (self.brush.get_at((i, j)).a,))

    def get_color(self):
        return self.color

    def draw(self, pos):
        if self.drawing:
            for p in self._get_points(pos):
                if p[0] in range(84,790) and p[1]<=530:
                    if self.style:
                        self.screen.blit(self.brush_now, p)
                    else:
                        pygame.draw.circle(self.screen, self.color, p, self.size)
            self.last_pos = pos

    def _get_points(self, pos):
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x**2 + len_y**2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append((points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points))


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        #画板预定义的颜色值
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]
        #计算每个色块在画板中的坐标值，便于绘制
        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 254 + i / 2 * 32, 32, 32)
            self.colors_rect.append(rect)
        
        #两种笔刷的按钮图标
        self.pens = [
            pygame.image.load("images/pen1.png").convert_alpha(),
            pygame.image.load("images/pen2.png").convert_alpha(),
        ]
        #计算笔刷的按钮图标的坐标
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)
            
        #调整笔刷大小的按钮图标
        self.sizes = [
            pygame.image.load("images/big.png").convert_alpha(),
            pygame.image.load("images/small.png").convert_alpha()
        ]
        #计算坐标，便于绘制
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(10 + i * 32, 138, 32, 32)
            self.sizes_rect.append(rect)
            
        #功能按钮图标，包括重置和识别
        self.buttons = [
            pygame.image.load("images/reset.png").convert_alpha(),
            pygame.image.load("images/recognize.png").convert_alpha()
        ]
        self.buttons_rect = []
        for (i,img) in enumerate(self.buttons):
            rect = pygame.Rect(84 + i * 363, 530, 343, 68)
            self.buttons_rect.append(rect)
    
    def set_brush(self, brush):
        self.brush = brush

    def draw(self):
        # 绘制画笔样式按钮
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)
        #绘制“+ -”图标
        for (i, img) in enumerate(self.sizes):
            self.screen.blit(img, self.sizes_rect[i].topleft)
        #绘制功能按钮
        for (i, img) in enumerate(self.buttons):
            self.screen.blit(img,self.buttons_rect[i].topleft)
            
        #绘制用于实时展示笔刷的小窗口
        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 180 + 32
        if self.brush.get_brush_style():
            x = x - size
            y = y - size
            self.screen.blit(self.brush.get_current_brush(), (x, y))
        else:
            pygame.draw.circle(self.screen,
                               self.brush.get_color(), (x, y), size)
        #绘制色块
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])
        #绘制画图区
        pygame.draw.rect(self.screen,(0,0,0),(84,0,710,530),1)


    def click_button(self, pos):
        for (i, rect) in enumerate(self.pens_rect):
            if rect.collidepoint(pos):
                self.brush.set_brush_style(bool(i))
                return True
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i:
                    self.brush.set_size(self.brush.get_size() - 1)
                else:
                    self.brush.set_size(self.brush.get_size() + 1)
                return True
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                return True
                
        if self.buttons_rect[0].collidepoint(pos):
            print("# reset the screen.")
            self.screen.fill((255,255,255))
        if self.buttons_rect[1].collidepoint(pos):
            print("# begin to recognize")
            screen_copy = self.screen.copy()
            img = pygame.Surface((708,528))
            img.blit(screen_copy,dest=(0,0),area=(85,1,708,528))
            pygame.image.save(img,"to_recognize.png")
            result = recognize("to_recognize.png")
            print("result is {}".format(result))
            new_window(result)
        return False


class Painter:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 610)) #设置窗口大小为800*600
        pygame.display.set_caption("Painter") #设置窗口标题为Painter
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_brush(self.brush)

    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                elif event.type == MOUSEBUTTONDOWN:
                    self.menu.click_button(event.pos)
                    if event.pos[0]>=84 and event.pos[1]<=530:
                        self.brush.start_draw(event.pos)
                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()
            self.menu.draw()
            pygame.display.update()


def main():
    app = Painter()
    app.run()

if __name__ == '__main__':
    main()
