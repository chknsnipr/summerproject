import random
from scripts.enemy import Enemy
from scripts.game_state import player_speed

class WaveManager:
    def __init__(self):
        self.enemies = []
        self.wave = 0
        self.boss_spawned = False
    def update(self,player):
        for enemy in self.enemies:
            enemy.update(player)    
        if not self.enemies:
            self.wave +=1
            print(f"wave {self.wave} started")

            if self.wave <=10:
                self.spawn_wave()
            elif self.wave ==11 and not self.boss_spawned:
                self.spawn_boss()
                self.boss_spawned=True    
    def spawn_wave(self):
        from scripts.enemy import Enemy
        for _ in range(1):
            x= random.randint(0,800)
            y = random.randint(0,600)
            speed = 1 + self.wave *.2
            self.enemies.append(Enemy(x,y,speed))

    def update(self, player, screen):
        if not self.enemies:
           self.wave += 1

        # Increase player speed
        from scripts import game_state
        game_state.player_speed["value"] = min(game_state.player_speed["value"] + 0.2, 8.0)
        print(f"Wave {self.wave} started. Player speed:    { game_state.player_speed['value']}")

        if self.wave <= 10:
            self.spawn_wave()
        elif self.wave == 11 and not hasattr(self, "boss_spawned"):
            self.spawn_boss()
            self.boss_spawned = True

        for enemy in self.enemies[:]:
           enemy.update(player)
           enemy.draw(screen)
           if enemy.rect.colliderect(player.rect):
               self.enemies.remove(enemy)
    def spawn_boss(self):
        from scripts.enemy import BossEnemy
        self.enemies.append(BossEnemy(400, 300))
        print("Boss has spawned!")           