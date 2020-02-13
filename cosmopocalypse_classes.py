import random
import os
import pygame
import cosmopocalypse_constants as cc
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



class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load(os.path.join(cc.BACKGROUND_PATH, "Background1.png")).convert()
        self.image.set_colorkey((cc.BLACK), RLEACCEL)
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        #class for the player
        super(Player, self).__init__()
        #init sprite constructor
        self.image = pygame.image.load(os.path.join(cc.PLAYER_PATH, "PlayerShip001.png")).convert()
        self.image.set_colorkey((cc.BLACK), RLEACCEL)
        self.health = 10
        self.invulnerable = 0
        self.rect = self.image.get_rect(
            center=(
                cc.SCREEN_WIDTH / 2, cc.SCREEN_HEIGHT / 2
            )
        )

    def update(self):
        #this controls player movement, change values to affect speed, also changes sprites
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
            self.image = pygame.image.load(os.path.join(cc.PLAYER_PATH, "PlayerShip003.png")).convert()
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(5, 0)
            self.image = pygame.image.load(os.path.join(cc.PLAYER_PATH, "PlayerShip001.png")).convert()
        #this binds the player to the screen area, can wander off without
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > cc.SCREEN_WIDTH:
            self.rect.right = cc.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= cc.SCREEN_HEIGHT:
            self.rect.bottom = cc.SCREEN_HEIGHT
        #checks
        if self.invulnerable > 0:
            self.invulnerable -= 1
        print("invuln", self.invulnerable)

    def take_damage(self):
        if self.invulnerable == 0:
            self.health -= 1
            self.invulnerable = 300
        if self.health == 0:
            self.kill()



class Bullet(pygame.sprite.Sprite):
    #class for projectiles
    def __init__(self):
        super(Bullet, self).__init__()
        #call sprite constructor
        self.image = pygame.image.load(os.path.join(cc.PROJECTILE_PATH, "Bullet.png")).convert()
        self.image.set_colorkey((cc.BLACK), RLEACCEL)
        self.rect = self.image.get_rect()
        self.speed = (10, 0)

    def update(self, screen):
        #movement for projectiles change values to change speed
        self.rect.move_ip(self.speed)
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > cc.SCREEN_WIDTH:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    #class for enemies
    def __init__(self):
        super(Asteroid, self).__init__()
        self.image = pygame.image.load(os.path.join(cc.ASTEROID_PATH, "Asteroid00" + str(random.randint(1, 4)) + ".png")).convert()
        self.image.set_colorkey((cc.BLACK), RLEACCEL)
        self.speed = random.randint(1, 20)
        self.rect = self.image.get_rect(
            center=(
                random.randint(cc.SCREEN_WIDTH + 20, cc.SCREEN_WIDTH + 100),
                random.randint(0, cc.SCREEN_HEIGHT)
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
        self.image = pygame.image.load(os.path.join(cc.MARSSHIP_PATH, "EnemySpaceship002.png")).convert()
        self.image.set_colorkey((cc.BLACK), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(cc.SCREEN_WIDTH - 20, random.randint(0, cc.SCREEN_HEIGHT))
        )
        self.speed = (-3, 0)
        self.shoot_timer = 5

    def update(self, screen):
        #movement for asteroids
        self.rect.move_ip(self.speed)
        if self.rect.right < 0:
            self.kill()


class MarsDeathStar(pygame.sprite.Sprite):
    def __init__(self):
        super(MarsDeathStar, self).__init__()
        self.image = pygame.image.load(os.path.join(cc.DEATHSTAR_PATH, "DEATHSTAR.png")).convert()
        self.image.set_colorkey((cc.BLACK), RLEACCEL)
        self.rect = self.image.get_rect(center=((cc.SCREEN_WIDTH - 100), (cc.SCREEN_HEIGHT // 2)))
        self.health = 5000
        self.speed = 2
        self.timer = 0

    def update(self, screen, player):
        self.cannon(screen)
        if self.health == 0:
            self.kill()
        # Find directional vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(0, player.rect.y - self.rect.y)
        if dirvect[1] > 0 or dirvect[1] < 0:
        # Move along this normalized vector towards the player at current speed.            
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
        #if the vector is 0 it cannot be normalised, this means boss is at correct level, we pass
        else:
            pass

    def cannon(self, screen):
        self.timer += 1
        if self.timer == 300:
            #call fire
            self.timer = 0

    def fire(self):
        pass

class button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(button, self).__init__()
        self.image = pygame.image.load(os.path.join(cc.BUTTON_PATH, image)).convert()
        self.image.set_colorkey((cc.BLACK), RLEACCEL)
        self.rect = self.image.get_rect(topleft=(x, y))






def draw_text(surf, text, size, x, y, colour):
    font = pygame.font.Font(cc.TITLE_FONT, size)
    text_surface = font.render(text, True, (colour))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
