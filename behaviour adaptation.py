import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Behavior Adaptation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Character attributes
class Character:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)

    def move(self, target_x, target_y):
        if self.x < target_x:
            self.x += self.speed
        elif self.x > target_x:
            self.x -= self.speed
        if self.y < target_y:
            self.y += self.speed
        elif self.y > target_y:
            self.y -= self.speed

# Initialize characters
jack = Character(100, 100, RED, 4)
jill = Character(300, 300, BLUE, 2)

# Main game loop
running = True
target_x, target_y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Draw and move characters
    jack.move(target_x, target_y)
    jack.draw()
    jill.move(jack.x, jack.y)  # Jill follows Jack
    jill.draw()

    # Update target if Jack reaches it
    if abs(jack.x - target_x) < 10 and abs(jack.y - target_y) < 10:
        target_x, target_y = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
