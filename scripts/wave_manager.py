import random
from scripts.enemy import Enemy

class WaveManager:
    def __init__(self):
        self.enemies = []
        self.wave = 1
        self.spawn_wave()

    def spawn_wave(self):
        self.enemies = [Enemy(random.randint(0, 800), random.randint(0, 600), 1 + self.wave * 0.2) for _ in range(self.wave * 3)]

    def update(self, player, screen):
        if not self.enemies:
            self.wave += 1
            self.spawn_wave()
        for enemy in self.enemies[:]:
            enemy.update(player)
            enemy.draw(screen)
            if enemy.rect.colliderect(player.rect):
                self.enemies.remove(enemy)
