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

        # Prevent freezing when very close
        if dist < 1:
            dist = 1

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
        super().__init__(x, y, width=20, height=20, speed=3.7, health=1, damage=1)
        self.color = (0, 255, 255)  # Cyan


class TankEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=50, height=50, speed=2.5, health=16, damage=3)
        self.color = (100, 100, 100)  # Gray


class NormalEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, width=28, height=28, speed=3, health=5, damage=2)
        self.color = (255, 165, 0)  # Orange
class BossHelper(Enemy):
    def __init__(self, x, y, boss):
        super().__init__(x, y, width=20, height=20, speed=3.0, health=5, damage=0)
        self.color = (0, 200, 0)
        self.boss = boss
        self.last_heal_time = pygame.time.get_ticks()

    def update(self, player):
        # Move toward boss to heal it
        dx = self.boss.rect.centerx - self.rect.centerx
        dy = self.boss.rect.centery - self.rect.centery
        dist = max((dx**2 + dy**2)**0.5, 1)
        self.rect.x += (dx / dist) * self.speed
        self.rect.y += (dy / dist) * self.speed

        # Heal boss if close
        if self.rect.colliderect(self.boss.rect):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_heal_time >= 500:
                self.boss.health = min(self.boss.health + 3.5, self.boss.max_health)
                self.last_heal_time = current_time


class BossEnemy(Enemy):
    def __init__(
        self, x, y,
        width=80,
        height=80,
        speed=4.2,
        health=60,
        damage=50,
        color=(128, 0, 128)  # Deep purple
    ):
        super().__init__(x, y, width=width, height=height, speed=speed, health=health, damage=damage)
        self.color = color
