import pygame 
import math

# Инициализация Pygame
pygame.init()

# Определение цветов (RGB)
WHITE = (255,255,255)  # Белый цвет
RED = (255,0,0)        # Красный цвет
GREEN = (0,255,0)      # Зеленый цвет
BLUE = (0,0,255)       # Синий цвет
BLACK = (0,0,0)        # Черный цвет

# Установка начального цвета
COLOR = RED   

# Настройки FPS
clock = pygame.time.Clock()
FPS = 30

# Переменные для рисования
prev, cur = None, None  # Для пера (линий)
prev1, cur1 = None, None # Для ластика

# Создание окна программы
lenght, weight = 1000, 600
screen = pygame.display.set_mode((lenght,weight))
screen.fill(WHITE)  # Заливка фона белым цветом
running = True

# Режим рисования
pen = "mouse"
last_event = None

# Главный цикл программы
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Завершение программы при закрытии окна

        # Обработка нажатий клавиш для изменения режима рисования
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pen = "mouse"  # Режим рисования карандашом (линии)
            if event.key == pygame.K_w:
                pen = "rect"  # Режим рисования прямоугольника
            if event.key == pygame.K_e:
                pen = "circle"  # Режим рисования круга
            if event.key == pygame.K_r:
                pen = "eraser"  # Режим ластика
            
            # Изменение цвета
            if event.key == pygame.K_z:
                COLOR = RED  # Красный
            if event.key == pygame.K_x:
                COLOR = GREEN  # Зеленый
            if event.key == pygame.K_c:
                COLOR  = BLUE  # Синий
            if event.key == pygame.K_v:
                COLOR = BLACK  # Черный

        # Режим рисования карандашом (линии)
        if pen == "mouse":
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev = pygame.mouse.get_pos()  # Начальная точка линии
            if event.type == pygame.MOUSEMOTION:
                cur = pygame.mouse.get_pos()  # Текущая позиция мыши
            if prev:
                pygame.draw.line(screen, COLOR, prev, cur, 1)  # Рисуем линию
                prev = cur
            if event.type == pygame.MOUSEBUTTONUP:
                prev = None  # Сброс точки после отпускания кнопки

        # Режим рисования прямоугольника
        if pen == "rect":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.line(screen, COLOR, (x, y), (x1, y), 1)
                pygame.draw.line(screen, COLOR, (x1, y), (x1, y1), 1)
                pygame.draw.line(screen, COLOR, (x1, y1), (x, y1), 1)
                pygame.draw.line(screen, COLOR, (x, y1), (x, y), 1)
                last_event = 'None'

        # Режим рисования круга
        if pen == "circle":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.circle(screen, COLOR, (x + (x1 - x) // 2, y + (y1 - y) // 2), (x1 - x) // 2)
                pygame.draw.circle(screen, WHITE, (x + (x1 - x) // 2, y + (y1 - y) // 2), ((x1 - x) // 2) - 1)
                last_event = 'None'

        # Режим ластика
        if pen == "eraser":
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev1 = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                cur1 = pygame.mouse.get_pos()
            if prev1:
                pygame.draw.line(screen, WHITE, prev1, cur1, 10)  # Ластик рисует белым
                prev1 = cur1
            if event.type == pygame.MOUSEBUTTONUP:
                prev1 = None

    # Обновление экрана
    pygame.display.flip()
    
    # Ограничение FPS
    clock.tick(FPS)

# Завершение работы pygame
pygame.quit()
