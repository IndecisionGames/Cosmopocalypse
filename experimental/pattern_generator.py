import pygame
import math
import random

class Player:
    def __init__(self, x, y):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.colour = (r, g, b)
        self.x = x
        self.y = y
        self.width = 20
        self.height = 15
        self.speed = 5

    def move(self, vertical=0, horizontal=0):
        self.y += vertical * self.speed
        if self.y > 480:
            self.y = 480
        if self.y < 0:
            self.y = 0

        # Comment below section to disable horizontal movement
        self.x += horizontal * self.speed
        if self.x > 400:
            self.x = 400
        if self.x < 20:
            self.x = 20

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [self.x, self.y, self.width, self.height])

class Bullet:
    def __init__(self, x, y, speed):
        self.colour = ()
        self.x = x
        self.y = y
        self.xr = 16
        self.yr = 8
        self.speed = speed
        self.alive = True

    def randomiseColour(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.colour = (r, g, b)

    def playerBullets(self):
        self.colour = (255, 201, 34)
        self.xr = 10
        self.yr = 4
        self.speed *= 3

    def update(self):
        self.x += self.speed
        if self.x < 0:
            self.alive = False
        if self.x > 500:
            self.alive = False

    def isAlive(self):
        return self.alive

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.colour, [self.x, self.y, self.xr, self.yr]) 


class PatternGenerator:
    def __init__(self, x, y, playerGuns):
        self.x = x
        self.y = y
        self.bullet_speed = 4
        self.bullets = []
        self.fire_rate = 20
        self.fire_rate_counter = 0
        self.playerGuns = playerGuns

    def update(self):
        if self.fire_rate_counter == 0:
            b = Bullet(self.x, self.y, self.bullet_speed)
            if self.playerGuns:
                b.playerBullets()
            else:
                b.randomiseColour()
            self.bullets.append(b)
            self.fire_rate_counter = self.fire_rate
        else:
            self.fire_rate_counter -= 1

        for bullet in self.bullets:
            bullet.update()
            if not bullet.isAlive():
                self.bullets.remove(bullet)
        
    def updateLocation(self, x, y):
        self.x = x
        self.y = y
    
    def updateDirection(self, d):
        self.bullet_speed *= d

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)


#https://www.youtube.com/watch?v=xbQ9e0zYuj4 
#https://www.youtube.com/watch?v=GDs3QEbV_l0
#bullets per array
#individual array spread

#total bullet arrays
#total array spread

#current spin speed
#spin speed change rate
#spin reversal
#max spin speed

#object width
#object height
#x offset
#y offset

#track bullets on screen
#fps on screen

def main():
     
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)

    pygame.display.set_caption("Bullet Pattern Test")
    screen = pygame.display.set_mode((500,500))
     
    running = True
    clock = pygame.time.Clock()

    gen = PatternGenerator(475, 250, False)
    gen.updateDirection(-1)
    p = Player(25, 225)
    p_hmove = 0
    p_vmove = 0
    lgun = PatternGenerator(35, 223, True)
    rgun = PatternGenerator(35, 238, True)

    # Game loop
    while running:

        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            p_vmove = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            p_vmove = 1
        else:
            p_vmove = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            p_hmove = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            p_hmove = 1
        else:
            p_hmove = 0

        # Updates
        gen.update()
        p.move(p_vmove, p_hmove)
        lgun.updateLocation(p.x + 10, p.y - 2)
        rgun.updateLocation(p.x + 10, p.y + 13)
        lgun.update()
        rgun.update()


        # Draw
        screen.fill(BLACK)
        gen.draw(screen)
        p.draw(screen)
        lgun.draw(screen)
        rgun.draw(screen)
        pygame.display.flip()
     
if __name__=="__main__":
    main()