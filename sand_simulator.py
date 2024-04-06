import pygame
import numpy as np
from random import choice
from time import time

# Initializing Pygame
pygame.init()

# Instructions timer
start_time = time()
elapsed_time = 0

# Particles settings
particle_size = 5  # Change this value to play with the particles size
particle_number = 15 # Number of particles added by each iteration

# Screen settings
width, height = 600, 600
screen = pygame.display.set_mode((width, height))

# Clock object to control FPS rate
clock = pygame.time.Clock()
fps = 60


class TheGrid:

    def __init__(self):
        self.grid = np.zeros((int((width / particle_size) + 2), int(height / particle_size)))    # Creates the grid based on the particle size
        
        # particles positions
        self.sand_positions = [] 
        self.water_positions = []
        self.wall_positions = []
        
        # Colors
        self.BACKGROUND_COLOR:tuple = (0, 0, 0)
        self.SAND_COLOR:tuple = (197, 175, 128)
        self.WATER_COLOR:tuple = (77, 200, 253)
        self.WALL_COLOR:tuple = (155, 155, 155)
        self.TEXT_COLOR:tuple = (255, 255, 255)


    def sand(self, mouseX, mouseY): # Adds sand particles
        gridX, gridY = int(mouseX / particle_size), int(mouseY / particle_size)

        if self.grid[gridX][gridY] == 0:
            self.grid[gridX][gridY] = 1
            for _ in range(particle_number):
                self.sand_positions.append([gridX * particle_size, gridY * particle_size])
                
    
    def water(self, mouseX, mouseY): # Adds water particles
        gridX, gridY = int(mouseX / particle_size), int(mouseY / particle_size)

        if self.grid[gridX][gridY] == 0:
            self.grid[gridX][gridY] = 2
            for _ in range(particle_number):
                self.water_positions.append([gridX * particle_size, gridY * particle_size])
                

    def wall(self, mouseX, mouseY): # Adds a solid wall particle particles
        gridX, gridY = int(mouseX / particle_size), int(mouseY / particle_size)
        
        if self.grid[gridX][gridY] == 0:
            self.grid[gridX][gridY] = 3
            self.wall_positions.append([gridX * particle_size, gridY * particle_size])


    def create(self, screen):    # Draws the particles
        for particles in self.sand_positions:
            pygame.draw.rect(screen, self.SAND_COLOR, (particles[0], particles[1], particle_size, particle_size), 0)
        
        for particles in self.water_positions:
            pygame.draw.rect(screen, self.WATER_COLOR, (particles[0], particles[1], particle_size, particle_size), 0)

        for particles in self.wall_positions:
            pygame.draw.rect(screen, self.WALL_COLOR, (particles[0], particles[1], particle_size, particle_size), 0)


    def update_sand_positions(self): # Updates the position of sand particles
        for particle in self.sand_positions:
            x, y = particle
            gridX, gridY = int(x / particle_size), int(y / particle_size)
            
            # Checks the screen limits
            if gridX >= 0 and gridX < self.grid.shape[0] and gridY >= 0 and gridY < self.grid.shape[1] - 1:
               
                # Checks if it can move downwards
                if self.grid[gridX][gridY + 1] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX][gridY + 1] = 1
                    particle[:] = [x, y + particle_size]

                # Checks if both lower diagonals are free and chooses one to slide down
                elif gridX < self.grid.shape[0] - 1 and  self.grid[gridX + 1][gridY + 1] == 0 and self.grid[gridX - 1][gridY + 1] == 0:
                    direction = choice([1, -1])
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX + direction][gridY + 1] = 1
                    particle[:] = [x + (particle_size * direction), y + particle_size]

                # Checks if the lower right diagonal is free and slides down to it    
                elif gridX < self.grid.shape[0] - 1 and self.grid[gridX + 1][gridY + 1] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX + 1][gridY + 1] = 1
                    particle[:] = [x + particle_size, y + particle_size]
                
                # Checks if the lower left diagonal is free and slides down to it    
                elif self.grid[gridX - 1][gridY + 1] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX - 1][gridY + 1] = 1
                    particle[:] = [x - particle_size, y + particle_size]

    def update_water_positions(self): # Updates the position of water particles
        for particle in self.water_positions:
            x, y = particle
            gridX, gridY = int(x / particle_size), int(y / particle_size)
            
            # Checks the screen limits
            if gridX >= 0 and gridX < self.grid.shape[0] and gridY >= 0 and gridY < self.grid.shape[1]:
                
                # Checks if it can move downwards
                if gridY < self.grid.shape[1] - 1 and self.grid[gridX][gridY + 1] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX][gridY + 1] = 2
                    particle[:] = [x, y + particle_size]
                
                #Checks if the water can move to both sides
                elif gridX < self.grid.shape[0] - 1 and self.grid[gridX + 1][gridY] == 0 and self.grid[gridX - 1][gridY] == 0:
                    direction = choice([1, -1])
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX + direction][gridY] = 2
                    particle[:] = [x + (direction * particle_size), y]
                
                # Checks if the water can move to the right
                elif gridX < self.grid.shape[0] - 1 and self.grid[gridX + 1][gridY] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX + 1][gridY] = 2
                    particle[:] = [x + particle_size, y]

                #Checks if the water can move to the left
                elif self.grid[gridX - 1][gridY] == 0:
                    self.grid[gridX][gridY] = 0
                    self.grid[gridX - 1][gridY] = 2
                    particle[:] = [x - particle_size, y]


    def display_text(self, text): # Shows instrutions on screen
        font = pygame.font.Font(None, 27)
        text1 = font.render(text, True, self.TEXT_COLOR)
        text_rect = text1.get_rect(center = (width // 2, 15))
        screen.blit(text1, text_rect)



def main(start_time, elapsed_time):

    # Main loop
    while True:

        #start2 = time()

        # Shows some informations
        pygame.display.set_caption(f"sand Simulator  |  FPS: {int(clock.get_fps())}  |  Number of Particles: {len(universe.sand_positions) + len(universe.water_positions)}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #mouse_buttons = pygame.mouse.get_pressed()
            key = pygame.key.get_pressed()

            if key[pygame.K_1]:
                pos = pygame.mouse.get_pos()
                universe.sand(pos[0] - pos[0] % particle_size, pos[1] - pos[1] % particle_size)
            
            if key[pygame.K_2]:
                pos = pygame.mouse.get_pos()
                universe.water(pos[0] - pos[0] % particle_size, pos[1] - pos[1] % particle_size)

            if key[pygame.K_3]:
                pos = pygame.mouse.get_pos()
                universe.wall(pos[0] - pos[0] % particle_size, pos[1] - pos[1] % particle_size)
                

        # Fill the screen with a color
        screen.fill(universe.BACKGROUND_COLOR)

        # Shows instructions
        if elapsed_time < 10:
            universe.display_text("Particles options:     1 = Sand    2 = Water   3 = Wall")
            elapsed_time = time() - start_time
        
        # Updates Particle Positions
        universe.update_sand_positions()
        universe.update_water_positions()

        # Draws the particles
        universe.create(screen)

        # Updates the display
        pygame.display.flip()
        
        # FPS rate
        clock.tick(fps)

        #end2 = time()
        #print(end2 - start2)


if __name__ == '__main__':
    universe = TheGrid()
    while True:
        main(start_time, elapsed_time)
