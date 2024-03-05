import pygame
import numpy as np
from time import time
from random import choice


# Initializing Pygame
pygame.init()


# Screen settings
width, height = 1100, 600
screen = pygame.display.set_mode((width, height))

# Clock object to control FPS rate
clock = pygame.time.Clock()
fps = 120

class TheGrid:

    def __init__(self):

        # Particles settings
        self.particle_size = 3  # Change this value to play with the particles size

        # Creates the grid based on the particle size
        self.grid = np.zeros((int((width / self.particle_size) + 2), int(height / self.particle_size)))
        
        # Colors
        self.BACKGROUND_COLOR:tuple = (0, 0, 0)
        self.SAND_COLOR:tuple = (197, 175, 128)


    def sand(self, x, y): # Adds sand particles

        gridX, gridY = x // self.particle_size, y // self.particle_size
        self.grid[gridX][gridY] = 1
        self.grid[gridX + 1][gridY] = 1
        self.grid[gridX - 1][gridY] = 1
           

    def create(self, screen):    # Draws the particles]

        # Makes a 3d array with the particles colors
        color_array = np.zeros((self.grid.shape[0], self.grid.shape[1], 3))
        
        # Define the colors for each type of particle
        color_array[self.grid == 1] = self.SAND_COLOR
        #color_array[self.grid == 2] = self.WATER_COLOR
        #color_array[self.grid == 2] = self.WALL_COLOR

        # Cria uma superfície a partir do array de cores
        surface = pygame.surfarray.make_surface(color_array)

        # Redimensiona a superfície para o tamanho da tela
        surface = pygame.transform.scale(surface, (width, height))

        # Desenha a superfície na tela
        screen.blit(surface, (0, 0))


    def update_sand_positions(self, array): # Updates the position of sand particles      
        
        # Checks if it can move downwards
        down = (array[:, :-1] == 1) & (array[:, 1:] == 0)
        
        array[:, :-1][down] = 0
        array[:, 1:][down] = 1

        # Checks if the lower right diagonal is free and slides down to it
        """right_diagonal = (array[:-1, :-1] == 1) & (array[1:, 1:] == 0)
        
        array[:-1, :-1][right_diagonal] = 0
        array[1:, 1:][right_diagonal] = 1"""

        # Checks if the lower left diagonal is free and slides down to it
        left_diagonal = (array[1:, 1:] == 1) & (array[1:, :-1] == 0)
        
        array[:-1, 1:][left_diagonal] = 0
        array[1:, :-1][left_diagonal] = 1


        
def main():

    # Main loop
    while True:

        start2 = time()

        # Shows some informations
        pygame.display.set_caption(f"Sand Simulator |  FPS: {int(clock.get_fps())}  |   Particulas: {np.count_nonzero(universe.grid == 1)}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #mouse_buttons = pygame.mouse.get_pressed()
            key = pygame.key.get_pressed()

            if key[pygame.K_1]:
                pos = pygame.mouse.get_pos()
                universe.sand(pos[0] - pos[0] % universe.particle_size, pos[1] - pos[1] % universe.particle_size)
               

        # Fill the screen with a color
        screen.fill(universe.BACKGROUND_COLOR)

        # Draws the particles
        universe.create(screen)
        
        # Updates Particle Positions
        universe.update_sand_positions(universe.grid)

        # Updates the display
        pygame.display.flip()
        
        # FPS rate
        clock.tick(fps)

        end2 = time()
        print(end2 - start2)


if __name__ == '__main__':
    universe = TheGrid()
    main()