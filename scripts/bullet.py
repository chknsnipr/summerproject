import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, damage=10):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.damage = damage
        # Normalize the direction vector and multiply by speed
        if isinstance(direction, pygame.math.Vector2):
            if direction.length() != 0:
                self.velocity = direction.normalize() * speed
            else:
                self.velocity = pygame.math.Vector2(0, 0)
        else:
            # fallback if you pass (dx, dy)
            dx, dy = direction
            vec = pygame.math.Vector2(dx, dy)
            if vec.length() != 0:
                self.velocity = vec.normalize() * speed
            else:
                self.velocity = pygame.math.Vector2(0, 0)

     

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
