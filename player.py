import pygame
import os

# Citation: Some code is reused from LAB 3 of the course. Provided by Dr. Nixon

class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        url = os.path.join(script_dir, "shooter.png")
        # citation: https://www.pngkey.com/download/u2w7w7a9y3y3i1e6_laser-cannon-space-invaders-player-sprite/
        original_image = pygame.image.load(url)
        self.image = pygame.transform.scale(original_image, (30, 30)) # Set size of player block
        self.rect = self.image.get_rect()


    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position as a list of two numbers.
        pos = pygame.mouse.get_pos()
        # Set the player x position to the mouse x position
        self.rect.x = pos[0]
        # If out of bounds, the following ensures player is within the boundary
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 640:
            self.rect.right = 640
