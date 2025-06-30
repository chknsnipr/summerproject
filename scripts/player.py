import pygame
import main

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = (0, 255, 0)
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    