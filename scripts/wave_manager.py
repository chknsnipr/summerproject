import pygame
import random
from scripts.enemy import ScoutEnemy, TankEnemy, NormalEnemy
from scripts.enemy import BossHelper
from scripts.game_state import player_speed
from scripts.enemy import BossEnemy

class WaveManager:
    def __init__(self):
        self.enemies = []
        self.wave = 0
        self.boss_spawned = False
        self.game_over = False
        self.explosions = []
        self.boss = None
        self.last_helper_spawn = 0
        self.awaiting_weapon_choice = False
        self.weapon_offer = None
        self.weapon_prompt_ready = False


    def spawn_wave(self):
        for _ in range(5 + self.wave):
            x, y = random.randint(0, 800), random.randint(0, 600)
            self.enemies.append(random.choice([ScoutEnemy, NormalEnemy, TankEnemy])(x, y))

    def spawn_boss(self):
        self.boss = BossEnemy(400, 300)
        self.enemies.append(self.boss)
        self.last_helper_spawn = pygame.time.get_ticks()

    def handle_explosion(self, player):
        if not player.trigger_explosion:
            return

        player.trigger_explosion = False
        self.explosions.append((player.rect.center, pygame.time.get_ticks()))
        for enemy in self.enemies[:]:
            dist = ((player.rect.centerx - enemy.rect.centerx) ** 2 + (player.rect.centery - enemy.rect.centery) ** 2) ** 0.5
            if dist <= 150:
                damage = 5
                if isinstance(enemy, TankEnemy):
                    damage *= (1 + player.perk_mods.tank_damage_bonus)
                if enemy.take_damage(damage):
                    self.enemies.remove(enemy)
                    self.try_drop_weapon()

    def try_drop_weapon(self):
        if not self.awaiting_weapon_choice and random.random() < 0.3:
            self.weapon_offer = random.choice(["shotgun", "sniper", "smg"])
            self.awaiting_weapon_choice = True

    def draw_explosions(self, screen):
        now = pygame.time.get_ticks()
        for pos, start_time in self.explosions[:]:
            if now - start_time < 500:
                alpha = max(0, 255 - int(255 * ((now - start_time) / 500)))
                radius = 50 + int(50 * ((now - start_time) / 500))
                surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 100, 0, alpha), (radius, radius), radius)
                screen.blit(surf, (pos[0] - radius, pos[1] - radius))
            else:
                self.explosions.remove((pos, start_time))

    def update(self, player, screen):
        if self.game_over: return

        self.handle_explosion(player)
        for enemy in self.enemies[:]:
            enemy.update(player)
            enemy.draw(screen)
            if enemy.rect.colliderect(player.rect):
                player.health -= enemy.collision_damage
                player.health = max(0, player.health)
                self.enemies.remove(enemy)
                if player.health <= 0:
                    self.game_over = True
                    return

            for bullet in player.bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    player.bullets.remove(bullet)

                    # Base damage based on player's current weapon
                    if player.weapon == "shotgun":
                        damage = 1
                    elif player.weapon == "sniper":
                        damage = 8
                    elif player.weapon == "smg":
                        damage = 0.4
                    else:
                        damage = 1  # default pistol

                    # Apply boss damage bonus if relevant
                    if isinstance(enemy, BossEnemy):
                        damage *= (1 + player.perk_mods.boss_damage_bonus)

                    if enemy.take_damage(damage):
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                    break

        self.draw_explosions(screen)

        if self.boss and self.boss in self.enemies:
            if pygame.time.get_ticks() - self.last_helper_spawn > 2000:
                self.enemies.append(BossHelper(random.randint(0, 800), random.randint(0, 600), self.boss))
                self.last_helper_spawn = pygame.time.get_ticks()

        if not self.enemies:
            self.wave += 1
            player_speed["value"] = min(player_speed["value"] + 0.2, 8.0)
            player.can_explode = True
            player.health = min(player.health + player.perk_mods.health_per_wave, 10)
            if self.wave < 5:
                self.spawn_wave()
            elif self.wave == 5 and not self.boss_spawned:
                self.spawn_boss()
                self.boss_spawned = True