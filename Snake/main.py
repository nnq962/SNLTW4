import pygame
from pygame.locals import *
import time
from random import randint


class Apple:
    """
    Class đại diện cho quả táo
    """
    def __init__(self, x=0, y=0, step=40):
        """
        Hàm khởi tạo
        :param x: vị trí x của quả táo
        :param y: vị trí y của quả táo
        :param step: bước nhảy trên hệ trục toạ độ
        """
        self.step = step
        self.x = x * self.step
        self.y = y * self.step

        # màu xanh (r, g, b)
        self.color = (0, 255, 0)  # Quả táo màu xanh

    def draw(self, surface):
        """
        Hàm vẽ ra quả táo
        """
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.step, self.step))


class Player:
    """
    Class Player đại diện cho Rắn
    """
    def __init__(self, length=3, step=40, direction=0, updatecountmax=4, updatecount=0, score=0):
        """
        Hàm khởi tạo
        :param length: độ dài
        :param step: bước nhảy trên hệ trục toạ độ
        :param direction: hướng
        :param updatecountmax: giới hạn update
        :param updatecount: số lần update
        :param score: Điểm số
        """
        self.updateCount = updatecount
        self.updateCountMax = updatecountmax
        self.direction = direction
        self.length = length
        self.step = step
        self.score = score

        # khởi tạo 2 list
        self.x = [0]
        self.y = [0]

        # mở rộng x và y để lưu vị trí rắn
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # khởi tạo vị trí đầu tiên
        self.x[1] = 1 * self.step
        self.x[2] = 2 * self.step

        # màu đỏ (r, g, b)
        self.color = (255, 0, 0)

    def update(self):

        # làm chậm số lần update
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # cập nhật vị trí cũ
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # cập nhật vị trí đầu rắn
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    def draw(self, surface):
        """
        Hàm vẽ rắn
        """
        for i in range(0, self.length):
            pygame.draw.rect(surface, self.color, (self.x[i], self.y[i], self.step, self.step))

    def up_score(self):
        self.score += 1


def is_collision(x1, y1, x2, y2):
    """
    Hàm kiểm tra va chạm
    :param x1: toạ độ x vật 1
    :param y1: toạ độ y vật 1
    :param x2: toạ độ x vật 2
    :param y2: toạ độ y vật 2
    :return: bool
    """
    if x1 == x2 and y1 == y2:
        return True
    return False


class App:
    """
    Giao diện game
    """
    def __init__(self, width=880, height=520):
        self.running = True
        self.display_surface = None
        self.width = width
        self.height = height
        self.snake = Player(length=3)
        self.apple = Apple(4, 4)

    def on_init(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Snake")

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_loop(self):
        self.snake.update()

        # Nếu rắn đi ra khỏi cửa sổ
        if self.snake.x[0] < 0:
            self.snake.x[0] = self.width - self.snake.step
        if self.snake.x[0] >= self.width:
            self.snake.x[0] = 0
        if self.snake.y[0] < 0:
            self.snake.y[0] = self.height - self.snake.step
        if self.snake.y[0] >= self.height:
            self.snake.y[0] = 0

        # Kiểm tra xem rắn ăn táo
        for i in range(0, self.snake.length):
            if is_collision(self.apple.x, self.apple.y, self.snake.x[i], self.snake.y[i]):
                self.apple.x = randint(0, 21) * self.snake.step
                self.apple.y = randint(0, 12) * self.snake.step
                self.snake.up_score()
                self.snake.length += 1

        # Kiểm tra xem rắn có cắn vào bản thân
        for i in range(2, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                print()
                print("====== YOU LOSE ======")
                print("YOUR SCORES:", self.snake.score)
                self.running = False

    def on_render(self):
        self.display_surface.fill((255, 255, 255))
        self.snake.draw(self.display_surface)
        self.apple.draw(self.display_surface)

        # Tạo lưới ô vuông
        line_color = (200, 200, 200)
        cell_size = self.snake.step
        for x in range(0, self.width, cell_size):
            pygame.draw.line(self.display_surface, line_color, (x, 0), (x, self.height))
        for y in range(0, self.height, cell_size):
            pygame.draw.line(self.display_surface, line_color, (0, y), (self.width, y))

        # Vẽ điểm số lên màn hình
        font = pygame.font.Font(None, 36)  # Tạo đối tượng font
        text = font.render("Score: " + str(self.snake.score), True, (0, 0, 0))  # Tạo đối tượng văn bản
        self.display_surface.blit(text, (10, 10))  # Vẽ văn bản tại vị trí (10, 10)

        # Cập nhật màn hình
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while self.running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.snake.move_right()

            if keys[K_LEFT]:
                self.snake.move_left()

            if keys[K_UP]:
                self.snake.move_up()

            if keys[K_DOWN]:
                self.snake.move_down()

            if keys[K_ESCAPE]:
                self.running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0)
        self.on_cleanup()


mygame = App()
mygame.on_execute()
