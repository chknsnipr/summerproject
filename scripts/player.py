import pygame
import math
from scripts.bullet import Bullet

class Player(pygame.sprite.Sprite):
    class PerkMods:
        def __init__(self):
            self.tank_damage_bonus = 0.0
            self.boss_damage_bonus = 0.0
            self.shoot_speed_multiplier = 1.0
            self.speed_multiplier = 1.0
            self.healing_bonus = 0

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))

        self.base_speed = 5
        self.health = 100
        self.max_health = 100
    

        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.weapon = "pistol"
        self.perk_mods = Player.PerkMods()  

        self.perks = self.PerkMods()
        self.velocity = pygame.math.Vector2()
        self.perk_names = []

    def update(self, bullets_group):
        self.handle_movement()
        self.handle_shooting(bullets_group)

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.velocity.y = keys[pygame.K_s] - keys[pygame.K_w]

        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize()

        speed = self.base_speed * self.perks.speed_multiplier
        self.rect.x += self.velocity.x * speed
        self.rect.y += self.velocity.y * speed

        screen_width, screen_height = 800, 600 
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(screen_height, self.rect.bottom)

    def handle_shooting(self, bullets_group):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        if dx != 0 or dy != 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot >= self.shoot_delay / self.perks.shoot_speed_multiplier:
                direction = pygame.math.Vector2(dx, dy).normalize()
                speed = 10
                bullets_group.add(Bullet(self.rect.centerx, self.rect.centery, (direction.x, direction.y), speed))
                self.last_shot = now


    def shoot(self, bullets_group):
        mx, my = pygame.mouse.get_pos()
        angle = math.atan2(my - self.rect.centery, mx - self.rect.centerx)
        speed = 15

        if self.weapon == "pistol":
            bullets_group.add(Bullet(self.rect.centerx, self.rect.centery, angle, speed))
        elif self.weapon == "shotgun":
            for offset in [-0.2, -0.1, 0, 0.1, 0.2]:
                bullets_group.add(Bullet(self.rect.centerx, self.rect.centery, angle + offset, speed))
        elif self.weapon == "sniper":
            bullets_group.add(Bullet(self.rect.centerx, self.rect.centery, angle, speed * 1.5, damage=30))
        elif self.weapon == "smg":
            for _ in range(2):
                bullets_group.add(Bullet(self.rect.centerx, self.rect.centery, angle, speed))

    def take_damage(self, amount):
        self.health -= amount
        print(f"Player took {amount} damage. Health is now {self.health}")
        if self.health <= 0:
            print("Player died")
            self.health = 0

    def heal(self, amount):
        self.health = min(self.health + amount + self.perks.healing_bonus, self.max_health)
