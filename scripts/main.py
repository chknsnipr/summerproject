
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
player.trigger_explosion = False
wave_manager = WaveManager()
enemy_bullets = []

# Fonts
big_font = pygame.font.SysFont(None, 64)
ui_font = pygame.font.SysFont("Arial", 24)

running = True
while running:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if wave_manager.awaiting_weapon_choice and not wave_manager.weapon_prompt_ready:
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_y, pygame.K_n):
                    wave_manager.weapon_prompt_ready = True
        elif wave_manager.awaiting_weapon_choice and wave_manager.weapon_prompt_ready:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    player.weapon = wave_manager.weapon_offer
                    wave_manager.awaiting_weapon_choice = False
                    wave_manager.weapon_prompt_ready = False
                elif event.key == pygame.K_n:
                    wave_manager.awaiting_weapon_choice = False
                    wave_manager.weapon_prompt_ready = False

    if not wave_manager.game_over and not wave_manager.awaiting_weapon_choice:
        player.update(player_speed["value"], screen)
        player.draw(screen)
        wave_manager.update(player, screen)



        for bullet in enemy_bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if not screen.get_rect().contains(bullet.rect):
                enemy_bullets.remove(bullet)

        wave_text = ui_font.render(f"Wave: {wave_manager.wave}", True, (255, 255, 255))
        screen.blit(wave_text, (800 - wave_text.get_width() - 10, 10))
    elif wave_manager.awaiting_weapon_choice:
        pause_text = big_font.render("New Weapon Found!", True, (255, 255, 0))
        instr1 = ui_font.render(f"Use {wave_manager.weapon_offer.upper()}?", True, (255, 255, 255))
        instr2 = ui_font.render("Press Y to Accept, N to Decline", True, (200, 200, 200))
        screen.blit(pause_text, (200, 200))
        screen.blit(instr1, (200, 270))
        screen.blit(instr2, (200, 310))
    else:
        text = big_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (250, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
