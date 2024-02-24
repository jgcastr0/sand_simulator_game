import pygame
import numpy as np
from random import choice
from time import time


# Initializing Pygame
pygame.init()

# Instructions timer
start_time = time()
elapsed_time = 0

# Screen settings
particle_size = 10  # Change this value to play with the particles size
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))

# Colors
BACKGROUND_COLOR = tuple((0, 0, 0))
SAND_COLOR = tuple((197, 175, 128))
TEXT_COLOR = tuple((255, 255, 255))

# Clock object to control FPS rate
clock = pygame.time.Clock()

class TheGrid:

    def __init__(self):
        self.grid = np.zeros((int(width / particle_size), int(height / particle_size)))    # Creates the grid based on the particle size
        self.sand_positions = [] # particles positions


    def sand(self, mouseX, mouseY):
        gridX, gridY = int(mouseX / particle_size), int(mouseY / particle_size)

        if gridX >= 0 and gridX < self.grid.shape[0] and gridY >= 0 and gridY < self.grid.shape[1]:
            if self.grid[gridX][gridY] == 0:
                self.grid[gridX][gridY] = 1
                self.sand_positions.append([gridX * particle_size, gridY * particle_size])


    def create(self, screen):
        for particles in self.sand_positions:
            pygame.draw.rect(screen, SAND_COLOR, (particles[0], particles[1], particle_size, particle_size), 0)     


    def update_particles_positions(self):
        for particles in self.sand_positions:
            x, y = particles
            gridX, gridY = int(x / particle_size), int(y / particle_size)
            
            # Checks if it can move downwards
            if gridY < self.grid.shape[1] - 1 and self.grid[gridX][gridY + 1] == 0:
                self.grid[gridX][gridY] = 0
                self.grid[gridX][gridY + 1] = 1
                self.sand_positions.remove([x, y])
                self.sand_positions.append([x, y + particle_size])

            # Checks if both lower diagonals are free and chooses one to slide down
            elif gridY < self.grid.shape[1] - 1 and gridX > 0 and gridX < self.grid.shape[0] - 1 and self.grid[gridX + 1][gridY + 1] == 0 and self.grid[gridX - 1][gridY + 1] == 0:
                direction = choice([1, -1])
                self.grid[gridX][gridY] = 0
                self.grid[gridX + direction][gridY + 1] = 1
                self.sand_positions.remove([x, y])
                self.sand_positions.append([x + (particle_size * direction), y + particle_size])

            # Checks if the lower right diagonal is free and slides down to it    
            elif gridY < self.grid.shape[1] - 1 and gridX > 0 and gridX < self.grid.shape[0] - 1 and self.grid[gridX + 1][gridY + 1] == 0:
                self.grid[gridX][gridY] = 0
                self.grid[gridX + 1][gridY + 1] = 1
                self.sand_positions.remove([x, y])
                self.sand_positions.append([x + particle_size, y + particle_size])
            
            # Checks if the lower left diagonal is free and slides down to it    
            elif gridY < self.grid.shape[1] - 1 and gridX > 0 and gridX < self.grid.shape[0] - 1 and self.grid[gridX -1][gridY + 1] == 0:
                self.grid[gridX][gridY] = 0
                self.grid[gridX - 1][gridY + 1] = 1
                self.sand_positions.remove([x, y])
                self.sand_positions.append([x - particle_size, y + particle_size])


    def display_text(text):
        font = pygame.font.Font(None, 27)
        text1 = font.render(text, True, TEXT_COLOR)
        text_rect = text1.get_rect(center = (width // 2, 50))
        screen.blit(text1, text_rect)



def main(start_time, elapsed_time):

    # Main loop
    while True:

        xm, ym = pygame.mouse.get_pos()

        # Shows some informations
        pygame.display.set_caption(f"sand Simulator  |  FPS: {int(clock.get_fps())}  |  Number of Particles: {len(universe.sand_positions)}  |  Mouse posX: [{xm}]  Mouse posY: [{ym}]")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            mouse_buttons = pygame.mouse.get_pressed()
            
            if mouse_buttons[0]:
                pos = pygame.mouse.get_pos()
                universe.sand(pos[0] - pos[0] % particle_size, pos[1] - pos[1] % particle_size)
                

        # Fill the screen with a color
        screen.fill(BACKGROUND_COLOR)

        # Shows instructions
        if elapsed_time < 5:
            TheGrid.display_text("Press the left mouse button to add particles")
            elapsed_time = time() - start_time

        # Updates Particle Positions
        universe.update_particles_positions()

        # Draws the particles
        universe.create(screen)

        # Updates the display
        pygame.display.flip()
        
        # FPS rate
        clock.tick(120) 


if __name__ == '__main__':
    universe = TheGrid()
    while True:
        main(start_time, elapsed_time)
