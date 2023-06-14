import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE WAR GAME")
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BLACK = (0, 0, 0)
YELLOW = (255, 245, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

MAX_BULLETS = 3
BULLET_VEL = 5

HEALTH_FONT = pygame.font.SysFont("cosmics", 30)
WIN_TEXT_FONT = pygame.font.SysFont("cosmics", 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

FPS = 60
SPACE_SHIP_HEIGHT, SPACE_SHIP_WIGHT = 60, 45
VELOCITY = 4

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
                                            (YELLOW_SPACESHIP_IMAGE, (SPACE_SHIP_HEIGHT, SPACE_SHIP_WIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
                                        (RED_SPACESHIP_IMAGE, (SPACE_SHIP_HEIGHT, SPACE_SHIP_WIGHT)), 270)

SCREEN_IMAGE = pygame.image.load(os.path.join("Assets", "space.png"))
SCREEN = pygame.transform.scale(SCREEN_IMAGE, (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SCREEN, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("HEALTH:" + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH:" + str(yellow_health), True, WHITE)

    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (780, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(text):
    draw_text = WIN_TEXT_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() // 2, HEIGHT / 2 - draw_text.get_height() // 2))
    pygame.display.update()

    pygame.time.delay(5000)


def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    if key_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VELOCITY
    if key_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY
    if key_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT:  # DOWN
        yellow.y += VELOCITY


def red_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VELOCITY - 10 > BORDER.x:
        red.x -= VELOCITY
    if key_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:
        red.x += VELOCITY
    if key_pressed[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if key_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.width < HEIGHT - 15:
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(800, 250, SPACE_SHIP_WIGHT, SPACE_SHIP_HEIGHT)
    yellow = pygame.Rect(50, 250, SPACE_SHIP_WIGHT, SPACE_SHIP_HEIGHT)

    run = True
    clock = pygame.time.Clock()

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == YELLOW_HIT:
                red_health -= 1

            if event.type == RED_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "RED WINS!"
        if yellow_health <= 0:
            winner_text = "YELLOW WINS!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
