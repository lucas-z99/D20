import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
background_color = (255, 255, 255)  # White
triangle_color = (0, 128, 255)  # Some color for the triangle

# Fill the background
screen.fill(background_color)

# Define the triangle's vertices
triangle_vertices = [(100, 100), (200, 50), (300, 100)]  # Example coordinates

# Draw the triangle
pygame.draw.polygon(screen, triangle_color, triangle_vertices)

# Update the display
pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Game logic and drawing code goes here

    # No need to continually redraw the static triangle in this example
