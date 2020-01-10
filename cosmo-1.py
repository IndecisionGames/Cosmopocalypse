import time
import os
import random
import pygame
import sys
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_UP, K_w,
    K_DOWN, K_s,
    K_LEFT, K_a,
    K_RIGHT, K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

##############
#  classes   #
##############

class SceneBase():
    #base class for each game scene
    def __init__(self):
        self.next = self

    def ProcessInput(self, pressed_keys):
        print("override ProcessInput")

    def Update(self):
        print("override Update")

    def Render(self):
        print("override Render")

    def SwitchScene(self, next_scene):
        self.next = next_scene

#class DeathStar(pygame.sprite.Sprite):
#    def __init__(self):
#        super(Deathstar, self).__init__()
#        self.image = 
#        self.image.set_colorkey((0, 0, 0), RLEACCEL)
#        self.rect = self.image.get_rect()
#        self.health = 5000
#        self.speed = 5

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load("Background1.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    #class for the player
    def __init__(self):
        super(Player, self).__init__()
        #init sprite constructor
        self.image = pygame.image.load("PlayerShip001.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()
        self.health = 1000

    def update(self, pressed_keys):
        #this controls player movement, change values to affect speed, also changes sprites
        #FIX: currently bound to each frame
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
            self.image = pygame.image.load("PlayerShip003.png").convert()
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(5, 0)
            self.image = pygame.image.load("PlayerShip001.png").convert()
        #this binds the player to the screen area, can wander off without
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    #class for projectiles
    def __init__(self):
        super(Bullet, self).__init__()
        #call sprite constructor
        self.image = pygame.image.load("Bullet.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()

    def update(self):
        #movement for projectiles change values to change speed
        self.rect.move_ip(10, 0)
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    #class for enemies
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("Asteroid00" + str(random.randint(1,4)) + ".png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(1, 20)

    def update(self):
        #movement for enemies
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_health(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, (0, 255, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

###############
#  constants  #
###############

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FONT_NAME = "NebulousV54.ttf"




def main():

    pygame.display.set_caption("Cosmopocalypse")

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 150)

    score = 0

    game_pause = False


    #different sprite groups
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    background = Background()
    all_sprites.add(background)

    #instance player
    player = Player()
    all_sprites.add(player)

    #dont touch this
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_pause = True
                    draw_text(screen, "PAUSED", 120, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    pygame.display.flip()
                    while game_pause:
                        for event1 in pygame.event.get():
                            if event1.type == KEYDOWN:
                                if event1.key == K_ESCAPE:
                                    game_pause = False
                                    clock.tick(30)
                                elif event1.type == QUIT:
                                    running = False




                elif event.key == K_SPACE:
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 40
                    bullet.rect.y = player.rect.y + 20
                    projectiles.add(bullet)
                    all_sprites.add(bullet)

            elif event.type == QUIT:
                running = False

            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)


        #handles inputs for player
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)


        #sets the background colour for the screen, currently black
        screen.fill((0, 0, 0,))

        #set all the sprites on the screen-
        for i in all_sprites:
            screen.blit(i.image, i.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            player.health = player.health - 1
            if player.health == 0:
                player.kill()
                running = False

        #move enemies and projectiles
        enemies.update()
        projectiles.update()

        #checks if projectiles and enemies have collided, if so kill both
        kills = pygame.sprite.groupcollide(projectiles, enemies, True, True)
        for i in kills:
            score += 150

        draw_text(screen, "Score: " + str(score), 22, 700, 550)
        draw_health(screen, "Health: " + str(player.health), 22, 100, 550)

        #this updates the display
        pygame.display.flip()
        #this is an fps cap
        clock.tick(60)


main()
