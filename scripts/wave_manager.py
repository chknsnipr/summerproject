import pygame
import random
from scripts.enemy import Enemy, TankEnemy, BossEnemy, EnemyBullet

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.radius = 30
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 165, 0, 128), (30, 30), 30)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        self.radius -= 1
        if self.radius <= 0:
            self.kill()
        else:
            self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 165, 0, 128), (self.radius, self.radius), self.radius)
            self.rect = self.image.get_rect(center=self.rect.center)

class WaveManager:
    def __init__(self, screen_rect, player):
        self.screen_rect = screen_rect
        self.player = player
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.wave_number = 0
        self.spawn_index = 0
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_delay = 500
        self.wave_in_progress = False
        self.next_wave_timer = 0
        self.enemies_to_spawn = []
        self.start_next_wave()

    def start_next_wave(self):
        self.wave_number += 1
        self.enemies_to_spawn = []
        self.spawn_index = 0
        self.wave_in_progress = True

        if self.wave_number % 5 == 0:
            self.enemies_to_spawn.append(("boss", 1))
        else:
            for _ in range(self.wave_number * 2):
                self.enemies_to_spawn.append((random.choice(["normal", "tank"]), 1))

    def spawn_enemy(self, enemy_type):
        x = random.randint(50, self.screen_rect.width - 50)
        y = random.randint(50, self.screen_rect.height // 3)
        if enemy_type == "normal":
            enemy = Enemy(x, y)
        elif enemy_type == "tank":
            enemy = TankEnemy(x, y, self)
        elif enemy_type == "boss":
            enemy = BossEnemy(x, y, self)
        self.enemies.add(enemy)

    def update(self):
        now = pygame.time.get_ticks()

        # Spawn handling
        if self.wave_in_progress and self.spawn_index < len(self.enemies_to_spawn):
            if now - self.last_spawn >= self.spawn_delay:
                kind, count = self.enemies_to_spawn[self.spawn_index]
                for _ in range(count):
                    self.spawn_enemy(kind)
                self.spawn_index += 1
                self.last_spawn = now

        elif self.wave_in_progress and not self.enemies:
            self.wave_in_progress = False
            self.next_wave_timer = now + 3000

        elif not self.wave_in_progress and now >= self.next_wave_timer:
            self.start_next_wave()

        self.enemies.update(self.player)
        self.enemy_bullets.update()
        self.explosions.update()

        # Collisions
        for bullet in pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.player.take_damage(bullet.damage)

        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.player.take_damage(enemy.damage)

        for enemy in list(self.enemies):
            if hasattr(enemy, 'health') and enemy.health <= 0:
                self.explosions.add(Explosion(enemy.rect.center))
                enemy.kill()

    def draw(self, surface):
        self.enemies.draw(surface)
        self.enemy_bullets.draw(surface)
        self.explosions.draw(surface)
