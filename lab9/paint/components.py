import pygame
import random


YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


def create_coin(length, width, coin_radius):
    x = random.randint(0, length - coin_radius * 2)
    y = random.randint(0, width - coin_radius * 2)
    coin = pygame.Rect(x, y, coin_radius * 2, coin_radius * 2)
    return coin


def draw_player(screen, player_pos):
    pygame.draw.rect(screen, BLUE, player_pos)


def draw_coins(screen, coins):
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin.center, 10)


def collect_coins(player_pos, coins):
    collected_coins = 0
    for coin in coins[:]:
        if player_pos.colliderect(coin):
            coins.remove(coin)
            collected_coins += 1
    return collected_coins


def draw_coin_count(screen, collected_coins, length):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Coins: {collected_coins}', True, (0, 0, 0))
    screen.blit(text, (length - 150, 20))


def move_enemy(enemy_pos, enemy_speed, length):
    enemy_pos.x += enemy_speed
    if enemy_pos.right > length or enemy_pos.left < 0:
        enemy_speed = -enemy_speed 
    return enemy_pos, enemy_speed
