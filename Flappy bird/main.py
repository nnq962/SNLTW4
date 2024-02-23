import pygame
import random
import sys

pygame.init()

# chèn background
background = pygame.transform.scale2x(pygame.image.load("assets/background-night.png"))  # phóng to lên 2 lần
# chèn sàn
floor = pygame.transform.scale2x(pygame.image.load("assets/floor.png"))  # phóng to lên 2 lần
# chèn chim
bird_mid = pygame.image.load("assets/yellowbird-midflap.png")
bird_up = pygame.image.load("assets/yellowbird-upflap.png")
bird_down = pygame.image.load("assets/yellowbird-downflap.png")
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))  # tạo một hình chữ nhật bao quanh bird
# chèn ống
pipe = pygame.transform.scale2x(pygame.image.load("assets/pipe-green.png"))  # phóng to lên 2 lần
# chèn game over
game_over = pygame.transform.scale2x(pygame.image.load("assets/message.png"))
game_over_rect = game_over.get_rect(center=(216, 384))
# tạo timeer cho chim
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)
# tạo timer cho ống
spawnpipe_event = pygame.USEREVENT
pygame.time.set_timer(spawnpipe_event, 1200)  # sau 1.2 giây
# load font
game_font = pygame.font.Font("font.TTF", 40)


class Player:
    """
    Class quản lí chim
    """

    def __init__(self):
        self.bird_list = bird_list
        self.bird_index = 0
        self.bird = bird_list[bird_index]
        self.bird_rect = bird_rect
        self.gravity = 0.2
        self.bird_movement = 0
        self.score = 0
        self.high_score = 0

    def down(self):
        self.bird_movement = -5

    def check_collision(self, pipes):
        for i in pipes:
            if self.bird_rect.colliderect(i):
                return False
                pass
        if self.bird_rect.top <= -75 or self.bird_rect.bottom >= 700:
            return False
            pass
        return True

    def bird_animation(self):
        if self.bird_index < 2:
            self.bird_index += 1
        else:
            self.bird_index = 0
        self.bird = self.bird_list[self.bird_index]
        self.bird_rect = self.bird.get_rect(center=(100, self.bird_rect.centery))

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        return self.high_score

    def reset_score(self):
        self.score = 0


class App:
    """
    Giao diện game
    """

    def __init__(self, width=432, height=768):
        self.width = width
        self.height = height
        self.background = background
        self.floor = floor
        self.x_floor = 0
        self.screen = None
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.pipe = pipe
        self.pipe_height = [300, 400, 500]
        self.player = Player()
        self.spawnpipe_event = None
        self.game_active = True
        self.game_over = game_over
        self.game_over_rect = game_over_rect
        self.pipe_list = []

    def on_init(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird")

    def create_pipe(self):
        random_pipe_height = random.choice(self.pipe_height)
        bottom_pipe = self.pipe.get_rect(midtop=(500, random_pipe_height))
        top_pipe = self.pipe.get_rect(midtop=(500, random_pipe_height - 750))
        return top_pipe, bottom_pipe

    def move_pipe(self):
        for i in self.pipe_list:
            i.centerx -= 5
        return self.pipe_list

    def draw_pipe(self):
        for i in self.pipe_list:
            if i.bottom >= 600:
                self.screen.blit(self.pipe, i)
            else:
                flip_pipe = pygame.transform.flip(self.pipe, False, True)
                self.screen.blit(flip_pipe, i)

    def draw_floor(self):
        self.screen.blit(self.floor, (self.x_floor, 650))  # vẽ sàn 1
        self.screen.blit(self.floor, (self.x_floor + 432, 650))  # vẽ sàn 2
        self.x_floor -= 1
        if self.x_floor <= -432:  # lùi sàn
            self.x_floor = 0

    def draw_bird(self):
        rotated_bird = self.rotate_bird()
        self.screen.blit(rotated_bird, self.player.bird_rect)
        self.player.bird_movement += self.player.gravity
        self.player.bird_rect.centery += self.player.bird_movement

    def score_display(self):
        if self.game_active:
            self.player.score += 0.01
            score_surface = game_font.render(str(int(self.player.score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(216, 100))
            self.screen.blit(score_surface, score_rect)
        else:
            self.player.update_score()
            score_surface = game_font.render(f'Score: {(int(self.player.score))}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(216, 100))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = game_font.render(f'High Score: {(int(self.player.high_score))}', True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(216, 630))
            self.screen.blit(high_score_surface, high_score_rect)
            self.end_game()

    def restart_game(self):
        self.game_active = True
        self.pipe_list.clear()
        self.player.bird_rect.center = (100, 384)
        self.player.bird_movement = 0
        self.player.reset_score()

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.player.bird, -self.player.bird_movement * 3, 1)
        return new_bird

    def end_game(self):
        self.screen.blit(self.game_over, self.game_over_rect)

    def on_render(self):
        self.screen.blit(self.background, (0, 0))  # vẽ background
        self.score_display()
        if self.game_active:
            self.draw_bird()
            self.move_pipe()
            self.draw_pipe()
        self.draw_floor()
        self.clock.tick(self.fps)
        # cập nhật màn hình
        pygame.display.flip()

    def on_execute(self):
        self.on_init()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active is True:
                        self.player.down()
                    if event.key == pygame.K_SPACE and self.game_active is False:
                        self.restart_game()
                if event.type == spawnpipe_event:
                    self.pipe_list.extend(self.create_pipe())
                if event.type == bird_flap:
                    self.player.bird_animation()
            self.game_active = self.player.check_collision(self.pipe_list)
            self.on_render()


mygame = App()
mygame.on_execute()
