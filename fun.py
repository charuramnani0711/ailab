import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zodiac Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (255, 223, 186)  # Light color for text

# Load assets (images, sounds, etc.)
background = pygame.image.load("background.png")  # Replace with actual file path
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
zodiac_images = {  # Placeholder, you should replace these with actual images for each zodiac
    "Aries": pygame.image.load("aries.png"),
    "Taurus": pygame.image.load("taurus.png"),
    # Add other zodiac images here
}

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Game state
current_scene = "intro"
character_x = WIDTH // 2
character_y = HEIGHT - 100  # Character starts at the bottom
zodiac_x = WIDTH // 2
zodiac_y = -100  # Starts off-screen above

# Function to display text
def display_text(text, y_offset=100):
    lines = text.split("\n")
    max_width = max(font.size(line)[0] for line in lines)
    text_surface = pygame.Surface((max_width + 20, len(lines) * 40 + 20), pygame.SRCALPHA)
    screen.blit(text_surface, (50, y_offset - 10))
    
    # Render the text
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, FONT_COLOR)
        screen.blit(text_surface, (60, y_offset + i * 40))

# Function to handle scene transitions and zodiac interaction
def handle_scene():
    global current_scene, zodiac_x, zodiac_y
    
    screen.fill(BLACK)
    screen.blit(background, (0, 0))  # Draw the background
    
    if current_scene == "intro":
        display_text("Welcome to the Zodiac Adventure!\n\nWhich sign would you like to interact with?", 100)
        display_text("Press 1 for Aries\nPress 2 for Taurus", 300)
    
    # Animate the zodiac sign
    if zodiac_y < HEIGHT // 2:  # Move the zodiac sign towards the player
        zodiac_y += 5
    
    screen.blit(zodiac_images["Aries"], (zodiac_x, zodiac_y))  # Example for Aries

    pygame.display.flip()

# Main game loop
def game_loop():
    global current_scene
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_scene = "Aries"
                elif event.key == pygame.K_2:
                    current_scene = "Taurus"
        
        handle_scene()
        pygame.time.Clock().tick(60)

    pygame.quit()

# Start the game
game_loop()
