import pygame
import random
from pygame.locals import *
# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

font_small = pygame.font.SysFont("Verdana", 20)

# Snake properties
block_size = 20
snake_speed = 10

# Fonts
font = pygame.font.SysFont(None, 25)

# Function to draw snake
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], block_size, block_size])

# Function to display message
def message(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [screen_width / 6, screen_height / 3])

# Function to create food
def generate_food():
    food_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0
    return food_x, food_y

# Game loop
def game_loop(snake_speed):
    game_over = False
    game_close = False

    # Snake properties
    snake_list = []
    snake_length = 1
    snake_x = screen_width / 2
    snake_y = screen_height / 2
    snake_x_change = 0
    snake_y_change = 0

    # Food properties
    food_x, food_y = generate_food()

    # Score and level
    score = 0
    level = 1

    
    clock = pygame.time.Clock()

    # Main game loop
    while not game_over:
        # Game over screen
        while game_close == True:
            screen.fill(white)
            message("You lost! Press Q to quit or C to play again", red)
            pygame.display.update()

            # Event handling for game over screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(snake_speed)

        # Event handling
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

        # Move the snake
        snake_x += snake_x_change
        snake_y += snake_y_change

        # Check for border collision
        if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
            game_close = True

        # Check for food collision
        if snake_x == food_x and snake_y == food_y:
            score += 1
            snake_length += 1
            food_x, food_y = generate_food()

            # Increase level every 3 foods
            if score % 3 == 0:
                level += 1
                snake_speed += 2

        screen.fill(white)
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        #show score and level
        draw_snake(snake_list)
        score_text = font_small.render("Score: " + str(score), True, black)
        level_text = font_small.render("Level: " + str(level), True, black)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 30))
        pygame.display.update()

        # Adjust game speed based on snake_speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game loop with snake_speed
game_loop(snake_speed)
