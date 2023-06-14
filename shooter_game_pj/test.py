import os
import pygame

pygame.font.init()

WIDTH = 900
HEIGHT = 500
SPACESHIP_WIDTH = 60
SPACESHIP_HEIGHT = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

VELOCITY = 4
BULLET_VELOCITY = 6
MAX_BULLETS = 3

BORDER = pygame.Rect(WIDTH / 2 + 5, 0, 10, HEIGHT)

FPS = 60

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("cosmics", 30)
WINNER_FONT = pygame.font.SysFont("cosmics", 100)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STAR WARS")

SPACE_IMAGE = pygame.image.load(os.path.join("Assets", "space.png"))
SPACE_BACKGROUND = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def drawing(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health):
    WINDOW.blit(SPACE_BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), True, WHITE)

    WINDOW.blit(red_health_text, (10, 10))
    WINDOW.blit(yellow_health_text, (780, 10))
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    pygame.display.update()


def winner(text):
    text_winner = WINNER_FONT.render(text, True, WHITE)
    WINDOW.blit(text_winner, (WIDTH / 2 - text_winner.get_width() // 2, HEIGHT / 2 - text_winner.get_height() // 2))
    pygame.display.update()

    pygame.time.delay(4000)


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x + bullet.width > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT:
        red.y += VELOCITY


def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT:
        yellow.y += VELOCITY


def main():
    run = True
    clock = pygame.time.Clock()

    red = pygame.Rect(820, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(30, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < 3:
                    bullet = pygame.Rect(yellow.x + yellow.width - 10, yellow.y + yellow.height // 2 - 5, 10, 7)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < 3:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 5, 10, 7)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
        if yellow_health <= 0:
            winner_text = "RED WINS!"
        if winner_text != "":
            winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        drawing(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
