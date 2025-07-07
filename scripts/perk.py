import pygame

# ---------- CONFIGURATION ----------

PERK_TYPES = {
    "rare": {
        "color": (255, 0, 255),
        "perks": [
            {
                "name": "Tank Slayer",
                "effect": lambda player: setattr(player.perk_mods, "tank_damage_bonus", 0.25)
            },
            {
                "name": "Rapid Fire+",
                "effect": lambda player: setattr(player.perk_mods, "shoot_speed_multiplier", 0.8)  # 20% faster
            },
            {
                "name": "Extra Explosion",
                "effect": lambda player: setattr(player.perk_mods, "extra_explosions", 1)
            },
            {
                "name": "Wave Healer++",
                "effect": lambda player: setattr(player.perk_mods, "health_per_wave", 5)
            },
        ]
    },
    "normal": {
        "color": (0, 128, 255),
        "perks": [
            {
                "name": "Faster Reload",
                "effect": lambda player: setattr(player.perk_mods, "shoot_speed_multiplier", 0.9)  # 10% faster
            },
            {
                "name": "Boss Breaker",
                "effect": lambda player: setattr(player.perk_mods, "boss_damage_bonus", 0.05)
            },
            {
                "name": "Speed Boost",
                "effect": lambda player: setattr(player.perk_mods, "speed_multiplier", 1.15)
            }
        ]
    },
    "common": {
        "color": (0, 255, 0),
        "perks": [
            {
                "name": "Heal",
                "effect": lambda player: setattr(player, "health", min(10, player.health + 1))
            }
        ]
    }
}

# ---------- Perk Object ----------

class Perk:
    def __init__(self, x, y, tier, perk_data):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.tier = tier
        self.color = PERK_TYPES[tier]["color"]
        self.name = perk_data["name"]
        self.effect_fn = perk_data["effect"]
        self.spawn_time = pygame.time.get_ticks()

    def apply(self, player):
        print(f"Applied Perk: {self.name}")
        self.effect_fn(player)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 7000
