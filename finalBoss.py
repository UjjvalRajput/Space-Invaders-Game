import pygame
import random
import os
from bullet import EnemyBullet

class FinalBoss(pygame.sprite.Sprite):
    """ This class represents the final boss enemy. """

    def __init__(self, all_sprites_list, bullet_list, level):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Finding the path to the image and assigning image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alien_url = os.path.join(script_dir, "finalboss.png")
        # citation: https://www.pngegg.com/en/png-yjamf/download
        original_image = pygame.image.load(alien_url)
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.shooting_chance = 0.01
        self.all_sprites_list = all_sprites_list
        self.bullet_list = bullet_list
        self.level = level
        self.health = level * 9  # Health scales with the level (harder to kill as level goes up)
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 2
        self.move_counter = 0
        self.move_interval = random.randint(30, 60)  # Random interval for movement
        self.boundary_margin = 30  # Margin to stay within screen boundary


    def update(self):
        """ Move the final boss, shoot bullets, and check for collisions. """
        self.move_counter += 1
        # Random left-right movement within boundaries
        if self.move_counter >= self.move_interval:
            self.direction *= random.choice([-1, 1])  # Randomly change direction
            self.move_counter = 0
            self.move_interval = random.randint(30, 60)  # Reset movement interval
        self.rect.x += self.direction * self.speed
        # Check if the enemy reaches the screen boundaries, if it does move it down one-fourth block and reverse direction
        if self.rect.right >= 640 or self.rect.left <= 0:
            self.rect.y += self.rect.height // 4
            self.direction *= -1
        # Shoot bullets
        if random.random() < self.shooting_chance:
            bullet = EnemyBullet()
            bullet.image.fill(pygame.color.THECOLORS['red'])
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.y = self.rect.bottom
            self.all_sprites_list.add(bullet)
            self.bullet_list.add(bullet)
