import pygame
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.wave_manager import WaveManager
from scripts.game_state import player_speed

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

    pygame.display.flip()

pygame.quit()
