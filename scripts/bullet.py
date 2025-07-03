import pygame
import math

class Bullet:
    def __init__(self, x, y, direction, speed=8, damage=1, spread=0):
        self.rect = pygame.Rect(x, y, 6, 6)
        self.color = (255, 255, 0)
        self.speed = speed
        self.damage = damage

        # Apply spread to direction (used for shotgun)
        angle = math.atan2(direction[1], direction[0]) + spread
        self.direction = (math.cos(angle), math.sin(angle))

    def update(self):
        self.rect.x += int(self.direction[0] * self.speed)
        self.rect.y += int(self.direction[1] * self.speed)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
