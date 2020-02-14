import pygame
import cosmopocalypse_constants as cc
import cosmopocalypse_classes as ccl
import Levels


def run_game():

    pygame.init()

    #set caption
    pygame.display.set_caption("Cosmopocalypse")

    #this sets display size
    screen = pygame.display.set_mode((cc.SCREEN_WIDTH, cc.SCREEN_HEIGHT))

    #init clock obj, limits fps
    clock = pygame.time.Clock()




    #set opening scene !!!!! set to splash screen eventually
    active_scene = Levels.SplashScreen()

    #this is the game loop
    while active_scene is not None:
        #updates for active scene
        active_scene.ProcessInput()
        active_scene.Update(screen)
        active_scene.Render(screen)

        #checks each frame if scene is changing
        active_scene = active_scene.next

        #update the screen
        pygame.display.flip()

        #arg = max fps
        clock.tick(60)

        #print("fps", clock.get_fps())



if __name__ == "__main__":
    run_game()
