import pygame
import random
from components import create_coin, draw_player, draw_coins, collect_coins, draw_coin_count, move_enemy

# инициализация game, этот файл у меня управляет логикой игры. Он импортирует функции из components.py и запускает
# игровой процесс: движение игрока, сбор монет, увеличение скорости врагов и другие аспекты
pygame.init()

# устанавливаем цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# частота кадров (fps как в кс го но намного тормознейXD)
clock = pygame.time.Clock()
FPS = 30

# переменные игры
length, width = 1000, 600  # размеры экрана
player_pos = pygame.Rect(400, 300, 50, 50)  # игрок как прямоугольник (положение и размер)
player_speed = 5  # скорость игрока
coins = []  # список монет
collected_coins = 0  # количество собранных монет
coin_radius = 10  # радиус монеты
enemy_speed = 2  # скорость врага
enemy_pos = pygame.Rect(random.randint(0, length-50), random.randint(0, width-50), 50, 50)  # враг

# инициализация экрана
screen = pygame.display.set_mode((length, width))
screen.fill(WHITE)  # заполняем экран белым фоном
running = True  # флаг, управляющий игрой

# главный игровой цикл
while running:
    for event in pygame.event.get():  # обрабатываем все события
        if event.type == pygame.QUIT:  # если окно закрыто
            running = False  # завершаем игру

    # управление движением игрока
    keys = pygame.key.get_pressed()  # получаем состояние клавиш
    if keys[pygame.K_LEFT] and player_pos.left > 0:  # если нажата стрелка влево и игрок не выходит за границы
        player_pos.x -= player_speed
    if keys[pygame.K_RIGHT] and player_pos.right < length:  # если нажата стрелка вправо
        player_pos.x += player_speed
    if keys[pygame.K_UP] and player_pos.top > 0:  # если нажата стрелка вверх
        player_pos.y -= player_speed
    if keys[pygame.K_DOWN] and player_pos.bottom < width:  # если нажата стрелка вниз
        player_pos.y += player_speed

    # случайное создание монет без лог. посл.
    if random.random() < 0.05:  # 5% шанс на создание монеты каждый кадр
        coin = create_coin(length, width, coin_radius)
        coins.append(coin)  # добавляем монету в наш список

    # Сбор монет игроком
    collected_coins += collect_coins(player_pos, coins)  # kolichestvo sozdannyh monet

    # увеличение скорости врага каждое количество монет
    if collected_coins >= 5 and collected_coins % 5 == 0:
        enemy_speed += 1  # увеличиваем скорость врага

    # перемещение врага
    enemy_pos, enemy_speed = move_enemy(enemy_pos, enemy_speed, length)

    # сделать видимым или оботражение все элементы игры
    screen.fill(WHITE)  # Очищаем экран

    # отрисовываем игрока
    draw_player(screen, player_pos)

    # отрисовываем монеты
    draw_coins(screen, coins)

    # отображаем количество собранных монет
    draw_coin_count(screen, collected_coins, length)

    # делаем видимым врага врага
    pygame.draw.rect(screen, RED, enemy_pos)  # рисуем врага как прямоугольник

    pygame.display.flip()  # Обновляем экран

    # ограничиваем количество кадров в секунду
    clock.tick(FPS)

pygame.quit()  # Закрытие после выхода из игры
