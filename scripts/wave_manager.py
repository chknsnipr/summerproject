import pygame
import random
from scripts.enemy import Enemy
from scripts.game_state import player_speed

class WaveManager:
    def __init__(self):
        self.enemies = []
        self.wave = 0
        self.boss_spawned = False

    def update(self, player, screen):
        # 🔫 Bullet–enemy collision
        for enemy in self.enemies[:]:
            for bullet in player.bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    print("Hit!")
                    self.enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    break  # Skip to next enemy after hit

        # 🌊 Wave management
        if not self.enemies:
            self.wave += 1

            # Increase player speed (capped at 8.0)
            from scripts import game_state
            game_state.player_speed["value"] = min(game_state.player_speed["value"] + 0.2, 8.0)
            print(f"Wave {self.wave} started. Player speed: {game_state.player_speed['value']}")

            if self.wave <= 10:
                self.spawn_wave()
            elif self.wave == 11 and not self.boss_spawned:
                self.spawn_boss()
                self.boss_spawned = True

        # 👹 Update and draw enemies
        for enemy in self.enemies[:]:
            enemy.update(player)
            enemy.draw(screen)
            if enemy.rect.colliderect(player.rect):
                print("Player hit!")
                self.enemies.remove(enemy)
                player.health -= 1
                if player.health <= 0:
                    print("Game Over!")
                    pygame.quit()
                    exit()

                print(f"Player health: {player.health}")

    def spawn_wave(self):
        for _ in range(4):  # You can increase this number for more enemies
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            speed = 1 + self.wave * 0.2
            self.enemies.append(Enemy(x, y, speed))

    def spawn_boss(self):
        from scripts.enemy import BossEnemy
        self.enemies.append(BossEnemy(400, 300))
        print("Boss has spawned!")
