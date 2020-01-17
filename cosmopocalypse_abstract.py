import pygame

pygame.init()






#classes




class Player(pygame.sprite.Sprite):
    def __init__(self):
        """ Description
        player class calls pygame sprite method to create a player on screen
        :param Pygame.sprite.Sprite
        :return None
        """
    def update(self):
        """ Description
        Moves the player and shoots according to input from user,
        binds player to screen
        :param pressed_keys pygame SDL_2 keyboard inputs
        :return None
        """

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        """ Description
        calls a pygame sprite method to create a projectile tied to player
        :paramm None
        :return None
        """
    def update(self):
        """ Description
        moves the projectile a set distance each frame
        if projectile leaves screen, projectile is destroyed
        :param None
        :return None
        """

class SceneBase():
    def __init__(self):
        """ Description
        creates structure for each scene in game,
        allows switching between multiple scenes
        :param None
        :return None
        """

    def ProcessInput(self):
        """ Description
        accept input from user or objects
        :param None
        :Return None
        """

    def Update(self):
        """ Description
        update player and other game objects
        :param None
        :return None
        """

    def Render(self):
        """ Description
        Draw all game objects onto the current game screen
        :param None
        :Return None
        """

    def SwitchScene(self, next_scene):
        """ Description
        Walks the game to the next scene in the list on param fulfilment
        :param call to init the next scene
        :Return None
        """
