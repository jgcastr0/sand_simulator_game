import pygame
import numpy as np
from random import choice
from functools import cache


# Initializing Pygame
pygame.init()

# Particles settings
particle_size = 3  # Change this value to play with the particles size
particle_number = 10 # Number of particles added by each iteration

# Screen settings
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))

# Clock object to control FPS rate
clock = pygame.time.Clock()


class TheGrid:

    def __init__(self):
        self.grid = np.zeros((int(width / particle_size), int(height / particle_size)))    # Creates the grid based on the particle size

        # Colors
        self.BACKGROUND_COLOR:tuple = (0, 0, 0)
        self.SAND_COLOR:tuple = (197, 175, 128)


    def sand(self, x, y): # Adds sand particles
        gridX, gridY = int(x / particle_size), int(y / particle_size)
        
        if self.grid[gridX][gridY] == 0:
            self.grid[gridX][gridY] = 1
           

    def create(self, screen):    # Draws the particles
        
        self.sand_postions = np.where(self.grid == 1)
        for x, y in zip(self.sand_postions[0], self.sand_postions[1]):
            pygame.draw.rect(screen, self.SAND_COLOR, (x * particle_size, y * particle_size, particle_size, particle_size))
        

    def update_sand_positions(self): # Updates the position of sand particles      
        
        for gridX, gridY in zip(self.sand_postions[0], self.sand_postions[1]):

            # Checks the screen limits
            if gridX >= 0 and gridX < self.grid.shape[0] and gridY >= 0 and gridY < self.grid.shape[1] - 1:
                
                # Checks if it can move downwards
                if self.grid[gridX][gridY + 1] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX][gridY + 1] = 1
                    
                    
                # Checks if both lower diagonals are free and chooses one to slide down
                elif gridX < self.grid.shape[0] - 1 and self.grid[gridX + 1][gridY + 1] == 0 and self.grid[gridX - 1][gridY + 1] == 0:
                    direction = choice([1, -1])
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX + direction][gridY + 1] = 1
                    

                # Checks if the lower right diagonal is free and slides down to it    
                elif gridX < self.grid.shape[0] - 1 and self.grid[gridX + 1][gridY + 1] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX + 1][gridY + 1] = 1
                    

                # Checks if the lower left diagonal is free and slides down to it    
                elif self.grid[gridX - 1][gridY + 1] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX - 1][gridY + 1] = 1


def main():

    # Main loop
    while True:

        # Shows some informations
        pygame.display.set_caption(f"Sand Simulator  |  FPS: {int(clock.get_fps())}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #mouse_buttons = pygame.mouse.get_pressed()
            key = pygame.key.get_pressed()

            if key[pygame.K_1]:
                pos = pygame.mouse.get_pos()
                universe.sand(pos[0] - pos[0] % particle_size, pos[1] - pos[1] % particle_size)
               

        # Fill the screen with a color
        screen.fill(universe.BACKGROUND_COLOR)

        # Draws the particles
        universe.create(screen)
        
        # Updates Particle Positions
        universe.update_sand_positions()

        # Updates the display
        pygame.display.flip()
        
        # FPS rate
        clock.tick(120) 


if __name__ == '__main__':
    universe = TheGrid()
    while True:
        main()