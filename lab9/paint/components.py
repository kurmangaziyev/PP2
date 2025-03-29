"""
Это игра Змейка, где игрок, студент, учитель или любой человек управляет змейкой, 
которая двигается по экрану, съедает еду и растет. 
Игрок должен избегать столкновений с стенами или с самой собой, иначе игра заканчивается.
"""

import pygame
import random
from pygame.locals import *
#Мы подключаем библиотеку pygame, которая нужна для создания графики и анимации. 
#Также подключаем random, чтобы случайным образом генерировать еду для змеи.

pygame.init()
#Эта команда запускает все необходимые компоненты библиотеки Pygame для работы с графикой, звуком и т. д.

# Настройка экрана игры чисто хуже hd чтобы не лагалXD
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# шрифт для текста
font_small = pygame.font.SysFont("Verdana", 20)

# настройки змеи
block_size = 20  # Размер блока змеи
snake_speed = 10  # Начальная скорость змеи

# основной шрифт для отображения текста
font = pygame.font.SysFont(None, 25)

# зис фанкшин для рисования змеи
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], block_size, block_size])

# зис фанкшин нужен для отображения сообщения на экране
def message(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [screen_width / 6, screen_height / 3])


def generate_food():
    food_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0
    return food_x, food_y


def game_loop(snake_speed):
    game_over = False
    game_close = False

    snake_list = []  
    snake_length = 1  
    snake_x = screen_width / 2  
    snake_y = screen_height / 2  
    snake_x_change = 0  
    snake_y_change = 0  

    # Настройки еды
    food_x, food_y = generate_food()  # Генерируем еду

    # начальный счет и уровень
    score = 0
    level = 1

    # таймер для обновления экрана
    clock = pygame.time.Clock()

    # основной игровой цикл
    while not game_over:
        # экран окончания игры
        while game_close == True:
            screen.fill(white)
            message("You lost! Press Q to quit or C to play again", red)
            pygame.display.update()

            # обработка событий на экране окончания игры
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Нажатие Q для выхода из игры
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # Нажатие C для новой игры
                        game_loop(snake_speed)

        # Обработка движения змеи
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -block_size
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = block_size
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_y_change = -block_size
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_y_change = block_size
                    snake_x_change = 0

      
        snake_x += snake_x_change
        snake_y += snake_y_change

        # проверка на столкновение с границами экрана
        if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
            game_close = True

        # проверка на столкновение с едой
        if snake_x == food_x and snake_y == food_y:
            score += 1  # увеличиваем счет
            snake_length += 1  # увеличиваем длину змеи
            food_x, food_y = generate_food()  # генерируем новую еду

            # увеличиваем уровень каждый раз, когда съедено 3 еды
            if score % 3 == 0:
                level += 1
                snake_speed += 2  # увеличиваем скорость змеи с каждым уровнем

        # рисуем фон и еду
        screen.fill(white)
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        # добавляем голову змеи в список
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)

        # удаляем хвост змеи, если она слишком длинная, так скажем режем)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка на столкновение змеи с собой
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

     
        draw_snake(snake_list)   # для прорисовки змеи на экране

        
        score_text = font_small.render("Score: " + str(score), True, black)
        level_text = font_small.render("Level: " + str(level), True, black)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 30))# Счет уровень показывается блягодоаря этой команде

      
        pygame.display.update()  # нужна для обновление экрана

        
        clock.tick(snake_speed) # регулируем скорость игры в зависимости от текущего уровня

    # ииии завершение столь мощной игры:(
    pygame.quit()
    quit()


game_loop(snake_speed)
