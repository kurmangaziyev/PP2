import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# Устанавливаем частоту кадров
FPS = 60
FramePerSec = pygame.time.Clock()

# Определяем цвета
BLACK = (0, 0, 0)

# Размеры экрана
SCREEN_WIDTH = 390
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

# Настройки шрифтов
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загружаем изображения
background = pygame.image.load(r"C:\Users\Рабочий стол\PP2\lab8\racer\road.jpg")
DEFAULT_IMAGE_SIZE = (80, 150)
enemy_image = pygame.image.load(r"C:\Users\Рабочий стол\PP2\lab8\racer\enemy.png")
enemy = pygame.transform.scale(enemy_image, DEFAULT_IMAGE_SIZE)
player_image = pygame.image.load(r"C:\Users\Рабочий стол\PP2\lab8\racer\player.png")
player = pygame.transform.scale(player_image, DEFAULT_IMAGE_SIZE)
coin_image = pygame.image.load(r"C:\Users\Рабочий стол\PP2\lab8\racer\coin.png")
coin = pygame.transform.scale(coin_image, (50, 50))

# Создаем окно
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# Классы объектов
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = coin
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Создаем объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Создаем пользовательские события
INC_SPEED = pygame.USEREVENT + 1
ADD_COIN = pygame.USEREVENT + 2 
pygame.time.set_timer(INC_SPEED, 1000)  # Увеличение скорости каждую секунду
pygame.time.set_timer(ADD_COIN, 3000)  # Добавление новой монеты каждые 3 секунды

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Увеличиваем скорость врагов
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == ADD_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    # Проверяем столкновение игрока с монетами
    coin_collected = pygame.sprite.spritecollideany(P1, coins)
    if coin_collected:
        pygame.mixer.Sound(r"C:\Users\Рабочий стол\PP2\lab8\racer\coin_collect.mp3").play()
        coins.remove(coin_collected)  
        all_sprites.remove(coin_collected)  
        SCORE += 1  

    # Отображаем фон и счет
    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Перемещаем и рисуем все спрайты
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверяем столкновение с врагами
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(r"C:\Users\Рабочий стол\PP2\lab8\racer\crash.wav").play()
        time.sleep(0.5)

        crashed_image = pygame.image.load(r"C:\Users\Рабочий стол\PP2\lab8\racer\Crashed_Mercedes-Benz_vehicles.jpg")
        crashed_image = pygame.transform.scale(crashed_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        DISPLAYSURF.blit(crashed_image, (0, 0))
        DISPLAYSURF.blit(game_over, (30, 40))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
