import pygame

# Citation: Some code is reused from LAB 3 of the course. Provided by Dr. Nixon

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([4, 10]) # Set size of bullet block
        self.image.fill(pygame.color.THECOLORS['white'])
        self.rect = self.image.get_rect()


    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3


class EnemyBullet(Bullet):
    """ This class represents the enemy bullet. """

    def __init__(self):
        # Call the parent class (Bullet) constructor
        super().__init__()
        self.image.fill(pygame.color.THECOLORS['purple'])

    def update(self):
        """ Move the bullet. """
        self.rect.y += 3  # Move the bullet downwards instead of upwards as enemy shoots down towards the player
