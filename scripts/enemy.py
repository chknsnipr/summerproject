import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, width, height, enemy_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = enemy_type
        self.speed = self.get_speed_by_type(enemy_type)
        self.health = self.get_health_by_type(enemy_type)
        self.max_health = self.health
        self.collision_damage = 10
        self.color = (255, 0, 0)
        self.alive = True

        if self.type == 'tank':
            self.shoot_cooldown = random.randint(60, 120)

    def update(self, player, enemy_bullets, explosions):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist < 1:
            dist = 1
        dx /= dist
        dy /= dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if self.type == 'tank':
            self.shoot_cooldown -= 1
            if self.shoot_cooldown <= 0:
                self.shoot_at_player(player, enemy_bullets)
                self.shoot_cooldown = 30

        elif self.type == 'normal':
            if self.rect.colliderect(player.rect):
                player.health -= 5
                explosions.append(Explosion(self.rect.centerx, self.rect.centery))
                self.alive = False

    def shoot_at_player(self, player, enemy_bullets):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dx /= dist
        dy /= dist
        bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy, speed=12, damage=.2)
        enemy_bullets.append(bullet)

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        bar_width = self.rect.width
        bar_height = 4
        health_ratio = max(self.health / self.max_health, 0)
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 6, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 6, bar_width * health_ratio, bar_height))

    def get_speed_by_type(self, enemy_type):
        if enemy_type == 'scout':
            return 4
        elif enemy_type == 'tank':
            return 1.5
        elif enemy_type == 'normal':
            return 3
        return 2

    def get_health_by_type(self, enemy_type):
        if enemy_type == 'tank':
            return 20
        elif enemy_type == 'normal':
            return 8
        elif enemy_type == 'scout':
            return 2
        return 10

class Bullet:
    def __init__(self, x, y, dx, dy, speed=7, damage=5):
        self.rect = pygame.Rect(x, y, 6, 6)
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.color = (255, 165, 0)

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Explosion:
    def __init__(self, x, y, duration=300):
        radius = 150  # match the damage radius
        size = radius * 2

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 100, 0), (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time <= self.duration

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Enemy variants
class ScoutEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=20, height=20, enemy_type='scout')
        self.color = (0, 255, 255)
        self.collision_damage=1
class TankEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=50, height=50, enemy_type='tank')
        self.color = (100, 100, 100)
        self.collision_damage=5
class NormalEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=28, height=28, enemy_type='normal')
        self.color = (255, 165, 0)
        self.collision_damage=3
class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=80, height=80, enemy_type='boss')
        self.color = (128, 0, 128)
       
        self.speed = 4.5
        self.health = 100
        self.max_health = 100
        self.collision_damage = 50

class BossHelper(Enemy):
    def __init__(self, x, y, boss):
        super().__init__(x, y, width=20, height=20, enemy_type='helper')
        self.color = (0, 200, 0)
        self.boss = boss
        self.speed = 3.0
        self.health = 5
        self.collision_damage = 0
        self.last_heal_time = pygame.time.get_ticks()

    def update(self, player, *args):
        dx = self.boss.rect.centerx - self.rect.centerx
        dy = self.boss.rect.centery - self.rect.centery
        dist = max((dx**2 + dy**2)**0.5, 1)
        self.rect.x += (dx / dist) * self.speed
        self.rect.y += (dy / dist) * self.speed

        if self.rect.colliderect(self.boss.rect):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_heal_time >= 500:
                self.boss.health = min(self.boss.health + 3.5, self.boss.max_health)
                self.last_heal_time = current_time