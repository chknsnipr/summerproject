import pygame
from scripts.player import Player
from scripts.bullet import Bullet
from scripts.wave_manager import WaveManager

pygame.init()
pygame.font.init()


def draw_player_health(surface, player):
    bar_x, bar_y = 20, 20
    bar_width = 200
    bar_height = 20
    health_ratio = player.health / player.max_health

    pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height)) 
    pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))  
    pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2) 

def draw_player_perks(surface, player):
    font = pygame.font.SysFont(None, 24)
    y_offset = 50 + 30 

    surface.blit(font.render("Perks:", True, (255, 255, 255)), (20, y_offset))
    for i, perk in enumerate(player.perk_names):

        text = font.render(f"- {perk}", True, (200, 200, 200))
        surface.blit(text, (20, y_offset + 20 + (i * 20)))

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Top-Down Shooter")


player = Player(400, 300)
player_group = pygame.sprite.Group(player)
player_bullets = pygame.sprite.Group()
player.perk_names.append("Fast Reload")
player.perk_names.append("Double Damage")


wave_manager = WaveManager(screen.get_rect(), player, player_bullets)


running = True
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(player_bullets)
    player_bullets.update()
    wave_manager.update()

    if player.health <= 0:
        print("Game Over")
        running = False

    screen.fill((0, 0, 0))  
    player_group.draw(screen)
    player_bullets.draw(screen)         # ✅ Make sure bullets get drawn
    wave_manager.draw(screen)

    draw_player_health(screen, player)  # ✅ Health UI
    draw_player_perks(screen, player)   # ✅ Perk UI

    pygame.display.flip()

pygame.quit()
