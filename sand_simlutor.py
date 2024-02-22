import pygame
import sys
import numpy as np

# Initializing Pygame
pygame.init()

# Window settings
particle_size = 10
width, height = 600, 600
screen = pygame.display.set_mode((width, height))

# Colors
background_color = (0, 0, 0)
sand = (197, 175, 128)

# Clock object to control FPS rate
clock = pygame.time.Clock()

class TheGrid:
    def __init__(self):
        self.grid = np.zeros([width / particle_size, height / particle_size]) # Creates the grid based on the particle size


class Sand:
    def __init__(self):
        self.sand_positions = np.array([])



# Main loop
while True:

    pygame.display.set_caption(f"Sand Simulator | FPS: {int(clock.get_fps())}") # Shows fps rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with a color
    screen.fill(background_color)


    

    # Update the display
    pygame.display.flip()

    clock.tick(120) # FPS rate
