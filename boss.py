import pygame
from pygame.sprite import Sprite
import math
import game_functions

class Boss(Sprite):
    def __init__(self, game_settings, screen, ship):
        super(Boss, self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.original_image = pygame.image.load('images/SS Boss.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.angle = 0
        
        self.movement_angle = 1
        self.movement_angle_speed = game_settings.boss_starting_speed_min
        self.move_direction = 1
        self.movement_radius = int(game_settings.screen_height / 2) - 32
        self.movement_center = int(game_settings.screen_width / 2), int(game_settings.screen_height / 2)
        self.laser_cool_down_default = game_settings.boss_starting_laser_cool_down_min
        self.laser_cool_down = self.laser_cool_down_default
        self.laser_duration_default = game_settings.boss_starting_laser_duration_min
        self.laser_duration = self.laser_duration_default
        
        self.x = self.movement_center[0]
        self.y = self.movement_center[1]
        self.rect.x = self.x
        self.rect.y = self.y

        self.current_target = ship

    def draw(self):
        self.screen.blit(self.image, self.rect)
        
    def update(self, ship, lasers, boss_turn, hyperspeed):
        self.aimAtShip(ship)
        if not boss_turn:
            
            y = math.sin(math.radians(self.movement_angle)) * self.movement_radius + self.movement_center[1]
            x = math.cos(math.radians(self.movement_angle)) * self.movement_radius + self.movement_center[0]
            
            self.x = x
            self.rect.x = self.x
            self.y = y
            self.rect.y = self.y
            
        if self.laser_cool_down  <=  0:
            if self.laser_duration > 0:
                game_functions.shoot_boss_laser(self.game_settings, self.screen, self, lasers)
                self.laser_duration -= 1 * hyperspeed
                return True
            else:
                self.movement_angle += self.movement_angle_speed * self.move_direction
                self.laser_cool_down = self.laser_cool_down_default
                self.laser_duration = self.laser_duration_default
                return False
                
        else:
            self.laser_cool_down -= 1 * hyperspeed
            self.movement_angle += self.movement_angle_speed * hyperspeed * self.move_direction
            self.movement_angle = self.movement_angle % 360
            return False
    
    def aimAtShip(self, ship):
        aim_angle = 0
        
        if (self.rect.y - ship.rect.y) != 0:
            aim_angle = abs(math.degrees(math.atan2((self.rect.x - ship.rect.x), (self.rect.y - ship.rect.y))))
        if (self.rect.x - ship.rect.x <= 0):
            aim_angle = 360.0 - aim_angle
        self.angle = aim_angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        