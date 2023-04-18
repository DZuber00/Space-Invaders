# "SpaceInvaders" remake by Daniel Zuber
# This was done to show how modern programming techniques would apply to an arcade game from 1978
# Python 3.11

import random
import pygame
from pygame import mixer
from class_list import Player, Enemy, Bullet, Text

# Initialize the game
pygame.init()

# Create clock object to handle refresh rates
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((1000, 1000))

# Create the background image
background = pygame.image.load("assets/background.png")

# Set the window caption
pygame.display.set_caption("Space Invaders by Daniel Zuber")
# Create and set the window icon
icon = pygame.image.load("assets/invader.png")
pygame.display.set_icon(icon)

# Create player object
player = Player(450, 900, "assets/player.png")

# Create list to store enemies
enemies = []


# Function to create and organize enemies
def setup_enemies():
    # Define enemy numbers
    number_enemies = 55
    enemies_per_row = 11
    enemy_spacing = 75
    # Create 3 rows of 11 enemy objects, spaced apart
    for i in range(number_enemies):
        row = i // enemies_per_row
        column = i % enemies_per_row
        # Change enemy x and y based on column and row
        enemy_x = 100 + (column * enemy_spacing)
        enemy_y = 30 + (row * 60)
        # Creates an enemy object
        enemy = Enemy(enemy_x, enemy_y, "assets/enemy.png")
        # Stores enemy object in enemies list
        enemies.append(enemy)
    return enemies


# Create the bullet object
player_bullet = Bullet(0, -100, "assets/pixel_laser_blue.png", "player")
enemy_bullets = []

# Create the score text object
score_value = 0
score = Text(10, 10, "assets/PressStart2P-Regular.ttf", 24)
score.rendered("Score: " + str(score_value), True, (255, 255, 255))

# Create game over text object
game_over = Text(250, 450, "assets/PressStart2P-Regular.ttf", 64)
game_over.rendered("GAME OVER", True, (255, 255, 255))

# Create title text
title = Text(50, 350, "assets/PressStart2P-Regular.ttf", 64)
title.rendered("Space Invaders", True, (255, 255, 255))

# Create continue text
continue_text = Text(100, 900, "assets/PressStart2P-Regular.ttf", 32)
continue_text.rendered("Press Enter to continue...", True, (255, 255, 255))


# Function to check for collision between rectangles
def is_collision(object_1, object_2):
    # Create rectangles using images
    rect_1 = pygame.Rect(object_1.x, object_1.y, object_1.image.get_width(), object_1.image.get_height())
    rect_2 = pygame.Rect(object_2.x, object_2.y, object_2.image.get_width(), object_2.image.get_height())

    # Return True if rectangles overlap, else return false
    return rect_1.colliderect(rect_2)


# Explosion sound for when collision happens
explosion_sound = mixer.Sound("assets/explosion.wav")

# Set title flag variables
title_screen = True
running = False
game_over_state = False

# Title screen loop
while title_screen:

    # Draw background image on screen
    screen.blit(background, (0, 0))

    # Draw title text
    title.draw(screen)
    continue_text.draw(screen)

    # Event handler
    for event in pygame.event.get():
        # If application is exited, stop running
        if event.type == pygame.QUIT:
            title_screen = False
        # Create key-binds using keydown events
        if event.type == pygame.KEYDOWN:
            # If the Enter/Return key is pressed
            if event.key == pygame.K_RETURN:
                # Start the game
                running = True
                # Stop the title screen
                title_screen = False

    # Update frames
    pygame.display.flip()
    clock.tick(60)


# Main game loop

# While the game is running
while running:

    # Event handler
    for event in pygame.event.get():
        # If application is exited, stop running
        if event.type == pygame.QUIT:
            running = False
        # Create key-binds using keydown events
        if event.type == pygame.KEYDOWN:
            # Move left keybind
            if event.key == pygame.K_LEFT:
                player.x_change = -5
            # Move right keybind
            if event.key == pygame.K_RIGHT:
                player.x_change = 5
            # Fire bullet keybind
            if event.key == pygame.K_SPACE:
                # Check if bullet is in ready state
                if player_bullet.bullet_state == "ready":
                    # If bullet is fired, change bullet position
                    player_bullet.fire_bullet(player.x + 40, player.y - 40)

        # Handle keyup events
        if event.type == pygame.KEYUP:
            # Stop movement if key is up
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

    # Setup enemies
    if len(enemies) == 0:
        enemies = setup_enemies()

    # Collision detection
    for i, enemy in enumerate(enemies):
        if is_collision(enemy, player_bullet):
            # Remove the enemy from the list
            enemies.pop(i)
            # Play explosion sound
            explosion_sound.play()
            # Reset the bullet state
            player_bullet.bullet_state = "ready"
            # Increase the score
            score_value += 100
            score.rendered("Score: " + str(score_value), True, (255, 255, 255))
        # Check if enemy collides with player
        if is_collision(enemy, player):
            # Play explosion sound
            explosion_sound.play()
            # Start game over screen
            game_over_state = True
            running = False

    # Draw background image on screen
    screen.blit(background, (0, 0))

    # Draw the player if not game over
    player.draw(screen)
    player.update()

    # Draw the enemies if not game over
    for enemy in enemies:
        enemy.draw(screen)
        enemy.update()

    # Add enemy movement using a flag variable
    change_direction = False
    # Check each enemy x if it hits border
    for enemy in enemies:
        if enemy.x >= 1000 - enemy.image.get_width() or enemy.x <= 0:
            # If enemy hits border, change flag
            change_direction = True
            break

    # If flag is true then change enemy position and direction
    if change_direction:
        for enemy in enemies:
            enemy.x_change *= -1
            enemy.y += enemy.image.get_height() // 2
        change_direction = False

    # Draw the bullet if not game over
    player_bullet.draw(screen)
    player_bullet.update()

    # Draw the score
    score.draw(screen)

    # Periodically fire bullets from random enemies
    fire_enemy_bullet = random.random() < 0.02
    if fire_enemy_bullet:
        # Chooses random enemy from object list
        random_enemy = random.choice(enemies)
        # Call fire_bullet method from enemy class to create and return a bullet
        enemy_bullet = random_enemy.create_bullet(random_enemy.x, random_enemy.y)
        # Adds enemy bullet to enemy bullet list
        enemy_bullets.append(enemy_bullet)
    # Draw a bullet on screen for each bullet in list, update (x, y)
    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw(screen)
        enemy_bullet.update()

    # Check each enemy for collision with player
    for i, enemy_bullet in enumerate(enemy_bullets):
        if is_collision(enemy_bullet, player):
            # Play explosion sound
            explosion_sound.play()
            # Remove the bullet from the list
            enemy_bullets.pop(i)
            # Start game over screen
            game_over_state = True
            # Stop game from running
            running = False

        # Check if enemy bullet reaches the bottom
        elif enemy_bullet.y >= 1000:
            # Remove the bullet from the list
            enemy_bullets.pop(i)

    # Update frames
    pygame.display.flip()
    clock.tick(60)

# Game over loop
while game_over_state:

    # Event handler
    for event in pygame.event.get():
        # If application is exited, stop running
        if event.type == pygame.QUIT:
            game_over_state = False
        # Create key-binds using keydown events
        #if event.type == pygame.KEYDOWN:

    # Draw background image on screen
    screen.blit(background, (0, 0))

    # Draw the game over
    game_over.draw(screen)

    # Update score position
    score.x = 400
    score.y = 550
    score.draw(screen)

    # Update frames
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
