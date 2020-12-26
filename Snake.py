import pygame
import sys
import random
import math


def movement():
    if direction == 1:
        snake.y -= 10
    if direction == 2:
        snake.y += 10
    if direction == 3:
        snake.x -= 10
    if direction == 4:
        snake.x += 10


def collision():
    global snake_pos_x, snake_pos_y, snake_list
    if ball.colliderect(snake):
        ball.x = math.ceil((random.randint(0, screen_width - 10)) / 10) * 10
        ball.y = math.ceil((random.randint(0, screen_height - 10)) / 10) * 10
        new_snake = pygame.Rect(snake_pos_x, snake_pos_y, 10, 10)
        snake_list.append(new_snake)
        pygame.mixer.Sound.play(point_sound)

    if (snake.x >= screen_width) or (snake.x < 0) or (snake.y >= screen_height) or (snake.y < 0):
        pygame.quit()
        sys.exit()

    new_snakes = snake_list[1:len(snake_list)]
    for x in new_snakes:
        if len(new_snakes) <= 1:
            break
        elif x.x == snake.x and x.y == snake.y:
            pygame.quit()
            sys.exit()


def draw_snake():
    global snake_list
    new_snakes = snake_list[1:len(snake_list)]
    pygame.draw.rect(screen, (0, 100, 0), snake)
    for x in new_snakes:
        pygame.draw.rect(screen, (0, 80, 0), x)


def move_snake():
    global snake_list
    for x in range(len(snake_list), 1, -1):
        snake_list[x-1].x = snake_list[x-2].x
        snake_list[x-1].y = snake_list[x-2].y


pygame.init()

screen_width = 500
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PySnake")
clock = pygame.time.Clock()

snake = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 10, 10)
snake_list = [snake]
ball_location_x = math.ceil((random.randint(0, screen_width - 10)) / 10) * 10
ball_location_y = math.ceil((random.randint(0, screen_height - 10)) / 10) * 10
ball = pygame.Rect(ball_location_x, ball_location_y, 10, 10)

direction = random.randint(1, 4)
paused = -1

point_sound = pygame.mixer.Sound("point.wav")
pause_sound = pygame.mixer.Sound("pause.ogg")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                paused *= -1
                pygame.mixer.Sound.play(pause_sound)
            if event.key == pygame.K_UP:
                if direction != 2:
                    direction = 1
            if event.key == pygame.K_DOWN:
                if direction != 1:
                    direction = 2
            if event.key == pygame.K_LEFT:
                if direction != 4:
                    direction = 3
            if event.key == pygame.K_RIGHT:
                if direction != 3:
                    direction = 4

    if paused < 0:
        if len(snake_list) > 1:
            move_snake()
        snake_pos_x = snake_list[-1].x
        snake_pos_y = snake_list[-1].y
        movement()
        collision()

    screen.fill((20, 20, 20))
    pygame.draw.rect(screen, (200, 200, 200), ball)
    draw_snake()

    pygame.display.flip()
    clock.tick(10)
