# This file is used to store the classes
# Class List: Player, Enemy, Bullet, Text

import pygame
from pygame import mixer


# Create the player class
class Player:
    # Initialize player with (x,y), change in x position, and image file
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.x_change = 0

    # Draw player on screen using coordinates and image
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    # Update player position in x direction
    def update(self):
        self.x += self.x_change
        # Check if player is going out of bounds
        if self.x < 0:
            self.x = 0
        elif self.x > 1000 - self.image.get_width():
            self.x = 1000 - self.image.get_width()


# Create the enemy class
class Enemy:
    # Initialize enemy with (x,y), change in x, change in y, and image file
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        # Enemies constantly moving
        self.x_change = 1
        self.y_change = 0

    # Draw the enemy on screen using coordinates and image
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    # Update enemy position in x and y directions
    def update(self):
        self.x += self.x_change
        self.y += self.y_change

    # Function to have enemies fire bullets
    def create_bullet(self, x, y):
        self.x = x
        self.y = y
        # Create a bullet object
        bullet = Bullet(self.x + 40, self.y + 40, "assets/pixel_laser_red.png", "enemy")
        bullet.bullet_state = "fired"
        return bullet


# Create the bullet class
class Bullet:
    # Initialize bullet with (x,y), image, and bullet type
    def __init__(self, x, y, image, bullet_type):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.bullet_type = bullet_type
        # Change in coordinates
        self.x_change = 0
        self.y_change = 0
        # Create a bullet sound
        self.bullet_sound = mixer.Sound("assets/laser.wav")
        # Bullet will have two states, "ready" and "fired"
        self.bullet_state = "ready"

    # Draw the bullet on screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    # Update bullet position in x and y directions
    def update(self):
        self.x += self.x_change
        self.y += self.y_change
        # Check if bullet is fired and move up
        if self.bullet_state == "fired":
            if self.bullet_type == "player":
                self.y_change = -10
            elif self.bullet_type == "enemy":
                self.y_change = 10
        # Check if bullet is in ready status
        if self.bullet_state == "ready":
            # Move bullet off-screen based on bullet type
            if self.bullet_type == "player":
                self.y = -100
            # If bullet reaches top (for player) or bottom (for enemy), reset bullet state
        if (self.y == 0 and self.bullet_type == "player") or (self.y >= 1000 and self.bullet_type == "enemy"):
            self.bullet_state = "ready"

    # Update bullet state when fired
    def fire_bullet(self, x, y):
        self.x = x
        self.y = y
        self.bullet_state = "fired"
        self.bullet_sound.play()


# Create the text class
class Text:
    # Initialize text with (x, y), font type, font size, content, and rendered text
    def __init__(self, x, y, font_type, font_size):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font_type, font_size)

    # Render the object with text, anti-aliasing, and color
    def rendered(self, text, a_a, color):
        self.text = text
        self.a_a = a_a
        self.color = color
        self.rendered_text = self.font.render(text, a_a, color)

    # Draw the rendered text on screen
    def draw(self, screen):
        screen.blit(self.rendered_text, (self.x, self.y))