import pygame

class Map():
    def __init__(self, game_settings, screen):
        
        self.screen = screen
        self.hud_width = game_settings.hud_width
        self.hud_height = game_settings.hud_height
        self.color = game_settings.hud_color
        self.hud_frame_width = game_settings.hud_frame_width
        self.map_hud_ratio = game_settings.map_hud_ratio
        self.location_indicator_scaling = game_settings.map_scalar
        self.movement_scalar = self.map_hud_ratio * self.location_indicator_scaling
        self.indicator_color = game_settings.hud_indicator_color
        self.rect = pygame.Rect(0, 0, int(self.hud_width / self.location_indicator_scaling)-8, int(self.hud_height / self.location_indicator_scaling)-8)
        self.rect.y = 4
        self.rect.x = 4
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
        
        
    def update(self, dx, dy):
        
        self.x += dx / self.movement_scalar
        self.rect.x = self.x
        self.y += dy / self.movement_scalar
        self.rect.y = self.y
    
    def draw(self, ship, enemies, hyperspeed):
        ship_location = int(ship.counter.x / self.movement_scalar), int(ship.counter.y/self.movement_scalar)
        
        for enemy in enemies:
            enemy_location = int(enemy.counterx / self.movement_scalar), int(enemy.countery / self.movement_scalar)
            pygame.draw.rect(self.screen, self.indicator_color, pygame.Rect(enemy_location[0], enemy_location[1], 2, 2))
            
        
        pygame.draw.rect(self.screen, self.color, pygame.Rect(ship_location[0], ship_location[1], 2, 2))
        pygame.draw.rect(self.screen, self.color, pygame.Rect(0, 0, self.hud_width, self.hud_height), self.hud_frame_width)
        pygame.draw.rect(self.screen, self.indicator_color, self.rect, int(self.hud_frame_width/ 2))
        
# TODO: ISSUE, Enemy radar is offest after moving maps in hyperspeed
# probably some calculation error using enemy counter position