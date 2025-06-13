import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions
from hud_map import Map
from energy import Shield
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def game():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Splace Slinger")

    
    ship = Ship(game_settings, screen)
    map = Map(game_settings, screen)
    shield = Shield(game_settings, screen, ship)
    
    ship_lasers = Group()
    enemy_lasers = Group()
    enemies = Group()
    bosses = Group()
    asteroids = Group()
    
    stats = GameStats(game_settings)
    
    army_health = game_functions.generate_enemies(game_settings, screen, enemies, ship, 0)
    game_functions.generate_asteroids(game_settings, screen, asteroids)
    
    boss_phase = False
    boss_turn = False
    
    play_button = Button(game_settings, screen, "Play")
    scoreboard = Scoreboard(game_settings, screen, stats)
    hyperspeed = 1
    
    # pygame.mixer.music.load('Audio/ss music.wav')
    # pygame.mixer.music.play(-1)
    
    game_running = True
    while game_running:
        hyperspeed = game_functions.check_events(ship, game_settings, stats, play_button, enemies, bosses)
        if stats.game_active:
            enemy_in_range = game_functions.scanEnemy(ship, enemies, game_settings, bosses)
            dx, dy = ship.update(enemy_in_range, ship_lasers, boss_phase, boss_turn, hyperspeed)
            game_functions.update_lasers(game_settings, ship, enemies, ship_lasers, enemy_lasers, dx, dy, asteroids, bosses, hyperspeed, stats)
            game_functions.update_enemies(enemies, dx, dy, ship, enemy_lasers, hyperspeed)
            game_functions.update_asteroids(asteroids, dx, dy, hyperspeed)
            if boss_phase:
                    boss_turn = bosses.update(ship, enemy_lasers, boss_turn, hyperspeed)
            game_functions.update_map(map, dx, dy)
        boss_phase, difficulty = game_functions.update(game_settings, screen, ship, enemies, ship_lasers, enemy_lasers, map, shield, bosses, hyperspeed, play_button, stats, scoreboard, asteroids)

game()

# want to add mega beams instead of laser for boss
# want to add trails / afterburners (maybe sprites that follow sprites that follow sprites that...)
# want to add asteroids collision with ship and enemies (not bosses because static movement)
# maybe enemy dodge or warp?
# alot of clean up for the code...