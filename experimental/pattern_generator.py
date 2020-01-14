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
        self.height = 16
        self.speed = 5

    def move(self, direction):
        self.y += direction * self.speed
        if self.y > 480:
            self.y = 480
        if self.y < 0:
            self.y = 0

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

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.alive = False

    def isAlive(self):
        return self.alive

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.colour, [self.x, self.y, self.xr, self.yr]) 


class PatternGenerator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullet_speed = 4
        self.bullets = []
        self.fire_rate = 20
        self.fire_rate_counter = 0

    def update(self):
        
        if self.fire_rate_counter == 0:
            b = Bullet(self.x, self.y, self.bullet_speed)
            b.randomiseColour()
            self.bullets.append(b)
            self.fire_rate_counter = self.fire_rate
        else:
            self.fire_rate_counter -= 1

        for bullet in self.bullets:
            bullet.update()
            if not bullet.isAlive():
                self.bullets.remove(bullet)
        
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

    gen = PatternGenerator(475, 250)
    p = Player(25, 225)
    p_move = 0

    # Game loop
    while running:

        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p_move = -1
                if event.key == pygame.K_DOWN:
                    p_move = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    p_move = 0

        # Updates
        gen.update()
        p.move(p_move)


        # Draw
        screen.fill(BLACK)
        gen.draw(screen)
        p.draw(screen)
        pygame.display.flip()
     
if __name__=="__main__":
    main()