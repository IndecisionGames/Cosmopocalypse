import pygame
import cosmopocalypse_constants
import cosmopocalypse_classes
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

class LevelOne(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        #FIX: standardise attributes between levels, apply to scenebase
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

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False            
            elif event.type == pygame.KEYDOWN:
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
        #FIX:, use list.len() change formula
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

        #remove garbage timer usage
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
