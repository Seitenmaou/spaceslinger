import pygame
from pygame.sprite import Sprite
import math
import game_functions

class Enemy(Sprite):
    def __init__(self, game_settings, screen, ship):
        super(Enemy, self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.original_image = pygame.image.load('images/SS Enemy.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.angle = 0
        self.speed = game_settings.enemy_starting_speed_min = 0.5

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.counterx = float(self.rect.x)
        self.countery = float(self.rect.y)
        
        self.laser_cool_down_default = game_settings.enemy_starting_laser_cool_down_min
        self.laser_cool_down = self.laser_cool_down_default
        self.current_target = ship
        
        self.hit_points = game_settings.enemy_starting_hit_points

    def draw(self):
        self.screen.blit(self.image, self.rect)
        
    def update(self, dx, dy, ship, lasers, hyperspeed):
        
        dx2, dy2 = self.chaseShip(ship)
        self.counterx -= dx2 * hyperspeed
        self.countery -= dy2 * hyperspeed

        
        dx += dx2
        dy += dy2
        
        dx *= hyperspeed
        dy *= hyperspeed
        
        self.x -= dx
        self.rect.x = self.x
        self.y -= dy
        self.rect.y = self.y
        
        self.aimAtShip(ship)
        if self.laser_cool_down <= 0:
            game_functions.shoot_player(self.game_settings, self.screen, self, lasers)
            self.laser_cool_down = self.laser_cool_down_default
        else:
            self.laser_cool_down -= 1 * hyperspeed
        
        
    def chaseShip (self, ship):
        x_distance = ship.rect.centerx - self.rect.centerx
        y_distance = ship.rect.centery - self.rect.centery
        
        direct_distance = math.sqrt((x_distance) **2  + (y_distance) **2)
        ratio = direct_distance / self.speed
        if ratio != 0:
            dx = -x_distance / ratio
            dy = -y_distance / ratio
        else:
            dx =0
            dy = 0
        return dx, dy
    
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
        