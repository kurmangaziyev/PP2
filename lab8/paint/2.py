# Лабораторная работа 9 - Paint
import pygame 
import math

# Инициализация Pygame
pygame.init()

# Установка цветов (RGB)
WHITE = (255,255,255)  # Белый
RED = (255,0,0)        # Красный
GREEN = (0,255,0)      # Зеленый
BLUE = (0,0,255)       # Синий
BLACK = (0,0,0)        # Черный

# Начальный цвет рисования
COLOR = RED   

# Настройки FPS
clock = pygame.time.Clock()
FPS = 30

# Переменные для рисования
prev, cur = None, None  # Для карандаша
prev1, cur1 = None, None # Для ластика

# Создание окна
length, weight = 1000, 600
screen = pygame.display.set_mode((length, weight))
screen.fill(WHITE)  # Заливка фона белым цветом
running = True

# Переменные для режима рисования
pen = "mouse"
last_event = None

# Основной цикл программы
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Завершение программы

        # Изменение режима рисования
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pen = "mouse"  # Карандаш
            if event.key == pygame.K_w:
                pen = "rect"  # Прямоугольник
            if event.key == pygame.K_e:
                pen = "circle"  # Круг
            if event.key == pygame.K_r:
                pen = "eraser"  # Ластик
            if event.key == pygame.K_t:
                pen = "square"  # Квадрат
            if event.key == pygame.K_y:
                pen = "equilateral_triangle"  # Равносторонний треугольник
            if event.key == pygame.K_u:
                pen = "right triangle"  # Прямоугольный треугольник
            if event.key == pygame.K_i:
                pen = "rhombus"  # Ромб

            # Изменение цвета
            if event.key == pygame.K_z:
                COLOR = RED
            if event.key == pygame.K_x:
                COLOR = GREEN
            if event.key == pygame.K_c:
                COLOR = BLUE
            if event.key == pygame.K_v:
                COLOR = BLACK

        # Рисование карандашом (линии)
        if pen == "mouse":
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                cur = pygame.mouse.get_pos()
            if prev:
                pygame.draw.line(screen, COLOR, prev, cur, 1)
                prev = cur
            if event.type == pygame.MOUSEBUTTONUP:
                prev = None

        # Рисование прямоугольника
        if pen == "rect":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.rect(screen, COLOR, (x, y, x1-x, y1-y), 1)
                last_event = 'None'

        # Рисование круга
        if pen == "circle":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.circle(screen, COLOR, (x + (x1 - x) // 2, y + (y1 - y) // 2), (x1 - x) // 2)
                last_event = 'None'

        # Ластик
        if pen == "eraser":
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev1 = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                cur1 = pygame.mouse.get_pos()
            if prev1:
                pygame.draw.line(screen, WHITE, prev1, cur1, 10)
                prev1 = cur1
            if event.type == pygame.MOUSEBUTTONUP:
                prev1 = None

        # Рисование квадрата
        if pen == "square":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                side = min(abs(x1 - x), abs(y1 - y))
                pygame.draw.rect(screen, COLOR, (x, y, side, side), 1)
                last_event = 'None'

        # Рисование равностороннего треугольника
        if pen == "equilateral_triangle":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                h = y + (math.sqrt(3) * (x1 - x) / 2)
                a = ((x + (x1 - x) / 2), y)
                b = (x, h)
                c = (x1, h)
                pygame.draw.polygon(screen, COLOR, [a, b, c], 1)
                last_event = "None"

        # Рисование прямоугольного треугольника
        if pen == "right triangle":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.polygon(screen, COLOR, [(x, y), (x, y1), (x1, y1)], 1)
                last_event = "None"

        # Рисование ромба
        if pen == "rhombus":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                a = (x + (x1 - x) / 2, y)
                b = (x1, y + (y1 - y) / 2)
                c = (x + (x1 - x) / 2, y1)
                d = (x, y + (y1 - y) / 2)
                pygame.draw.polygon(screen, COLOR, [a, b, c, d], 1)
                last_event = "None"

    # Обновление экрана
    pygame.display.flip()
    
    # Ограничение FPS
    clock.tick(FPS)

# Завершение Pygame
pygame.quit()
