import pygame
import cosmopocalypse_constants as cc
import cosmopocalypse_classes as ccl
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

class SceneBase():
    #base class for each game scene
    def __init__(self):
        self.next = self

    def ProcessInput(self):
        print("override ProcessInput")

    def Update(self, screen):
        print("override Update")

    def Render(self, screen):
        print("override Render")

    def SwitchScene(self, next_scene):
        self.next = next_scene

class SplashScreen(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.next = next
        self.count = 0

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_e:
                    self.SwitchScene(TitleScene())

    def Update(self, screen):
        self.count += 1
        if self.count > 600:
            self.SwitchScene(TitleScene)

    def Render(self, screen):
        screen.fill((0, 0, 0))

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.next = self
        self.play_button = ccl.button(cc.SCREEN_WIDTH // 2, cc.SCREEN_HEIGHT // 2, "PlayButton.png")

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_e:
                    self.SwitchScene(LevelOne())
        mouse = pygame.mouse.get_pos()
        #play button
        if mouse[0] >= self.play_button.rect.x and mouse[0] <= self.play_button.rect.x + 100:
            if mouse[1] >= self.play_button.rect.y and mouse[1] <= self.play_button.rect.y + 100:
                self.SwitchScene(LevelOne)

    def Update(self, screen):
        pass

    def Render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.play_button.image, self.play_button.rect)
        ccl.draw_text(screen, "COSMOPOCALYPSE", 80, cc.SCREEN_WIDTH / 2, 10, cc.RED)

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
        self.background = ccl.Background()
        self.player = ccl.Player()
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
                    bullet = ccl.Bullet()
                    bullet.rect.x = self.player.rect.x + 30
                    bullet.rect.y = self.player.rect.y + 17
                    self.projectiles.add(bullet)
                    self.all_sprites.add(bullet)


            elif event.type == self.ADDENEMY:
                new_enemy = ccl.Asteroid()
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

        self.projectiles.update(screen)
        self.enemyprojectiles.update(screen)
        self.ships.update(screen)
        self.boss.update(screen, self.player)
        self.asteroids.update()
        self.player.update()
        if pygame.sprite.spritecollideany(self.player, self.asteroids):
            self.player.take_damage()

        self.timer += 1

        #remove garbage timer usage
        if self.timer > 600 and self.timer <= 601:
            ship = ccl.MarsShip()
            self.all_sprites.add(ship)
            self.ships.add(ship)

        if self.timer > 1200 and self.timer <= 1201:
            self.Deathstar = ccl.MarsDeathStar()
            self.all_sprites.add(self.Deathstar)
            self.boss.add(self.Deathstar)

        for i in self.ships:
            marsbullet = ccl.Bullet()
            self.all_sprites.add(marsbullet)
            self.enemyprojectiles.add(marsbullet)

    def Render(self, screen):
        screen.fill((0, 0, 0))
        for i in self.all_sprites:
            screen.blit(i.image, i.rect)
        ccl.draw_text(screen, "Score: " + str(self.score), 22, 700, 550, cc.RED)
        ccl.draw_text(screen, "Health: " + str(self.player.health), 22, 100, 550, cc.GREEN)

        if self.timer > 1201:
            pygame.draw.rect(screen, (cc.LIME_GREEN), pygame.Rect(self.Deathstar.rect.left + 49, self.Deathstar.rect.top + 63, 8, -45*self.Deathstar.timer//300))
