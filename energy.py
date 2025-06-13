import pygame

class Shield():
    def __init__(self, game_settings, screen, ship):
        self.screen = screen
        self.x = 0
        self.y = game_settings.hud_height
        self.hud_width = game_settings.hud_width
        self.hud_height = game_settings.hud_height / 8
        self.hud_frame_width = game_settings.hud_frame_width
        self.energy_color = game_settings.hud_color
        self.energy_max = ship.energy_max
        self.enemy_color = game_settings.hud_indicator_color
    

    def draw(self, ship, enemies, bosses, total_health):
        ratio = ship.energy_current / self.energy_max
        pygame.draw.rect(self.screen, self.energy_color, pygame.Rect(0, self.y, self.hud_width, self.hud_height), self.hud_frame_width)
        pygame.draw.rect(self.screen, self.energy_color, (0, self.y, self.hud_width * ratio, self.hud_height))
        if total_health > 0:
            if len(enemies) > 0:
                total = 0
                for enemy in enemies:
                    total += enemy.hit_points
                enemy_ratio = total / total_health
                pygame.draw.rect(self.screen, self.enemy_color, pygame.Rect(0, self.y + self.hud_height, self.hud_width, self.hud_height), self.hud_frame_width)
                pygame.draw.rect(self.screen, self.enemy_color, (0, self.y + self.hud_height, self.hud_width * enemy_ratio, self.hud_height))
            if len(bosses) > 0:
                total = 0
                for boss in bosses:
                    total += boss.hit_points
                enemy_ratio = total / total_health
                pygame.draw.rect(self.screen, self.enemy_color, pygame.Rect(0, self.y + self.hud_height, self.hud_width, self.hud_height), self.hud_frame_width)
                pygame.draw.rect(self.screen, self.enemy_color, (0, self.y + self.hud_height, self.hud_width * enemy_ratio, self.hud_height))