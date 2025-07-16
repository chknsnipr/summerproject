import pygame
from scripts.bullet import Bullet
import math
import random

class Weapon:
    def __init__(self, player):
        self.player = player
        self.cooldown = 0

    def shoot(self):
        pass

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1


class Shotgun(Weapon):
    def __init__(self, player):
        super().__init__(player)

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cooldown <= 0:
            for i in range(5): 
                angle = random.uniform(-0.6, 0.6)
                dir_x, dir_y = (0, -1)
                rotated = pygame.math.Vector2(dir_x, dir_y).rotate_rad(angle)
                bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, rotated, speed=5, range=60, damage=.65)
                self.player.bullets.append(bullet)
            self.cooldown = 40


class Sniper(Weapon):
    def __init__(self, player):
        super().__init__(player)

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cooldown <= 0:
            bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, (0, -1), speed=15, range=800, damage=8)
            self.player.bullets.append(bullet)
            self.cooldown = 60 

class SMG(Weapon):
    def __init__(self, player):
        super().__init__(player)

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cooldown <= 0:
            bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, (0, -1), speed=6, range=200, damage=0.4)
            self.player.bullets.append(bullet)
            self.cooldown = 4 
