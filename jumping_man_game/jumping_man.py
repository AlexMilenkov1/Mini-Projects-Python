import pygame
import os
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(150, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound(os.path.join("audio/jump.mp3"))
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.jump_sound.play()
            self.gravity = -20

    def gravity_apply(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.gravity_apply()
        self.animation_state()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "snail":
            snail_fr_1 = pygame.image.load(os.path.join("graphics/snail/snail1.png")).convert_alpha()
            snail_fr_2 = pygame.image.load(os.path.join("graphics/snail/snail2.png")).convert_alpha()
            self.frames = [snail_fr_1, snail_fr_2]
            y_pos = 300
        else:
            fly_fr_1 = pygame.image.load(os.path.join("graphics/Fly/fly1.png")).convert_alpha()
            fly_fr_2 = pygame.image.load(os.path.join("graphics/Fly/fly2.png")).convert_alpha()
            self.frames = [fly_fr_1, fly_fr_2]
            y_pos = 200

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_obstacles(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_obstacles()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x < -100:
            self.kill()


pygame.font.init()
pygame.init()

bg_music = pygame.mixer.Sound(os.path.join("audio/music.wav"))
bg_music.play(loops=-1)

HEIGHT = 400
WIDTH = 800

FPS = 60

SNAIL_1_VEL = 5


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping man")

# GROUPS
player_cl = pygame.sprite.GroupSingle()
player_cl.add(Player())

obstacles_group = pygame.sprite.Group()

# BACKGROUND
sky = pygame.image.load(os.path.join("graphics", "Sky.png")).convert()
ground = pygame.image.load(os.path.join("graphics", "ground.png")).convert()

# # SNAILS
# snail_frame_1 = pygame.image.load(os.path.join("graphics/snail/snail1.png")).convert_alpha()
# snail_frame_2 = pygame.image.load(os.path.join("graphics/snail/snail2.png")).convert_alpha()
# snail_frame = [snail_frame_1, snail_frame_2]
# snail_frame_index = 0
# snail_surf = snail_frame[snail_frame_index]
#
# # FLY
# fly_frame_1 = pygame.image.load(os.path.join("graphics/Fly/fly1.png")).convert_alpha()
# fly_frame_2 = pygame.image.load(os.path.join("graphics/Fly/fly2.png")).convert_alpha()
# fly_frame = [fly_frame_1, fly_frame_2]
# fly_frame_index = 0
# fly_surf = fly_frame[fly_frame_index]

# PLAYER
# player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
# player_walk = [player_walk_1, player_walk_2]
# player_index = 0
# player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

# player_surf = player_walk[player_index]
# player = player_surf.get_rect(midbottom=(80, 300))

starting_screen = pygame.transform.rotozoom(pygame.image.load("graphics/Player/player_stand.png").convert_alpha(), 0, 2)
starting_screen_rect = starting_screen.get_rect(center=(400, 200))

score_font = pygame.font.Font("font/Pixeltype.ttf", 50)

start_time = 0

current_time = pygame.time.get_ticks()

intro_screen_text = score_font.render("Pixel Runner", False, (128, 176, 167))
intro_screen = intro_screen_text.get_rect(center=(400, 80))

game_msg = score_font.render("Press SPACE to start", False, (128, 176, 167))
game_msg_surf = game_msg.get_rect(center=(400, 340))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer, 500)
#
# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 200)

# obstacle_list = []


def collision_sprite():
    if pygame.sprite.spritecollide(player_cl.sprite, obstacles_group, False):
        obstacles_group.empty()
        return False
    else:
        return True


def drawing():
    WINDOW.blit(sky, (0, 0))
    WINDOW.blit(ground, (0, 300))
    # WINDOW.blit(player_surf, player)
    player_cl.draw(WINDOW)
    obstacles_group.draw(WINDOW)


# def obstacle_movement(obstacle_lists):
#     if obstacle_lists:
#         for object_ in obstacle_lists:
#             object_.x -= SNAIL_1_VEL
#
#             if object_.y == 265:
#                 WINDOW.blit(snail_surf, object_)
#             else:
#                 WINDOW.blit(fly_surf, object_)
#
#         obstacle_lists = [obstacle for obstacle in obstacle_lists if obstacle.x > 100]
#
#         return obstacle_list
#
#     else:
#         return []


# def collisions(player, obstacles):
#     if obstacles:
#         for obj in obstacles:
#             if player.colliderect(obj):
#                 return False
#     return True


# def player_animation():
#     global player_surf, player_index
#
#     if player.bottom < 300:
#         player_surf = player_jump
#     else:
#         player_index += 0.1
#
#         if player_index >= len(player_walk):
#             player_index = 0
#         player_surf = player_walk[int(player_index)]
#

def display_score(start_time):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_text = score_font.render(f"Score: {current_time}", True, (15, 50, 20)).convert_alpha()
    score_surf = score_text.get_rect(center=(400, 50))
    WINDOW.blit(score_text, score_surf)
    return current_time


run = True
clock = pygame.time.Clock()
player_gravity = 0
game_active = False
score = 0

while run:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                    # if player.bottom >= 300:
                    #     player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer:
                obstacles_group.add(Obstacles(random.choice(["fly", "fly", "snail", "snail", "snail"])))
            #     if random.randint(0, 2):
            #         obstacle_list.append(snail_surf.get_rect(topleft=(random.randint(900, 1100), 265)))
            #     else:
            #         obstacle_list.append(fly_surf.get_rect(topleft=(random.randint(900, 1100), 140)))

            # if event.type == snail_animation_timer:
            #     if snail_frame_index == 0:
            #         snail_frame_index = 1
            #     else:
            #         snail_frame_index = 0
            #     snail_surf = snail_frame[snail_frame_index]
            #
            # if event.type == fly_animation_timer:
            #     if fly_frame_index == 0:
            #         fly_frame_index = 1
            #     else:
            #         fly_frame_index = 0
            #     fly_surf = fly_frame[fly_frame_index]

    if game_active:
        # player_gravity += 1
        # player.y += player_gravity
        #
        # if player.bottom >= 300:
        #     player.bottom = 300
        obstacles_group.update()
        player_cl.update()
        game_active = collision_sprite()
        # player_animation()
        drawing()
        # obstacle_list = obstacle_movement(obstacle_list)
        score = display_score(start_time)
        # game_active = collisions(player, obstacle_list)

    else:
        WINDOW.fill((94, 129, 162))
        WINDOW.blit(starting_screen, starting_screen_rect)
        WINDOW.blit(intro_screen_text, intro_screen)

        # obstacle_list.clear()
        # player.midbottom = (80, 300)
        player_gravity = 0

        score_msg = score_font.render(f"Your score: {score}",  False, (128, 176, 167))
        score_msg_rect = score_msg.get_rect(center=(400, 340))
        if score == 0:
            WINDOW.blit(game_msg, game_msg_surf)
        else:
            WINDOW.blit(score_msg, score_msg_rect)

    pygame.display.update()
