import pygame.font
class Scoreboard():
    def __init__(self, game_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        self.text_color = game_settings.hud_color
        self.font = pygame.font.SysFont(None, 48)
        
        self.font2 = pygame.font.SysFont(None, 32) 

        self.prep_score()
    
    def prep_score(self):
        controls_str = "[Move : Arrows] [??? : Space] [Quit : Q]"
        self.controls_image = self.font2.render(controls_str, True, self.text_color)
        self.controls_rect = self.controls_image.get_rect()
        self.controls_rect.right = self.screen_rect.right - 20
        self.controls_rect.top = 20
        
        score_str = "STAGE "+ str(self.stats.stage)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.controls_rect.y + 40

    def show_score(self):
        self.screen.blit(self.controls_image, self.controls_rect)
        self.screen.blit(self.score_image, self.score_rect)