import os

import pygame

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 40

DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 500
DISPLAY_COLOR = (20, 20, 20)
FPS = 60

VEL = 4

WINDOW = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Game Practice")

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)


def red_movement(key_pressed, red):
    if key_pressed[pygame.K_a]:
        red.x -= VEL
    if key_pressed[pygame.K_d]:
        red.x += VEL
    if key_pressed[pygame.K_w]:
        red.y -= VEL
    if key_pressed[pygame.K_s]:
        red.y += VEL


def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_LEFT]:
        yellow.x -= VEL
    if key_pressed[pygame.K_RIGHT]:
        yellow.x += VEL
    if key_pressed[pygame.K_UP]:
        yellow.y -= VEL
    if key_pressed[pygame.K_DOWN]:
        yellow.y += VEL


def drawing(red, yellow):
    WINDOW.fill(DISPLAY_COLOR)
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    red = pygame.Rect(800, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(50, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        drawing(red, yellow)
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        yellow_movement(keys_pressed, yellow)

    pygame.quit()


if __name__ == "__main__":
    main()
