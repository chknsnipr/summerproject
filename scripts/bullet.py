import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 6, 6)
        self.color = (255, 255, 0)
        self.speed = 8
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
