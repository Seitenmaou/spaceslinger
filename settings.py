import pygame

class Settings():
    def __init__(self):
        # screen settings
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        self.background_color = (15, 0, 15)
        self.map_scalar = 4
        self.map_width_max = self.screen_width * self.map_scalar
        self.map_height_max = self.screen_height * self.map_scalar
        self.screen_scroll_threshold = 400
    
        # environment settings
        self.asteroids_density = 4
        self.asteroids_amount = self.map_scalar **2 * self.asteroids_density
    
        # hud settings
        self.map_hud_ratio = 4
        self.hud_color = 0, 255, 255
        self.hud_indicator_color = 255, 0, 0
        self.hud_frame_width = 2
        self.hud_width = self.screen_width / self.map_hud_ratio
        self.hud_height = self.screen_height / self.map_hud_ratio
        
        # laser settings
        self.laser_speed_factor = 2
        self.laser_width = 6
        self.laser_height = 6
        self.laser_color = 255, 255, 0
        self.laser_damage = 100
        
        # ship settings
        # 1 or 2 recommended, not 1.5
        self.hyperspeed_multiplier = 0.25
        self.ship_speed_factor = 4.0
        self.ship_laser_cool_down = 50
        self.laser_frequency = 1
        self.laser_lockon_range = int(self.screen_height / 2)
        self.ship_hit_points = 10000
        self.ship_regen_cool_down = 1
        self.burner_trail_length = 1000
        
        # enemy settings
        self.enemy_starting_count = 10
        self.enemy_count_per_difficulty_multiplier = 2
        self.enemy_starting_speed_min = 0.5
        self.enemy_starting_speed_max = 1
        self.enemy_speed_per_difficulty_multiplier = 0.02
        self.enemy_starting_laser_cool_down_min = 500
        self.enemy_starting_laser_cool_down_max = 750
        self.enemy_laser_cool_down_per_difficulty_multiplier = 2
        self.enemy_starting_hit_points = 0.125
        self.enemy_hit_points_per_difficulty_multiplier = 0.0625
        
        # boss settings
        self.boss_starting_hit_points = 5
        self.boss_hit_points_per_difficulty_multiplier = 2
        self.boss_starting_speed_min = 0.015
        self.boss_starting_speed_max = 0.02
        self.boss_speed_per_difficulty_multiplier = 0.005
        self.boss_starting_count = 1
        self.boss_difficulty_increment = 5
        self.boss_starting_laser_cool_down_min = 750
        self.boss_starting_laser_cool_down_max = 1000
        self.boss_laser_cool_down_max_per_difficulty_multiplier = 5
        self.boss_starting_laser_duration_min = 5
        self.boss_starting_laser_duration_max = 10
        self.boss_duration_max_per_difficulty_multiplier = 2