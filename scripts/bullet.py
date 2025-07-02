import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 12, 12)       # ✅ hitbox is fine
        self.color = (255, 255, 0)                  # ✅ visible color
        self.speed = 8                              # ✅ decent speed
        self.direction = direction                  # ⚠️ must be a (x, y) tuple

    def update(self):
        self.rect.x += self.direction[0] * self.speed  # ✅ moves with direction
        self.rect.y += self.direction[1] * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # ✅ simple draw
