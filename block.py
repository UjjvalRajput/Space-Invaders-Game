import pygame
import os

# Citation: Some code is reused from LAB 3 of the course. Provided by Dr. Nixon

class Block(pygame.sprite.Sprite):
    """ This class represents the blocks. """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Finding the path to the image and assigning image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        url = os.path.join(script_dir, "rock.png")
        # citation: https://www.vecteezy.com/png/21680158-cartoon-mountain-rock-clip-art
        original_image = pygame.image.load(url)
        self.image = pygame.transform.scale(original_image, (20, 15)) # Set size of block
        self.rect = self.image.get_rect()
