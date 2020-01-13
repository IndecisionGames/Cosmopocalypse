import pygame
import math
import random

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
        self.bullet_speed = 2
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

#fire rate
#bullet speed
#bullet acceleration

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
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)

    pygame.display.set_caption("Bullet Pattern Test")
     
    screen = pygame.display.set_mode((500,500))
     
    running = True
    clock = pygame.time.Clock()

    gen = PatternGenerator(475, 250)

    while running:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        gen.update()

        # Clear the screen and set the screen background
        screen.fill(BLACK)

        gen.draw(screen)

        # Draw on the screen a GREEN line from (0,0) to (50.75) 
        # 5 pixels wide.
        #pygame.draw.line(screen, GREEN, [0, 0], [50,30], 5)
    
        # Draw on the screen a GREEN line from (0,0) to (50.75) 
        # 5 pixels wide.
        #pygame.draw.lines(screen, WHITE, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)
        
        # Draw on the screen a GREEN line from (0,0) to (50.75) 
        # 5 pixels wide.
        #pygame.draw.aaline(screen, GREEN, [0, 50],[50, 80], True)

        # Draw a rectangle outline
        #pygame.draw.rect(screen, WHITE, [75, 10, 50, 20], 2)
        
        # Draw a solid rectangle
        #pygame.draw.rect(screen, WHITE, [150, 10, 50, 20])
        
        # Draw an ellipse outline, using a rectangle as the outside boundaries
        #pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2) 

        # Draw an solid ellipse, using a rectangle as the outside boundaries
        #pygame.draw.ellipse(screen, RED, [300, 10, 50, 20]) 
    
        # This draws a triangle using the polygon command
        #pygame.draw.polygon(screen, WHITE, [[100, 100], [0, 200], [200, 200]], 5)
    
        # Draw an arc as part of an ellipse. 
        # Use radians to determine what angle to draw.
        #pygame.draw.arc(screen, WHITE,[210, 75, 150, 125], 0, pi/2, 2)
        #pygame.draw.arc(screen, GREEN,[210, 75, 150, 125], pi/2, pi, 2)
        #pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi,3*pi/2, 2)
        #pygame.draw.arc(screen, RED,  [210, 75, 150, 125], 3*pi/2, 2*pi, 2)
        
        # Draw a circle
        #pygame.draw.circle(screen, BLUE, [60, 250], 40)
        
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
     
if __name__=="__main__":
    main()