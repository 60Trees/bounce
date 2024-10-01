import pygame
import sys

def rgb_to_hue(r, g, b):
    """ Convert RGB to Hue value. """
    r /= 255.0
    g /= 255.0
    b /= 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)

    if mx == mn:
        return 0  # Achromatic (no hue)

    d = mx - mn
    if mx == r:
        h = (60 * ((g - b) / d) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / d) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / d) + 240) % 360

    return h

def hsv_to_rgb(hsv):
    """ Convert HSV back to RGB color space. """
    h, s, v = hsv
    if s == 0:
        r = g = b = int(v * 255)
    else:
        i = int(h // 60) % 6
        f = (h / 60) - i
        p = int(v * (1 - s) * 255)
        q = int(v * (1 - f * s) * 255)
        t = int(v * (1 - (1 - f) * s) * 255)
        v = int(v * 255)

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q

    return (r, g, b)

def adjustTint(surface, RGB):
    """ Adjust the tint of the surface based on the provided RGB value. """
    # Extract hue from the RGB input
    hue = rgb_to_hue(*RGB)

    # Create a new surface for the adjusted pixels
    finished_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            # Convert brightness to a scale from 0 to 1
            brightness = (r + g + b) / (3 * 255)  # Average of RGB
            # Adjust based on the pixel's alpha (transparency)
            opacity = a / 255.0
            
            # Calculate the new color using HSV
            new_color = hsv_to_rgb((hue, 1, brightness * opacity))
            
            # Set the new color with adjusted opacity
            finished_surface.set_at((x, y), (*new_color, int(a)))

    return finished_surface

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Tint Adjustment')

    # Load the image
    image = pygame.image.load("textures/note.png").convert_alpha()
    image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
    image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
    image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Example RGB value for tinting
        RGB = (16, 250, 124)
        tinted_surface = adjustTint(image, RGB)

        screen.fill((255, 255, 255))  # Clear the screen
        screen.blit(tinted_surface, (0, 0))  # Draw the tinted surface
        pygame.display.flip()

if __name__ == '__main__':
    main()
