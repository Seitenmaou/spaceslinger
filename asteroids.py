import pygame
from pygame.sprite import Sprite

class Asteroid(Sprite):
    def __init__(self, game_settings, screen):
        super(Asteroid, self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.original_image = pygame.image.load('images/SS Asteroids.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.angle = 0

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.counterx = float(self.rect.x)
        self.countery = float(self.rect.y)


    def draw(self):
        self.screen.blit(self.image, self.rect)
        
    def update(self, dx, dy, hyperspeed):
        
        dx *= hyperspeed
        dy *= hyperspeed
        
        self.counterx -= dx
        self.x -= dx
        self.rect.x = self.x
        self.countery -= dy
        self.y -= dy
        self.rect.y = self.y
        