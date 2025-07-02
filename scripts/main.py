import pygame
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.wave_manager import WaveManager
from scripts.game_state import player_speed
from scripts.bullet import Bullet
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = Player(400, 300)
wave_manager = WaveManager()

running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(player_speed["value"], screen)
    player.draw(screen)

    wave_manager.update(player, screen)

    # 🧪 TEST BULLET ON FIRST ENEMY
    if wave_manager.enemies and not hasattr(player, "test_bullet_spawned"):
        enemy = wave_manager.enemies[0]
        print("Injecting test bullet on enemy position")
        player.bullets.append(Bullet(enemy.rect.x, enemy.rect.y, (1, 0)))

        player.test_bullet_spawned = True

    pygame.display.flip()

pygame.quit()
