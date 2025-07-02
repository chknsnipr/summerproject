import pygame
from scripts.player import Player
from scripts.wave_manager import WaveManager
from scripts.game_state import player_speed

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Top-Down Wave Shooter")
clock = pygame.time.Clock()

# Game objects
player = Player(400, 300)
player.trigger_explosion = False  # ✅ Required for explosion to work
wave_manager = WaveManager()

# Fonts for text
font = pygame.font.SysFont(None, 64)

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not wave_manager.game_over:
        player.update(player_speed["value"], screen)
        player.draw(screen)
        wave_manager.update(player, screen)

    else:
        # Show Game Over screen
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (250, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

