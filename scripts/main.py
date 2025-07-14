import pygame
from scripts.player import Player
from scripts.bullet import Bullet
from scripts.wave_manager import WaveManager

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Top-Down Shooter")

# Create player and groups
player = Player(400, 300)
player_group = pygame.sprite.Group(player)
player_bullets = pygame.sprite.Group()

# Wave manager
wave_manager = WaveManager(screen.get_rect(), player, player_bullets)

running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(player_bullets)
    if player.health <= 0:
        print("Game Over")
        running = False

    player_bullets.update()
    wave_manager.update()

    # Draw
    screen.fill((20, 20, 20))
    player_group.draw(screen)
    player_bullets.draw(screen)
    wave_manager.draw(screen)

    pygame.display.flip()

pygame.quit()

  