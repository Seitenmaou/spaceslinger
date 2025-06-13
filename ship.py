
import pygame
import math
import game_functions

class Ship():

    def __init__(self, game_settings, screen):
        self.screen = screen
        self.original_image = pygame.image.load('images/SS Player.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.screen_dimention = screen.get_rect()
        self.game_settings = game_settings
        self.rect.centerx = self.screen_dimention.centerx
        self.rect.bottom = self.screen_dimention.centery
        self.counter = self.rect
        
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.angle = 0
        self.current_target = None
        self.laser_cool_down_default = self.game_settings.ship_laser_cool_down
        self.laser_cool_down = self.laser_cool_down_default
        self.energy_max = self.game_settings.ship_hit_points
        self.energy_current = self.energy_max
        self.regen_cool_down_default = game_settings.ship_regen_cool_down
        self.regen_cool_down = self.regen_cool_down_default

        
    def update(self, enemy_in_range, lasers, boss_phase, boss_turn, hyperspeed):
        dx = 0
        dy = 0
        
        if self.moving_right and (self.rect.right <= self.game_settings.screen_width):
            self.counter.centerx += self.game_settings.ship_speed_factor
            if self.rect.right >= (self.game_settings.screen_width - self.game_settings.screen_scroll_threshold) and self.counter.right <= (self.game_settings.map_width_max - self.game_settings.screen_scroll_threshold)  and not boss_phase:
                dx = self.game_settings.ship_speed_factor
            else:
                self.rect.centerx += self.game_settings.ship_speed_factor
            if self.angle > 90 and self.angle < 270:
                self.angle += 1
            elif (self.angle <= 90 and self.angle > 0) or (self.angle < 360 and self.angle > 270):
                self.angle -= 1
            elif self.angle <= 0:
                self.angle = 359

        elif self.moving_left and (self.rect.left >= 0):
            self.counter.centerx -= self.game_settings.ship_speed_factor
            if self.rect.left <= self.game_settings.screen_scroll_threshold and self.counter.left >= self.game_settings.screen_scroll_threshold  and not boss_phase:
                dx = -self.game_settings.ship_speed_factor
            else:
                self.rect.centerx -= self.game_settings.ship_speed_factor
            if (self.angle >= 270 and self.angle < 360) or (self.angle >= 0 and self.angle < 90):
                self.angle += 1
            elif (self.angle < 270 and self.angle > 90):
                self.angle -= 1
            elif self.angle > 359:
                self.angle = 0
                
        if self.moving_up and (self.rect.top >= 0):
            self.counter.centery -= self.game_settings.ship_speed_factor
            if self.rect.top <= self.game_settings.screen_scroll_threshold and self.counter.top >= self.game_settings.screen_scroll_threshold  and not boss_phase:
                dy = -self.game_settings.ship_speed_factor
            else:
                self.rect.centery -= self.game_settings.ship_speed_factor
            if (self.angle >= 180 and self.angle < 359):
                self.angle += 1
            elif (self.angle < 180 and self.angle > 0):
                self.angle -= 1
                
        
        elif self.moving_down and (self.rect.bottom <= self.game_settings.screen_height):
            self.counter.centery += self.game_settings.ship_speed_factor
            if self.rect.bottom >= (self.game_settings.screen_height - self.game_settings.screen_scroll_threshold) and self.counter.bottom <= (self.game_settings.map_height_max - self.game_settings.screen_scroll_threshold)  and not boss_phase:
                dy = self.game_settings.ship_speed_factor
            else:
                self.rect.centery += self.game_settings.ship_speed_factor
            if (self.angle >= 0 and self.angle < 180):
                self.angle += 1
            elif (self.angle < 359 and self.angle > 180):
                self.angle -= 1
        
        if enemy_in_range != -1 and self.laser_cool_down <= 0:
            self.current_target = enemy_in_range
            aimAtEnemy(self)
            if not boss_turn:
                game_functions.shoot_enemy(self.game_settings, self.screen, self, lasers)
            self.laser_cool_down = self.laser_cool_down_default
        else:
            self.laser_cool_down -= 1
            
        if self.energy_current < self.energy_max and self.regen_cool_down <= 0:
            self.energy_current += 1
            self.regen_cool_down = self.regen_cool_down_default
        elif self.energy_current < self.energy_max:
            self.regen_cool_down -= 1
        if hyperspeed < 1:
            self.energy_current -= 1

            
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        return dx, dy
        
    def draw(self):
        self.screen.blit(self.image, self.rect)

def aimAtEnemy(self):
    aim_angle = 0
    
    if (self.rect.y - self.current_target.rect.y) != 0:
        aim_angle = abs(math.degrees(math.atan2((self.rect.centerx - self.current_target.rect.centerx), (self.rect.centery - self.current_target.rect.centery))))
    if (self.rect.centerx - self.current_target.rect.centerx <= 0):
        aim_angle = 360.0 - aim_angle
    self.angle = aim_angle