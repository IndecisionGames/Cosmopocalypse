import random
import math
import pygame
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

####
#    classes
####

class SceneBase():
    #base class for each game scene
    def __init__(self):
        self.next = self

    def ProcessInput(self):
        print("override ProcessInput")

    def Update(self):
        print("override Update")

    def Render(self):
        print("override Render")

    def SwitchScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        active_scene = None

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.next = self

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_e:
                    self.SwitchScene(LevelOne())

    def Update(self, screen):
        pass

    def Render(self, screen):
        screen.fill((0, 0, 0))
        draw_text(screen, "COSMOPOCALYPSE", 80, SCREEN_WIDTH / 2, 10)

class LevelOne(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.next = self
        self.score = 0
        self.timer = 0
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemyprojectiles = pygame.sprite.Group()
        self.ships = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.background = Background()
        self.player = Player()
        self.all_sprites.add(self.background)
        self.all_sprites.add(self.player)
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_e:
                    self.SwitchScene(TitleScene())
                elif event.key == K_SPACE:
                    bullet = Bullet()
                    bullet.rect.x = self.player.rect.x + 30
                    bullet.rect.y = self.player.rect.y + 17
                    self.projectiles.add(bullet)
                    self.all_sprites.add(bullet)

            elif event.type == self.ADDENEMY:
                new_enemy = Asteroid()
                self.asteroids.add(new_enemy)
                self.all_sprites.add(new_enemy)

    def Update(self, screen):
        kills = pygame.sprite.groupcollide(self.projectiles, self.asteroids, True, True)
        for i in kills:
            self.score += 150

        kills = pygame.sprite.groupcollide(self.projectiles, self.ships, True, True)
        for i in kills:
            self.score += 500

        self.projectiles.update()
        self.enemyprojectiles.update()
        self.ships.update()
        self.boss.update(self.player)
        self.asteroids.update()
        self.player.update()
        if pygame.sprite.spritecollideany(self.player, self.asteroids):
            self.player.health = self.player.health - 1
            if self.player.health == 0:
                self.player.kill()

        self.timer += 1

        if self.timer > 600 and self.timer <= 601:
            ship = MarsShip()
            self.all_sprites.add(ship)
            self.ships.add(ship)

        if self.timer > 1200 and self.timer <= 1201:
            self.Deathstar = MarsDeathStar()
            self.all_sprites.add(self.Deathstar)
            self.boss.add(self.Deathstar)

        for i in self.ships:
            marsbullet = Bullet()
            self.all_sprites.add(marsbullet)
            self.enemyprojectiles.add(marsbullet)

    def Render(self, screen):
        screen.fill((0, 0, 0))
        for i in self.all_sprites:
            screen.blit(i.image, i.rect)
        draw_text(screen, "Score: " + str(self.score), 22, 700, 550)
        draw_health(screen, "Health: " + str(self.player.health), 22, 100, 550)

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load("Background1.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        #class for the player
        super(Player, self).__init__()
        #init sprite constructor
        self.image = pygame.image.load("PlayerShip001.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
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
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
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
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
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
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
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
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
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



####
#   constants
####

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TITLE_FONT = "NebulousV54.ttf"

####
#    main
####

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(TITLE_FONT, size)
    text_surface = font.render(text, True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_health(surf, text, size, x, y):
    font = pygame.font.Font(TITLE_FONT, size)
    text_surface = font.render(text, True, (0, 255, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def run_game(starting_scene):
    pygame.init()

    pygame.display.set_caption("Cosmopocalypse")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        active_scene.ProcessInput()
        active_scene.Update(screen)
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(60)

run_game(TitleScene())
