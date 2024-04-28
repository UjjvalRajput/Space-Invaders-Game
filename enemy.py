import pygame
import random
import os
from bullet import EnemyBullet

# Citation: Some code is reused from LAB 3 of the course. Provided by Dr. Nixon

class Enemy(pygame.sprite.Sprite):
    """ This class represents the Enemy. """

# Constructor has optional parameters such as speed and size of enemy
    def __init__(self, all_sprites_list, bullet_list, speed=1, size=(25, 25)):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Finding the path to the image and assigning image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alien_url = os.path.join(script_dir, "enemy.png")
        # citation: https://www.pngegg.com/en/png-zhjyi/download
        original_image = pygame.image.load(alien_url)
        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect()
        self.shooting_chance = 0.001
        # Set the initial movement direction
        self.direction = 1  # 1 for right, -1 for left
        self.all_sprites_list = all_sprites_list
        self.bullet_list = bullet_list
        self.speed = speed


    def update(self):
        """ Move the enemy and shoot the bullet. """
        # Move the enemy
        self.rect.x += self.direction * self.speed
        # Check if the enemy reaches the screen boundaries, if it does move it down one block and reverse direction
        if self.rect.right >= 640 or self.rect.left <= 0:
            self.rect.y += self.rect.height
            self.direction *= -1
        # The enemy may or may not shoot a bullet
        if random.random() < self.shooting_chance:
            # if it does shoot one, make the bullet and shoot from the enemy's centre (this way it actually looks like the enemy shot it)
            bullet = EnemyBullet()
            bullet.image.fill(pygame.color.THECOLORS['purple'])
            bullet.rect.x = self.rect.x + self.rect.width // 2 - bullet.rect.width // 2
            bullet.rect.y = self.rect.y + self.rect.height
            self.all_sprites_list.add(bullet)
            self.bullet_list.add(bullet)
