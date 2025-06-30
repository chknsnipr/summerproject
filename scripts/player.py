import pygame
from scripts.bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (0, 255, 0)
        self.bullets = []
        self.shoot_cooldown = 1  # prevent too-fast shooting

    def handle_input(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= speed
        if keys[pygame.K_s]:
            self.rect.y += speed
        if keys[pygame.K_a]:
            self.rect.x -= speed
        if keys[pygame.K_d]:
            self.rect.x += speed

    def shoot(self):
        keys = pygame.key.get_pressed()
        direction = None

        if keys[pygame.K_UP]:
            direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            direction = (0, 1)
        elif keys[pygame.K_LEFT]:
            direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            direction = (1, 0)

        if direction and self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
            self.bullets.append(bullet)
            self.shoot_cooldown = 10  # frames between shots

    def update(self, speed, screen):
        self.handle_input(speed)
        self.shoot()
        self.update_bullets(screen)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def update_bullets(self, screen):
        for bullet in self.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if (bullet.rect.x < 0 or bullet.rect.x > 800 or
                bullet.rect.y < 0 or bullet.rect.y > 600):
                self.bullets.remove(bullet)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
