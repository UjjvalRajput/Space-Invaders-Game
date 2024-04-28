import pygame
import random
import os
from block import Block
from bullet import Bullet
from player import Player
from enemy import Enemy
from finalBoss import FinalBoss

# Citation: Some code is reused from LAB 3 of the course. Provided by Dr. Nixon

class Game:
    """ This class represents the Game. It contains all the game objects. """

    def __init__(self):
        """ Set up the game on creation. """

        # Initialize Pygame
        pygame.init()
        # --- Create the window
        # Set the height and width of the screen
        self.level = 1
        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode(
            [self.screen_width, self.screen_height])
        self.num_blocks = (9 * self.level) + 9
        self.req_to_win = self.num_blocks
        self.num_enemies = 9 + self.level
        self.font = pygame.font.Font(os.path.join("ARCADE_N.TTF"), 18)
        # font citation: https://www.dafont.com/arcade-ya.font
        self.running = False
        # --- Sprite lists
        # This is a list of every sprite. All blocks, the player block, and enemies.
        self.all_sprites_list = pygame.sprite.Group()
        # List of each block in the game
        self.block_list = pygame.sprite.Group()
        # List of each bullet
        self.bullet_list = pygame.sprite.Group()
        # List of each enemy
        self.enemy_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        # --- Create the sprites
        self.create_blocks()
        self.player = Player()
        self.all_sprites_list.add(self.player)
        self.all_sprites_list.add(self.enemy_bullet_list)
        self.create_enemies()
        self.score = 0
        self.player.rect.y = self.screen_height - self.player.rect.height * 2
        # Load and scale the background image
        self.background_image = pygame.image.load("background.png")
        # citation: https://pngtree.com/freepng/star-space-transparency-background_5439546.html
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        # Make the background image slightly transparent
        self.background_image.set_alpha(190)
        # Initially there is no final boss, it will be added in level 3
        self.final_boss = None

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                bullet = Bullet()
                # Set the bullet so it is where the player is
                bullet.rect.center = self.player.rect.center
                # Add the bullet to the lists
                self.all_sprites_list.add(bullet)
                self.bullet_list.add(bullet)


    def update(self):
        # Call the update() method on all the sprites
        self.all_sprites_list.update()
        # Calculate mechanics for each enemy bullet
        for enemy_bullet in self.enemy_bullet_list:
            # Check if it hits the player
            if pygame.sprite.collide_rect(enemy_bullet, self.player):
                self.running = False
                print("Game Over! You Lose. Enemy Bullet Hit You!")
            # Remove the bullet if it flies down off the screen
            if enemy_bullet.rect.y > self.screen_height:
                self.enemy_bullet_list.remove(enemy_bullet)
                self.all_sprites_list.remove(enemy_bullet)
        # Calculate mechanics for each bullet
        for bullet in self.bullet_list:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(
                bullet, self.block_list, True)
            # For each block hit, remove the bullet and add to the score
            for _ in block_hit_list:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
                self.score += 1
                if self.score >= self.req_to_win:
                    print("Congratulations! You won!")
                    self.reset_level()
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < (0 - bullet.rect.height):
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
        # Check if an enemy hits the disappear_threshold
        disappear_threshold = self.screen_height - self.player.rect.height * 3
        for enemy in self.enemy_list:
            if enemy.rect.bottom >= disappear_threshold:
                self.score -= 1
                self.req_to_win -= 1
                self.enemy_list.remove(enemy)
                self.all_sprites_list.remove(enemy)
                if self.score < 0:
                    print("Game Over! You lose.")
                    self.running = False
        if self.req_to_win == 0:
            print("Congratulations! You won!")
            self.reset_level()
        # Update the final boss, if it exists
        if self.final_boss:
            # Check for collision with player bullets
            final_boss_bullet_collisions = pygame.sprite.spritecollide(self.final_boss, self.bullet_list, True)
            for _ in final_boss_bullet_collisions:
                self.final_boss.health -= 1
                if self.final_boss.health <= 0:
                    print("Final Boss defeated!")
                    self.final_boss.kill()  # Remove the final boss from the game
                    self.score += 5  # Increment the score for defeating the final boss
                    self.final_boss = None  # Reset the final boss variable to allow for another final boss to be created in subsequent level


    def create_blocks(self):
        for i in range(self.num_blocks):
            # This represents a block
            block = Block()
            # Set a random location for the block
            block.rect.x = random.randrange(self.screen_width - 20)
            block.rect.y = random.randrange(
                self.screen_height // 2)  # don't go all the way down
            # Add the block to the list of objects
            self.block_list.add(block)
            self.all_sprites_list.add(block)

    def create_enemies(self):
        # Create enemies
        if self.level != 1:
            for i in range(self.num_enemies - (self.level - 1)):
                enemy = Enemy(self.all_sprites_list, self.enemy_bullet_list)
                enemy.rect.x = random.randrange(self.screen_width - 20)
                enemy.rect.y = random.randrange(0, self.screen_height // 2)
                if enemy.rect.left <= 0:
                    enemy.rect.left = 1
                elif enemy.rect.right >= 640:
                    enemy.rect.right = 639
                self.enemy_list.add(enemy)
                self.all_sprites_list.add(enemy)
            # Create faster, bigger, scarier, more likely to shoot enemies if it is not the first level (as first level is easy)
            for i in range(self.level - 1):
                enemy = Enemy(self.all_sprites_list, self.enemy_bullet_list, speed=2, size=(40, 40))
                enemy.rect.x = random.randrange(self.screen_width - 20)
                enemy.rect.y = random.randrange(0, 20)
                new_image = enemy.image.copy()
                enemy.shooting_chance = 0.01 # higher shooting chance
                red_value = random.randint(200, 255)  # Generate a random red value between 200 and 255
                green_value = random.randint(0, 100)   # Generate a random green value between 0 and 100
                new_image.fill((red_value, green_value, 0), None, pygame.BLEND_RGBA_MULT)  # Use the generated values
                enemy.image = new_image
                if enemy.rect.left <= 0:
                    enemy.rect.left = 1
                elif enemy.rect.right >= 640:
                    enemy.rect.right = 639
                self.enemy_list.add(enemy)
                self.all_sprites_list.add(enemy)
        else:
            for i in range(self.num_enemies):
                enemy = Enemy(self.all_sprites_list, self.enemy_bullet_list)
                enemy.rect.x = random.randrange(self.screen_width - 20)
                enemy.rect.y = random.randrange(0, self.screen_height // 2)
                if enemy.rect.left <= 0:
                    enemy.rect.left = 1
                elif enemy.rect.right >= 640:
                    enemy.rect.right = 639
                self.enemy_list.add(enemy)
                self.all_sprites_list.add(enemy)
        if self.level > 2:
            self.final_boss = FinalBoss(self.all_sprites_list, self.enemy_bullet_list, level=self.level)
            self.all_sprites_list.add(self.final_boss)
            self.enemy_list.add(self.final_boss)

    def reset_level(self):
        """ Reset parameters for the next level """
        self.level += 1
        self.num_blocks = 9 * self.level
        self.req_to_win = self.num_blocks
        self.num_enemies = 9 + self.level
        # Remove all existing sprites except for the player
        for sprite in self.all_sprites_list.sprites():
            if sprite != self.player:
                self.all_sprites_list.remove(sprite)
        # Create new blocks and enemies
        self.create_blocks()
        self.create_enemies()
        # Reset score
        self.score = 0
        # Reset player position
        self.player.rect.y = self.screen_height - self.player.rect.height * 2


    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.color.THECOLORS['black'])
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))
        # Draw all the spites
        self.all_sprites_list.draw(self.screen)
        # Render the score text
        score_text = self.font.render("Score: {}".format(self.score), True, pygame.color.THECOLORS['white'])
        score_rect = score_text.get_rect()
        score_rect.bottomleft = (1, self.screen_height)
        self.screen.blit(score_text, score_rect)
        # Render the level text
        level_text = self.font.render("Level: {}".format(self.level), True, pygame.color.THECOLORS['white'])
        level_rect = level_text.get_rect()
        level_rect.bottomright = (self.screen_width - 1, self.screen_height)
        self.screen.blit(level_text, level_rect)


    def show_help(self):
        help_screen = True
        help_font = pygame.font.Font(None, 18)
        help_text = [
            "Moves: left & right",
            "Shoot bullet: mouse Click (mouse recommended)",
            "Object: asteroids and final boss (teal-orange-yellow) can be shot",
            "Levels: Unlimited (please allow time to spawn the new level)",
            "How to win:",
            "Shoot down all asteroids, do not get hit by enemy bullet, kill final boss to gain extra score and win early",
            "How to lose (because why not):",
            "Get shot by enemy bullet, let the aliens come down and reduce your score below 0",
            "Post/During gameplay, view console for more information",
            "Press 'Escape' to return to menu"
        ]

        while help_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        help_screen = False  # Close the help screen if 'Escape' is pressed

            # Draw the help screen
            self.screen.fill(pygame.color.THECOLORS['black'])
            for i, line in enumerate(help_text):
                text_render = help_font.render(line, True, pygame.color.THECOLORS['white'])
                text_rect = text_render.get_rect(center=(self.screen_width // 2, 100 + i * 40))
                self.screen.blit(text_render, text_rect)
            pygame.display.flip()


    def run(self):
        background_image = pygame.image.load("background.png")  # Set the background image
        background_image = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
        welcome_screen = True
        play_button_rect = pygame.Rect(250, 200, 140, 50)  # Define the play button rectangle
        help_button_rect = pygame.Rect(250, 300, 140, 50)  # Define the help button rectangle
        while welcome_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        welcome_screen = False  # Start the game if the play button is clicked
                    elif help_button_rect.collidepoint(event.pos):
                        self.show_help()  # Show the help screen if the help button is clicked
            # Draw the welcome screen
            self.screen.fill(pygame.color.THECOLORS['black'])
            self.screen.blit(background_image, (0, 0))
            welcome_text = self.font.render("Welcome to Space Invaders!", True, pygame.color.THECOLORS['white'])
            welcome_rect = welcome_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
            self.screen.blit(welcome_text, welcome_rect)
            # Draw the play button
            pygame.draw.rect(self.screen, pygame.color.THECOLORS['green'], play_button_rect)
            play_text = self.font.render("Play", True, pygame.color.THECOLORS['white'])
            play_rect = play_text.get_rect(center=play_button_rect.center)
            self.screen.blit(play_text, play_rect)
            # Draw the help button
            pygame.draw.rect(self.screen, pygame.color.THECOLORS['blue'], help_button_rect)
            help_text = self.font.render("Help", True, pygame.color.THECOLORS['white'])
            help_rect = help_text.get_rect(center=help_button_rect.center)
            self.screen.blit(help_text, help_rect)
            pygame.display.flip()
        # Start the game loop
        self.running = True
        clock = pygame.time.Clock()
        self.running = True
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        # -------- Main Program Loop -----------
        while self.running:
            # --- Event processing
            self.poll()
            # --- Handle game logic
            self.update()
            # --- Draw a frame
            self.draw()
            # Update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit the frames per second
            clock.tick(60)


if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shutting down in 3 seconds...")
    pygame.time.delay(3000)
    pygame.quit()
