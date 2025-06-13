
import pygame
from pygame.sprite import Sprite
import math

class Laser(Sprite):
    def __init__(self, game_settings, screen, shooter):
        super(Laser, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, game_settings.laser_width,game_settings.laser_height)
        self.rect.centerx = shooter.rect.centerx
        self.rect.centery = shooter.rect.centery
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.color = game_settings.laser_color
        self.laser_speed_factor = game_settings.laser_speed_factor
        self.current_target = shooter.current_target
        self.start_location = self.rect.centerx, self.rect.centery
        self.last_known_location = self.current_target.rect.centerx, self.current_target.rect.centery
        

    def update(self, dx, dy, hyperspeed):
        dx2, dy2 = self.calculate_trajectory()
        dx = -dx + dx2
        dy = -dy + dy2
        
        
        dx *= hyperspeed
        dy *= hyperspeed
        
        self.y += dy
        self.rect.centery = self.y
        self.x += dx
        self.rect.centerx = self.x
        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


    def calculate_trajectory(self):
        x_distance = self.last_known_location[0] - self.start_location[0]
        y_distance = self.last_known_location[1] - self.start_location[1]
        
        direct_distance = math.sqrt((x_distance) **2  + (y_distance) **2)
        ratio = direct_distance / self.laser_speed_factor
        if ratio != 0:
            dx = x_distance / ratio
            dy = y_distance / ratio
        else:
            dx =0
            dy = 0
        return dx, dy