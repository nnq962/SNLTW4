import pygame
from pygame.locals import *
import sys

pygame.init()

# Gọi vào các hình ảnh
background = pygame.image.load("assets/background-night.png")
background = pygame.transform.scale2x(background)  # phóng to lên 2 lần

floor = pygame.image.load("assets/floor.png")
floor = pygame.transform.scale2x(floor)  # phóng to lên 2 lần

bird = [pygame.image.load("assets/yellowbird-midflap.png"),
        pygame.image.load("assets/yellowbird-upflap.png"),
        pygame.image.load("assets/yellowbird-downflap.png")]
bird = [pygame.transform.scale2x(bird[0]),
        pygame.transform.scale2x(bird[1]),
        pygame.transform.scale2x(bird[2])]  # phóng to lên 2 lần
bird_rect = [bird[0].get_rect(center=(100, 384)),
             bird[1].get_rect(center=(100, 384)),
             bird[2].get_rect(center=(100, 384))]  # tạo một hình chữ nhật bao quanh bird


class App:
    """
    Giao diện game
    """

    def __init__(self, width=432, height=768):
        self.width = width
        self.height = height
        self.background = background
        self.floor = floor
        self.bird = bird
        self.bird_rect = bird_rect
        self.gravity = 0.25
        self.bird_movement = 0
        self.x_floor = 0
        self.screen = None
        self.running = True
        self.fps = 40
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird")

    def on_render(self):
        self.screen.blit(self.background, (0, 0))  # vẽ background

        self.screen.blit(self.floor, (self.x_floor, 600))   # vẽ sàn 1
        self.screen.blit(self.floor, (self.x_floor + 432, 600))   # vẽ sàn 2
        self.x_floor -= 1
        if self.x_floor <= -432:
            self.x_floor = 0

        self.screen.blit(self.bird[0], self.bird_rect[0])

        self.bird_movement += self.gravity

        self.clock.tick(self.fps)

        # cập nhật màn hình
        pygame.display.flip()

    def on_execute(self):
        self.on_init()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.K_DOWN:
                    if event.key == pygame.K_SPACE:
                        print("test")

            self.on_render()


mygame = App()
mygame.on_execute()
