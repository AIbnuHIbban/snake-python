import pygame
import sys
import random
import time

pygame.init()

# Konfigurasi layar
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Warna
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# varian makanan
food_type = random.choices(['red', 'blue', 'purple'], weights=[80, 15, 5])[0]

# Konfigurasi ular
SNAKE_SIZE = 20
snake_pos = [[WIDTH//2, HEIGHT//2], [WIDTH//2 + SNAKE_SIZE, HEIGHT//2], [WIDTH//2 + 2 * SNAKE_SIZE, HEIGHT//2]]
snake_speed = [-SNAKE_SIZE, 0]

# Konfigurasi makanan
FOOD_SIZE = 20
food_pos = [random.randrange(1, (WIDTH//FOOD_SIZE)) * FOOD_SIZE, random.randrange(1, (HEIGHT//FOOD_SIZE)) * FOOD_SIZE]
food_type = random.choices(['red', 'blue', 'purple'], weights=[80, 15, 5])[0]

# Skor
score = 0
font_score = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def draw_snake(snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

def draw_food(food_pos, food_type):
    color = None
    if food_type == 'red':
        color = RED
    elif food_type == 'blue':
        color = BLUE
    elif food_type == 'purple':
        color = PURPLE
    if color is not None:
        pygame.draw.rect(screen, color, pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE))

def draw_score(score):
    text = font_score.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    if restart_game():
        main_game()
    else:
        pygame.quit()
        sys.exit()

def restart_game():
    global score
    while True:
        font_instructions = pygame.font.Font(None, 24)
        retry_text = font_instructions.render("Tekan R untuk mencoba lagi atau Q untuk keluar", True, BLACK)
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT * 3 // 4 - retry_text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    return True
                if event.key == pygame.K_q:
                    return False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def start_screen():
    while True:
        screen.fill(WHITE)
        font_title = pygame.font.Font(None, 48)
        font_instructions = pygame.font.Font(None, 24)
        title = font_title.render("Snake Game", True, BLACK)
        instructions = font_instructions.render("Tekan ENTER untuk memulai", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3 - title.get_height() // 2))
        screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT * 2 // 3 - instructions.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_game():
    global snake_pos, snake_speed, food_pos, food_type, score
    snake_pos = [[WIDTH//2, HEIGHT//2], [WIDTH//2 + SNAKE_SIZE, HEIGHT//2], [WIDTH//2 + 2 * SNAKE_SIZE, HEIGHT//2]]
    snake_speed = [-SNAKE_SIZE, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_speed[1] != SNAKE_SIZE:
                    snake_speed = [0, -SNAKE_SIZE]
                elif event.key == pygame.K_DOWN and snake_speed[1] != -SNAKE_SIZE:
                    snake_speed = [0, SNAKE_SIZE]
                elif event.key == pygame.K_LEFT and snake_speed[0] != SNAKE_SIZE:
                    snake_speed = [-SNAKE_SIZE, 0]
                elif event.key == pygame.K_RIGHT and snake_speed[0] != -SNAKE_SIZE:
                    snake_speed = [SNAKE_SIZE, 0]

        # Perbarui posisi ular
        new_head = [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]]
        snake_pos.insert(0, new_head)

        # Cek tabrakan
        if snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT or snake_pos[0] in snake_pos[1:]:
            game_over()

        # Cek apakah ular telah makan makanan
        if snake_pos[0] == food_pos:
            if food_type == 'red':
                snake_pos.append(snake_pos[-1])
                score += 1 # Menambahkan 1 poin untuk makanan merah
            elif food_type == 'blue':
                snake_pos.extend([snake_pos[-1]] * 2)
                score += 2 # Menambahkan 2 poin untuk makanan biru
            elif food_type == 'purple':
                snake_pos.extend([snake_pos[-1]] * 3)
                score += 3 # Menambahkan 3 poin untuk makanan ungu
            food_pos = [random.randrange(1, (WIDTH//FOOD_SIZE)) * FOOD_SIZE, random.randrange(1, (HEIGHT//FOOD_SIZE)) * FOOD_SIZE]
            food_type = random.choices(['red', 'blue', 'purple'], weights=[80, 15, 5])[0]
        else:
            snake_pos.pop()

        # Gambar ular dan makanan
        screen.fill(WHITE)
        draw_snake(snake_pos)
        draw_food(food_pos, food_type)
        draw_score(score)
        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    start_screen()
    main_game()
    pygame.quit()
    sys.exit()
