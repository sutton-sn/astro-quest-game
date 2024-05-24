import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Define colors
BACKGROUND_COLOR = (33, 31, 41)  # Background color (#211F29)
WHITE = (255, 255, 255)

# Define window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Astro Quest")

# Load the spaceship image
spaceship_image = pygame.image.load("ship.png").convert_alpha()

# Resize the spaceship image to a much smaller size
scale_factor = 0.1  # Scale to 10% of the original size
spaceship_image = pygame.transform.smoothscale(spaceship_image, (int(spaceship_image.get_width() * scale_factor), int(spaceship_image.get_height() * scale_factor)))

# Get the dimensions of the resized spaceship image
spaceship_width, spaceship_height = spaceship_image.get_size()

# Initial position of the spaceship in the game world
world_width = 1600
world_height = 1200
spaceship_x = world_width // 2
spaceship_y = world_height // 2

# Spaceship movement speed
spaceship_speed = 5

# Initial rotation angle of the spaceship
spaceship_angle = 0

# List to store bullets
bullets = []

# Bullet size and speed
bullet_size = 5
bullet_speed = 10

# Load asteroid images and resize them to be smaller
small_asteroid_image = pygame.image.load("small-asteroid.png").convert_alpha()
medium_asteroid_image = pygame.image.load("medium-asteroid.png").convert_alpha()
big_asteroid_image = pygame.image.load("big-asteroid.png").convert_alpha()

# Resize the asteroids to be smaller
small_asteroid_image = pygame.transform.smoothscale(small_asteroid_image, (20, 20))
medium_asteroid_image = pygame.transform.smoothscale(medium_asteroid_image, (40, 40))
big_asteroid_image = pygame.transform.smoothscale(big_asteroid_image, (60, 60))

# List to store asteroids
asteroids = []

# Function to generate asteroids at random positions
def generate_asteroid():
    size = random.choice(['small', 'medium', 'big'])
    if size == 'small':
        asteroid_image = small_asteroid_image
    elif size == 'medium':
        asteroid_image = medium_asteroid_image
    else:
        asteroid_image = big_asteroid_image
    asteroid_rect = asteroid_image.get_rect(center=(random.randint(0, world_width), random.randint(0, world_height)))
    asteroids.append((asteroid_image, asteroid_rect))

# Generate initial asteroids
for _ in range(10):
    generate_asteroid()

# Function to handle collisions
def check_collisions():
    global asteroids, bullets, spaceship_x, spaceship_y
    new_asteroids = []
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if bullet[0].colliderect(asteroid[1]):
                if asteroid[1].width > small_asteroid_image.get_width():
                    if asteroid[1].width == big_asteroid_image.get_width():
                        new_size = medium_asteroid_image
                    else:
                        new_size = small_asteroid_image
                    for _ in range(2):
                        new_rect = new_size.get_rect(center=asteroid[1].center)
                        new_asteroids.append((new_size, new_rect))
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                break
    asteroids.extend(new_asteroids)

    # Ship collisions with asteroids
    spaceship_rect = pygame.Rect(spaceship_x - spaceship_width // 2, spaceship_y - spaceship_height // 2, spaceship_width, spaceship_height)
    for asteroid in asteroids:
        if spaceship_rect.colliderect(asteroid[1]):
            # Revert the ship's movement
            spaceship_x -= move_x
            spaceship_y -= move_y
            break

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new bullet
                bullet_angle = math.radians(spaceship_angle + 90)
                bullet_x = spaceship_x + math.cos(bullet_angle) * (spaceship_width // 2)
                bullet_y = spaceship_y - math.sin(bullet_angle) * (spaceship_height // 2)
                bullet_dx = math.cos(bullet_angle) * bullet_speed
                bullet_dy = -math.sin(bullet_angle) * bullet_speed
                bullets.append((pygame.Rect(bullet_x, bullet_y, bullet_size, bullet_size), bullet_dx, bullet_dy))

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Determine movement direction
    move_x = 0
    move_y = 0
    if keys[pygame.K_LEFT]:
        move_x -= spaceship_speed
    if keys[pygame.K_RIGHT]:
        move_x += spaceship_speed
    if keys[pygame.K_UP]:
        move_y -= spaceship_speed
    if keys[pygame.K_DOWN]:
        move_y += spaceship_speed

    # Update spaceship position
    spaceship_x += move_x
    spaceship_y += move_y

    # Update spaceship rotation angle
    if move_x != 0 or move_y != 0:
        spaceship_angle = (math.degrees(math.atan2(-move_y, move_x)) - 90) % 360

    # Rotate the spaceship image
    rotated_spaceship_image = pygame.transform.rotate(spaceship_image, spaceship_angle)
    rotated_spaceship_rect = rotated_spaceship_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Move bullets
    for bullet in bullets[:]:
        bullet[0].x += bullet[1]
        bullet[0].y += bullet[2]
        if bullet[0].x < 0 or bullet[0].x > world_width or bullet[0].y < 0 or bullet[0].y > world_height:
            bullets.remove(bullet)

    # Generate new asteroids randomly
    if random.randint(1, 60) == 1:  # Approximately one per second at 60 FPS
        generate_asteroid()

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Calculate camera offset
    camera_x = spaceship_x - SCREEN_WIDTH // 2
    camera_y = spaceship_y - SCREEN_HEIGHT // 2

    # Draw asteroids
    for asteroid_image, asteroid_rect in asteroids:
        screen.blit(asteroid_image, (asteroid_rect.x - camera_x, asteroid_rect.y - camera_y))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0].x - camera_x, bullet[0].y - camera_y, bullet[0].width, bullet[0].height))

    # Draw the spaceship in the center of the screen
    screen.blit(rotated_spaceship_image, rotated_spaceship_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

    # Check collisions
    check_collisions()

# Quit the game
pygame.quit()
sys.exit()