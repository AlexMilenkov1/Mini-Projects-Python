import pygame as py
import os
import time
import random
py.font.init()

WIDTH, HEIGHT = 750, 750
SHIP_WIDTH, SHIP_HEIGHT = 50, 50

FPS = 60

WHITE = (255, 255, 255)

SHIP_VEL = 5
BULLET_VEL = 4

LEVEL_FONT = py.font.SysFont("comics", 35)
LIVES_FONT = py.font.SysFont("comics", 35)
LOST_FONT = py.font.SysFont("comics", 60)

WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("SPACE SHOOT GAME")

BG = py.image.load(os.path.join("assets", "background-black.png"))
BG_set = py.transform.scale(BG, (WIDTH, HEIGHT))

BLUE_LASER_IMAGE = py.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER_IMAGE = py.image.load(os.path.join("assets", "pixel_laser_green.png"))
RED_LASER_IMAGE = py.image.load(os.path.join("assets", "pixel_laser_red.png"))
YELLOW_LASER_IMAGE = py.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

BLUE_SHIP_IMAGE = py.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SHIP_IMAGE = py.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
RED_SHIP_IMAGE = py.image.load(os.path.join("assets", "pixel_ship_red_small.png"))

YELLOW_SHIP_IMAGE = py.image.load(os.path.join("assets", "pixel_ship_yellow.png"))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lases = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = py.mask.from_surface(img)

    def move(self, vel):
        self.y -= vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def off_screen(self, height):
        return self.y <= height and self.y >= 0

    def collision(self, obj):
        return collide(self, obj)


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = YELLOW_SHIP_IMAGE
        self.laser_image = YELLOW_LASER_IMAGE
        self.mask = py.mask.from_surface(self.ship_image)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP_IMAGE, RED_LASER_IMAGE),
        "blue": (BLUE_SHIP_IMAGE, BLUE_LASER_IMAGE),
        "green": (GREEN_SHIP_IMAGE, GREEN_LASER_IMAGE)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.COLOR_MAP[color]
        self.mask = py.mask.from_surface(self.ship_image)

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    off_set_x = obj2.x - obj1.x
    off_set_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (off_set_x, off_set_y)) is not None


def main():
    run = True
    clock = py.time.Clock()

    level = 0
    lives = 5

    player = Player(300, 650)

    enemies = []
    wave_length = 5
    enemy_vel = 1.5

    lost = False
    lost_count = 0

    bullets = []

    def drawing(levels, lives_):
        WIN.blit(BG_set, (0, 0))
        text_level = LEVEL_FONT.render("LEVEL: " + str(levels), True, WHITE)
        lives_text = LIVES_FONT.render("LIVES: " + str(lives_), True, WHITE)

        WIN.blit(text_level, (630, 10))
        WIN.blit(lives_text, (15, 10))

        player.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        if lost:
            lost_text = LOST_FONT.render("YOU LOST!", True, WHITE)
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, 350))

        py.display.update()

    while run:
        clock.tick(FPS)
        drawing(level, lives)

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            enemy_vel += 0.1
            wave_length += 2

            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 50), random.randrange(-800, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in py.event.get():
            if event.type == py.QUIT:
                quit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_LCTRL:
                    bullet = py.Rect(player.x + player.get_width() / 2, player.y, 15, 5)
                    bullets.append(bullet)

        def main_movement(key_pressed):
            if key_pressed[py.K_d] and player.x + player.get_width() < WIDTH + 5:
                player.x += SHIP_VEL
            if key_pressed[py.K_a] and player.x > -5:
                player.x -= SHIP_VEL
            if key_pressed[py.K_w] and player.y > -5:
                player.y -= SHIP_VEL
            if key_pressed[py.K_s] and player.y + player.get_height() < HEIGHT - 5:
                player.y += SHIP_VEL

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        keys_pressed = py.key.get_pressed()
        main_movement(keys_pressed)


if __name__ == "__main__":
    main()
