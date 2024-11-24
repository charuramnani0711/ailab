import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "idle"
        self.target = None

    def update(self, player_pos):
        if self.state == "idle":
            if self.distance_to(player_pos) < 200:
                self.state = "pursuit"
        elif self.state == "pursuit":
            self.target = player_pos
            self.move_towards(self.target)
            if self.distance_to(player_pos) > 300:
                self.state = "idle"

    def distance_to(self, target_pos):
        dx = self.x - target_pos[0]
        dy = self.y - target_pos[1]
        return (dx**2 + dy**2)**0.5

    def move_towards(self, target_pos):
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx
            self.y += dy

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Create an enemy
enemy = Enemy(200, 200)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input (replace with actual player input)
    player_pos = (400, 300)

    # Update enemy AI
    enemy.update(player_pos)

    # Draw the enemy and player
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (int(enemy.x), int(enemy.y)), 10)
    pygame.draw.circle(screen, (0, 0, 255), (int(player_pos[0]), int(player_pos[1])), 10)
    pygame.display.flip()

pygame.quit()