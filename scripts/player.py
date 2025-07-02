import pygame
from scripts.bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (0, 255, 0)
        self.bullets = []
        self.health = 8
        self.shoot_cooldown = 1
        self.can_explode = True
        self.trigger_explosion = False  # Needed by wave_manager

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
            self.shoot_cooldown = 10

    def update(self, speed, screen):
        self.handle_input(speed)
        self.shoot()
        self.update_bullets(screen)
        self.handle_explosion()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def update_bullets(self, screen):
        for bullet in self.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if (
                bullet.rect.x < 0 or bullet.rect.x > 800 or
                bullet.rect.y < 0 or bullet.rect.y > 600
            ):
                self.bullets.remove(bullet)

    def handle_explosion(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and self.can_explode:
            self.trigger_explosion = True
            self.can_explode = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        # Optional: Draw health bar
        bar_width = 60
        bar_height = 10
        x = 10
        y = 10
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        green_width = int(bar_width * (self.health / 8))
        pygame.draw.rect(surface, (0, 255, 0), (x, y, green_width, bar_height))
