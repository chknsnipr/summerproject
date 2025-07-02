import pygame

class Enemy:
    def __init__(self, x, y, width, height, speed, health, damage):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.collision_damage = damage
        self.color = (255, 0, 0)

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist != 0:
            dx /= dist
            dy /= dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def take_damage(self, amount):
        self.health -= amount
        print(f"Enemy took {amount} damage, health is now {self.health}")
        return self.health <= 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        # Health bar
        bar_width = self.rect.width
        bar_height = 4
        health_ratio = max(self.health / self.max_health, 0)
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 6, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 6, bar_width * health_ratio, bar_height))


# ---------- Enemy Variants ----------

class ScoutEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=20, height=20, speed=3.0, health=1, damage=1)
        self.color = (0, 255, 255)  # Cyan


class TankEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=36, height=36, speed=1.4, health=5, damage=4)
        self.color = (100, 100, 100)  # Gray


class NormalEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=28, height=28, speed=2, health=3, damage=2)
        self.color = (255, 165, 0)  # Orange


class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=50, height=50, speed=0.5, health=50, damage=6)
        self.color = (128, 0, 128)  # Purple



