import random
import pygame
import cosmopocalypse_constants
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_UP, K_w,
    K_DOWN, K_s,
    K_LEFT, K_a,
    K_RIGHT, K_d,
    K_e,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()





class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load("Background1.png").convert()
        self.image.set_colorkey((BLACK), RLEACCEL)
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        #class for the player
        super(Player, self).__init__()
        #init sprite constructor
        self.image = pygame.image.load("PlayerShip001.png").convert()
        self.image.set_colorkey((BLACK), RLEACCEL)
        self.health = 1000
        self.rect = self.image.get_rect(
            center=(
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
            )
        )

    def update(self):
        #this controls player movement, change values to affect speed, also changes sprites
        #FIX: currently bound to each frame
        pressed_keys = pygame.key.get_pressed()
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
        self.image.set_colorkey((BLACK), RLEACCEL)
        self.rect = self.image.get_rect()
        self.speed = (10, 0)

    def update(self):
        #movement for projectiles change values to change speed
        self.rect.move_ip(self.speed)
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    #class for enemies
    def __init__(self):
        super(Asteroid, self).__init__()
        self.image = pygame.image.load("Asteroid00" + str(random.randint(1, 4)) + ".png").convert()
        self.image.set_colorkey((BLACK), RLEACCEL)
        self.speed = random.randint(1, 20)
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        #movement for asteroids
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class MarsShip(pygame.sprite.Sprite):
    #red and green ships of mars
    def __init__(self):
        super(MarsShip, self).__init__()
        self.image = pygame.image.load("EnemySpaceship002.png").convert()
        self.image.set_colorkey((BLACK), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH - 20, random.randint(0, SCREEN_HEIGHT))
        )
        self.speed = (-3, 0)

    def update(self):
        #movement for asteroids
        self.rect.move_ip(self.speed)
        if self.rect.right < 0:
            self.kill()


class MarsDeathStar(pygame.sprite.Sprite):
    def __init__(self):
        super(MarsDeathStar, self).__init__()
        self.image = pygame.image.load("DEATHSTAR001.png").convert()
        self.image.set_colorkey((BLACK), RLEACCEL)
        self.rect = self.image.get_rect(center=((SCREEN_WIDTH - 50), (SCREEN_HEIGHT // 2)))
        self.health = 5000
        self.speed = 5
        self.timer = 0

    def update(self, player):
        self.cannon()
        if self.health == 0:
            self.kill()
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)
        if self.rect.left < 700:
            self.rect.left = 700

    def cannon(self):
        self.timer += 1
        if self.timer == 120:
            self.image = pygame.image.load("DEATHSTAR002.png").convert()
        if self.timer == 240:
            self.image = pygame.image.load("DEATHSTAR003.png").convert()
        if self.timer == 360:
            self.image = pygame.image.load("DEATHSTAR004.png").convert()
        if self.timer == 480:
            self.image = pygame.image.load("DEATHSTAR005.png").convert()
