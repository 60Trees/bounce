import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))  # Create a window with the specified dimensions
pygame.display.set_caption("Image Movement and Cropping Example")

# Load the image
image = pygame.image.load('textures/glowstone.png')  # Replace with your image path
image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
image_rect = image.get_rect()  # Get the rectangle area of the image for positioning

# Variables for cropping from each side
crop_left = 0
crop_top = 0
crop_right = 0
crop_bottom = 0

# Variables for image position
image_x = 0
image_y = 0
image_speed = 5  # Speed at which the image moves

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the window is closed
            running = False
        if event.type == pygame.KEYDOWN:  # Check for key presses
            if event.key == pygame.K_DELETE:  # Reset everything if Delete key is pressed
                crop_left = 0
                crop_top = 0
                crop_right = 0
                crop_bottom = 0
                image_x = 0
                image_y = 0

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Control movement with WSAD keys
    if keys[pygame.K_w]:  # Move up
        image_y -= image_speed
    if keys[pygame.K_s]:  # Move down
        image_y += image_speed
    if keys[pygame.K_a]:  # Move left
        image_x -= image_speed
    if keys[pygame.K_d]:  # Move right
        image_x += image_speed

    # Control cropping with arrow keys
    if keys[pygame.K_UP]:  # Crop from the top
        crop_top += 1
    if keys[pygame.K_DOWN]:  # Crop from the bottom
        crop_bottom += 1
    if keys[pygame.K_LEFT]:  # Crop from the left
        crop_left += 1
    if keys[pygame.K_RIGHT]:  # Crop from the right
        crop_right += 1

    # Calculate the new cropped rectangle
    cropped_rect = pygame.Rect(
        crop_left,
        crop_top,
        image_rect.width - crop_left - crop_right,
        image_rect.height - crop_top - crop_bottom
    )

    # Fill the screen with white color
    screen.fill((255, 255, 255))

    # Check if the cropped rectangle is valid
    if cropped_rect.width > 0 and cropped_rect.height > 0:
        # Blit (draw) the cropped image onto the screen at the current position
        screen.blit(image, (image_x, image_y), cropped_rect)

    # Update the display with the new frame
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
