import pygame
from scripts.bullet import Bullet
import random

class Player:
    class PerkMods:
        def __init__(self):
            self.tank_damage_bonus = 0.0
            self.boss_damage_bonus = 0.0
            self.shoot_speed_multiplier = 1.0
            self.speed_multiplier = 1.0
            self.extra_explosions = 0
            self.health_per_wave = 3

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (0, 255, 0)
        self.bullets = []
        self.health = 10
        self.shoot_cooldown = 1
        self.can_explode = True
        self.trigger_explosion = False
        self.perk_mods = Player.PerkMods()
        self.weapon = "pistol"

    def handle_input(self, speed):
        keys = pygame.key.get_pressed()
        adjusted_speed = speed * self.perk_mods.speed_multiplier
        if keys[pygame.K_w]: self.rect.y -= adjusted_speed
        if keys[pygame.K_s]: self.rect.y += adjusted_speed
        if keys[pygame.K_a]: self.rect.x -= adjusted_speed
        if keys[pygame.K_d]: self.rect.x += adjusted_speed

        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

    def shoot(self):
        keys = pygame.key.get_pressed()
        direction = None
        if keys[pygame.K_UP]: direction = (0, -1)
        elif keys[pygame.K_DOWN]: direction = (0, 1)
        elif keys[pygame.K_LEFT]: direction = (-1, 0)
        elif keys[pygame.K_RIGHT]: direction = (1, 0)

        if direction and self.shoot_cooldown <= 0:
            if self.weapon == "pistol":
                self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, direction, speed=8, damage=1))
                self.shoot_cooldown = 10 * self.perk_mods.shoot_speed_multiplier
            elif self.weapon == "sniper":
                self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, direction, speed=20, damage=8))
                self.shoot_cooldown = 60
            elif self.weapon == "smg":
                self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, direction, speed=10, damage=0.4))
                self.shoot_cooldown = 4
            elif self.weapon == "shotgun":
                for angle in [-0.2, -0.1, 0, 0.1, 0.2]:
                    self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, direction, speed=6, damage=0.7, spread=angle))
                self.shoot_cooldown = 20

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
            if not screen.get_rect().contains(bullet.rect):
                self.bullets.remove(bullet)

    def handle_explosion(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and self.can_explode:
            self.trigger_explosion = True
            self.can_explode = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.SysFont("Arial", 20)
        bar_width, bar_height = 60, 10
        x, y = 10, 10

        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (x, y, int(bar_width * self.health / 10), bar_height))

        surface.blit(font.render(f"Health: {self.health}/10", True, (255, 255, 255)), (x, y + bar_height + 5))

        status_text = "Explosion: READY" if self.can_explode else "Explosion: USED"
        status_color = (0, 255, 0) if self.can_explode else (255, 0, 0)
        surface.blit(font.render(status_text, True, status_color), (x, y + 30))

        weapon_text = font.render(f"Weapon: {self.weapon.upper()}", True, (0, 200, 255))
        surface.blit(weapon_text, (x, y + 55))

    def apply_perk(self, rarity):
        pass  # already defined in earlier version