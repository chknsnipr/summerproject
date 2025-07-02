import random
from scripts.enemy import ScoutEnemy, TankEnemy, NormalEnemy
from scripts.game_state import player_speed

class WaveManager:
    def __init__(self):
        self.enemies = []
        self.wave = 0
        self.boss_spawned = False
        self.game_over = False

    def spawn_wave(self):
        for _ in range(5 + self.wave):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            enemy_type = random.choice(["scout", "normal", "tank"])

            if enemy_type == "scout":
                self.enemies.append(ScoutEnemy(x, y))
            elif enemy_type == "normal":
                self.enemies.append(NormalEnemy(x, y))
            else:
                self.enemies.append(TankEnemy(x, y))

    def spawn_boss(self):
        from scripts.enemy import BossEnemy
        self.enemies.append(BossEnemy(400, 300))
        print("Boss has spawned!")

    def handle_explosion(self, player):
        # Explosion radius
        EXPLOSION_RADIUS = 150
        EXPLOSION_DAMAGE = 3

        if hasattr(player, "trigger_explosion") and player.trigger_explosion:
            print("Explosion triggered!")

            for enemy in self.enemies[:]:
                dx = player.rect.centerx - enemy.rect.centerx
                dy = player.rect.centery - enemy.rect.centery
                dist = (dx**2 + dy**2) ** 0.5
                if dist <= EXPLOSION_RADIUS:
                    print("Enemy hit by explosion!")
                    if enemy.take_damage(EXPLOSION_DAMAGE):
                        self.enemies.remove(enemy)

            player.trigger_explosion = False  # ✅ One explosion per round

    def update(self, player, screen):
        if self.game_over:
            return

        # Explosion trigger
        self.handle_explosion(player)

        for enemy in self.enemies[:]:
            enemy.update(player)
            enemy.draw(screen)

            if enemy.rect.colliderect(player.rect):
                damage = enemy.collision_damage
                player.health -= damage
                player.health = max(player.health, 0)
                print(f"Player took {damage} damage! Health: {player.health}")
                self.enemies.remove(enemy)

                if player.health <= 0:
                    print("Player is dead! Game Over.")
                    self.game_over = True
                    return

            for bullet in player.bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    print("Hit!")
                    player.bullets.remove(bullet)
                    if enemy.take_damage(1):
                        self.enemies.remove(enemy)
                    break

        if not self.enemies:
            self.wave += 1
            player_speed["value"] = min(player_speed["value"] + 0.2, 8.0)
            print(f"Wave {self.wave} started. Player speed: {player_speed['value']}")

            player.can_explode = True  # ✅ Reset explosion flag

            if self.wave < 10:
                self.spawn_wave()
            elif self.wave == 10 and not self.boss_spawned:
                self.spawn_boss()
                self.boss_spawned = True
