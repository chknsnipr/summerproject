import pygame
import random

class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 12, 12)
        self.color = (255, 0, 0)
        self.speed = speed - .4

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist != 0:
            dx /= dist
            dy /= dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
