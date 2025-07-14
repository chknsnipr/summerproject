# enemy.py
import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None, health=1, damage=10):
        super().__init__()
        self.image = image if image else pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health
        self.damage=damage 


    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(math.hypot(dx, dy), 0.01)
        self.rect.x += int(2 * dx / dist)
        self.rect.y += int(2 * dy / dist)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, damage=5):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(dx, dy)
        self.damage = 20

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

class TankEnemy(Enemy):
    def __init__(self, x, y, wave_manager):
        super().__init__(x, y, health=15, damage=10)
        self.image.fill((255, 0, 0))
        self.wave_manager = wave_manager
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.damage = 10  # or whatever value
        self.health=20

    def update(self, player):
        super().update(player)
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(math.hypot(dx, dy), 0.01)
            speed = 30
            vx, vy = dx / dist * speed, dy / dist * speed
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, vx, vy, damage=5)
            self.wave_manager.enemy_bullets.add(bullet)
            self.last_shot = now

class BossEnemy(Enemy):
    def __init__(self, x, y, wave_manager):
        super().__init__(x, y, health=40, damage=20)
        self.image.fill((100, 0, 255))
        self.wave_manager = wave_manager
        self.last_shot = pygame.time.get_ticks()
        self.last_special_attack = pygame.time.get_ticks()
        self.shoot_delay = 800
        self.special_cooldown = 3000
        self.special_width = 50
        self.special_damage = 6
        self.damage = 10  # or whatever value
        self.health=100


    def update(self, player):
        super().update(player)
        now = pygame.time.get_ticks()

        # Shoot bullets
        if now - self.last_shot >= self.shoot_delay:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(math.hypot(dx, dy), 0.01)
            speed = 10
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed, damage=10)
            self.wave_manager.enemy_bullets.add(bullet)
            self.last_shot = now

        # Special diagonal attack
        if now - self.last_special_attack >= self.special_cooldown:
            if abs(player.rect.centerx - self.rect.centerx) == abs(player.rect.centery - self.rect.centery):
                player.take_damage(self.special_damage)
            self.last_special_attack = now
