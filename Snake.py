import pygame
import sys
import random


def movement():
    if direction == 1:
        snake.y -= movement_speed
    if direction == 2:
        snake.y += movement_speed
    if direction == 3:
        snake.x -= movement_speed
    if direction == 4:
        snake.x += movement_speed


def collision():
    global snake_pos_x, snake_pos_y, snake_list, score, game_over
    if ball.colliderect(snake):
        ball.x = random.choice(x_coordinates)
        ball.y = random.choice(y_coordinates)
        new_snake = pygame.Rect(snake_pos_x, snake_pos_y, 20, 20)
        snake_list.append(new_snake)
        score += 1
        pygame.mixer.Sound.play(point_sound)

    if (snake.x >= screen_width) or (snake.x < 0) or (snake.y >= screen_height) or (snake.y < 0):
        snake.x = screen_width / 2
        snake.y = screen_height / 2 - 10
        snake_list = [snake]
        pygame.mixer.Sound.play(game_over_sound)
        game_over = True

    for x in snake_list[1:len(snake_list)]:
        if len(snake_list) <= 1:
            break
        elif x.x == snake.x and x.y == snake.y:
            snake.x = screen_width / 2
            snake.y = screen_height / 2 - 10
            snake_list = [snake]
            pygame.mixer.Sound.play(game_over_sound)
            game_over = True


def draw_snake():
    global snake_list
    new_snakes = snake_list[1:len(snake_list)]
    pygame.draw.rect(screen, (120, 0, 140), snake)
    for x in new_snakes:
        pygame.draw.rect(screen, (100, 0, 120), x)


def move_snake():
    global snake_list
    for x in range(len(snake_list), 1, -1):
        snake_list[x-1].x = snake_list[x-2].x
        snake_list[x-1].y = snake_list[x-2].y


pygame.init()

screen_width = 600
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PySnake")
clock = pygame.time.Clock()

snake = pygame.Rect(screen_width / 2, screen_height / 2 - 10, 20, 20)
snake_list = [snake]
x_coordinates = [x for x in range(0, screen_width - 20, 20)]
y_coordinates = [y for y in range(0, screen_height - 20, 20)]
ball_location_x = random.choice(x_coordinates)
ball_location_y = random.choice(y_coordinates)
ball = pygame.Rect(ball_location_x, ball_location_y, 20, 20)
game_over_screen = pygame.Rect(screen_width / 2 - 150, screen_height / 2 - 100, 300, 200)
movement_speed = 20

direction = random.randint(1, 4)
paused = -1
game_over = False

point_sound = pygame.mixer.Sound("point.wav")
pause_sound = pygame.mixer.Sound("pause.ogg")
game_over_sound = pygame.mixer.Sound("gameOver.ogg")
movement_sound = pygame.mixer.Sound("movement.ogg")

score = 0
paused_font = pygame.font.Font("freesansbold.ttf", 16)
game_over_font = pygame.font.Font("freesansbold.ttf", 30)
score_font = pygame.font.Font("freesansbold.ttf", 20)
retry_font = pygame.font.Font("freesansbold.ttf", 15)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                paused *= -1
                pygame.mixer.Sound.play(pause_sound)
            if event.key == pygame.K_SPACE:
                if game_over:
                    score = 0
                    game_over = False
            if event.key == pygame.K_UP:
                if direction != 2:
                    direction = 1
                    pygame.mixer.Sound.play(movement_sound)
            if event.key == pygame.K_DOWN:
                if direction != 1:
                    direction = 2
                    pygame.mixer.Sound.play(movement_sound)
            if event.key == pygame.K_LEFT:
                if direction != 4:
                    direction = 3
                    pygame.mixer.Sound.play(movement_sound)
            if event.key == pygame.K_RIGHT:
                if direction != 3:
                    direction = 4
                    pygame.mixer.Sound.play(movement_sound)

    if not game_over:
        if paused < 0:
            if len(snake_list) > 1:
                move_snake()
            snake_pos_x = snake_list[-1].x
            snake_pos_y = snake_list[-1].y
            movement()
            collision()

        screen.fill((20, 20, 20))
        if paused > 0:
            paused_text = paused_font.render("PAUSED", False, (200, 200, 200))
            screen.blit(paused_text, (10, 10))
        draw_snake()
        pygame.draw.ellipse(screen, (200, 200, 200), ball)
    else:
        game_over_text = game_over_font.render("GAME OVER!", False, (200, 200, 200))
        score_text = score_font.render(f"Score: {score}", False, (200, 200, 200))
        retry_text = retry_font.render("Press SPACE to play again", False, (200, 200, 200))
        exit_text = retry_font.render("Press ESC to exit", False, (200, 200, 200))
        screen.fill((20, 20, 20))
        pygame.draw.rect(screen, (40, 40, 40), game_over_screen)
        screen.blit(game_over_text, (game_over_screen.x + 52, game_over_screen.y + 20))
        screen.blit(score_text, (game_over_screen.x + 110, game_over_screen.y + 90))
        screen.blit(retry_text, (game_over_screen.x + 55, game_over_screen.y + game_over_screen.height - 50))
        screen.blit(exit_text, (game_over_screen.x + 55, game_over_screen.y + game_over_screen.height - 30))

    pygame.display.flip()
    clock.tick(10)
