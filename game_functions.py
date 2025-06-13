import sys
import pygame
from laser import Laser
import math
from enemy import Enemy
import random
from boss import Boss
from asteroids import Asteroid

bossPhase = False
difficulty = 0
hyperspeed_active = False
army_health = 0

def check_keydown_events(event, ship):
    global hyperspeed_active
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        hyperspeed_active = True
    elif event.key == pygame.K_q:
        # stats.game_active = False
        sys.exit()
        
    if ship.energy_current <= 100:
        hyperspeed_active = False
def check_keyup_events(event, ship):
    global hyperspeed_active
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_SPACE:
        hyperspeed_active = False
        
def check_events(ship, game_settings, stats, play_button, enemies, bosses):
    global hyperspeed_active
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(enemies, bosses, play_button, mouse_x, mouse_y, stats)

    if hyperspeed_active:
        return game_settings.hyperspeed_multiplier
    else:
        return 1
    
def update(game_settings, screen, ship, enemies, lasers1, lasers2, map, shield, bosses, hyperspeed, play_button, stats, scoreboard, asteroids ):
    global bossPhase, difficulty, army_health
    screen.fill(game_settings.background_color)
    asteroids.draw(screen)
    for laser in lasers1.sprites():
        laser.draw()
    for laser in lasers2.sprites():
        laser.draw()
    ship.draw()
    enemies.draw(screen)
    if len(enemies) <= 0 and not bossPhase:
        army_health = generate_boss(game_settings, screen, bosses, ship)
        bossPhase = True
    if bossPhase:
        bosses.draw(screen)
    if len(bosses) <= 0 and bossPhase:
        bossPhase = False
        difficulty += 1
        reset_level(map, ship, enemies, lasers1, lasers2, hyperspeed, scoreboard)
        army_health = generate_enemies(game_settings, screen, enemies, ship, difficulty)
        generate_asteroids(game_settings, screen, asteroids)
    map.draw(ship, enemies, hyperspeed)
    shield.draw(ship, enemies, bosses, army_health)
    stats.stage = difficulty
    scoreboard.stats = stats
    scoreboard.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()
    return bossPhase, difficulty
    
def update_lasers(game_settings, ship, enemies, lasers1, lasers2, dx, dy, asteroids, bosses, hyperspeed, stats):
        lasers1.update(dx, dy, hyperspeed)
        lasers2.update(dx, dy, hyperspeed)
        shot_asteroid(lasers1, lasers2, asteroids)
        enemy_shot(enemies, lasers1)
        ship_shot(game_settings, ship, lasers2, stats)
        boss_shot(bosses, lasers1)
        for laser in lasers1.copy(): 
            if laser.rect.bottom <= 0:
                lasers1.remove(laser)
            elif laser.rect.right <= 0:
                lasers1.remove(laser)
            if laser.rect.top >= game_settings.screen_height:
                lasers1.remove(laser)
            elif laser.rect.left >= game_settings.screen_width:
                lasers1.remove(laser)
        for laser in lasers2.copy(): 
            if laser.rect.bottom <= 0:
                lasers2.remove(laser)
            elif laser.rect.right <= 0:
                lasers2.remove(laser)
            if laser.rect.top >= game_settings.screen_height:
                lasers2.remove(laser)
            elif laser.rect.left >= game_settings.screen_width:
                lasers2.remove(laser)
                
def shoot_enemy(game_settings, screen, ship, lasers):
    new_laser = Laser(game_settings, screen, ship)
    lasers.add(new_laser)
    
def shoot_player(game_settings, screen, enemy, lasers):
    new_laser = Laser(game_settings, screen, enemy)
    lasers.add(new_laser)
    
def shoot_boss_laser(game_settings, screen, boss_cannon, lasers):
    new_laser = Laser(game_settings, screen, boss_cannon)
    lasers.add(new_laser)

def generate_enemies(game_settings, screen, enemies, ship, difficulty):
    number_enemies = game_settings.enemy_starting_count + game_settings.enemy_count_per_difficulty_multiplier * difficulty
    enemy_speed_min = game_settings.enemy_starting_speed_min
    enemy_speed_max = game_settings.enemy_starting_speed_max + game_settings.enemy_speed_per_difficulty_multiplier * difficulty
    enemy_laser_cool_down_min = game_settings.enemy_starting_laser_cool_down_min - game_settings.enemy_laser_cool_down_per_difficulty_multiplier * difficulty
    enemy_laser_cool_down_max = game_settings.enemy_starting_laser_cool_down_max
    enemy_hit_points = game_settings.enemy_starting_hit_points + game_settings.enemy_hit_points_per_difficulty_multiplier * difficulty
    
    for _ in range(number_enemies):
        new_enemy = Enemy(game_settings, screen, ship)
        new_enemy.x = random.randint(100, game_settings.map_width_max-100)
        new_enemy.y = random.randint(100, game_settings.map_height_max-100)
        new_enemy.rect.x = new_enemy.x
        new_enemy.rect.y = new_enemy.y
        new_enemy.counterx = float(new_enemy.rect.x)
        new_enemy.countery = float(new_enemy.rect.y)
        new_enemy.speed = round(random.uniform(enemy_speed_min, enemy_speed_max), 2)
        new_enemy.laser_cool_down_default = round(random.uniform(enemy_laser_cool_down_min, enemy_laser_cool_down_max), 2)
        new_enemy.hit_points = enemy_hit_points
        enemies.add(new_enemy)
        
    return calculate_army_health(enemies)
        
def generate_boss(game_settings, screen, bosses, ship):
    number_bosses = int(game_settings.boss_starting_count + int(difficulty / game_settings.boss_difficulty_increment))
    boss_speed_min = game_settings.boss_starting_speed_min
    boss_speed_max = game_settings.boss_starting_speed_max + game_settings.boss_speed_per_difficulty_multiplier * difficulty
    boss_laser_cool_down_min = game_settings.boss_starting_laser_cool_down_min - game_settings.boss_laser_cool_down_max_per_difficulty_multiplier * difficulty
    boss_laser_cool_down_max = game_settings.boss_starting_laser_cool_down_max
    boss_hit_points = game_settings.boss_starting_hit_points + game_settings.boss_hit_points_per_difficulty_multiplier * difficulty
    boss_laser_duration_min = game_settings.boss_starting_laser_duration_min + game_settings.boss_duration_max_per_difficulty_multiplier * difficulty
    boss_laser_duration_max = game_settings.boss_starting_laser_duration_max + game_settings.boss_duration_max_per_difficulty_multiplier * difficulty
    
    for _ in range(number_bosses):
        new_boss = Boss(game_settings, screen, ship)
        new_boss.x = random.randint(100, game_settings.map_width_max-100)
        new_boss.y = random.randint(100, game_settings.map_height_max-100)
        new_boss.rect.x = new_boss.x
        new_boss.rect.y = new_boss.y
        new_boss.counterx = float(new_boss.rect.x)
        new_boss.countery = float(new_boss.rect.y)
        new_boss.movement_angle = random.randint(0, 359)
        new_boss.movement_angle_speed = round(random.uniform(boss_speed_min, boss_speed_max), 3)
        new_boss.laser_cool_down = round(random.uniform(boss_laser_cool_down_min, boss_laser_cool_down_max), 2)
        new_boss.hit_points = boss_hit_points
        new_boss.laser_duration= round(random.uniform(boss_laser_duration_min, boss_laser_duration_max), 2)
        new_boss.move_direction = random.choice([-1, 1])
        bosses.add(new_boss)
    return calculate_army_health(bosses)

def update_enemies(enemies, dx, dy, ship, lasers, hyperspeed):
    enemies.update(dx, dy, ship, lasers, hyperspeed)
    
def update_map(map, dx, dy):
    map.update(dx,dy)
    
def update_asteroids(asteroids, dx, dy, hyperspeed):
    asteroids.update(dx,dy, hyperspeed) 
    

def scanEnemy(ship, enemies, game_settings, bosses):
    returnValue = -1
    if len(enemies) > 0:
        closest = enemies.sprites()[0]
        search_range = game_settings.laser_lockon_range
        for enemy in enemies:
            enemy_distance = math.sqrt(((ship.rect.centerx - enemy.rect.centerx) ** 2) + ((ship.rect.centery - enemy.rect.centery) ** 2))
            if (enemy_distance <  math.sqrt(((ship.rect.centerx - closest.rect.centerx) ** 2) + ((ship.rect.centery - closest.rect.centery) ** 2))):
                closest = enemy
        
        if (math.sqrt(((ship.rect.centerx - closest.rect.centerx) ** 2) + ((ship.rect.centery - closest.rect.centery) ** 2)) <= search_range):
            returnValue = closest
    if len(bosses) > 0:
        closest = bosses.sprites()[0]
        search_range = game_settings.laser_lockon_range
        for enemy in bosses:
            enemy_distance = math.sqrt(((ship.rect.centerx - enemy.rect.centerx) ** 2) + ((ship.rect.centery - enemy.rect.centery) ** 2))
            if (enemy_distance <  math.sqrt(((ship.rect.centerx - closest.rect.centerx) ** 2) + ((ship.rect.centery - closest.rect.centery) ** 2))):
                closest = enemy
        if (math.sqrt(((ship.rect.centerx - closest.rect.centerx) ** 2) + ((ship.rect.centery - closest.rect.centery) ** 2)) <= search_range):
                returnValue = closest
    return returnValue
            

def enemy_shot(enemies, lasers):
    for enemy in enemies:
        collision = pygame.sprite.spritecollideany(enemy, lasers)
        if collision:
            collision.kill()
            enemy.hit_points -= 1
            if enemy.hit_points <= 0:
                enemy.kill()

        
def boss_shot(enemies, lasers):
    for enemy in enemies:
        collision = pygame.sprite.spritecollideany(enemy, lasers)
        if collision:
            collision.kill()
            enemy.hit_points -= 1
            if enemy.hit_points <= 0:
                enemy.kill()
        
def ship_shot(game_settings, ship, lasers, stats):
    collision = pygame.sprite.spritecollideany(ship, lasers)
    if collision:
        collision.kill()
        ship.energy_current -= game_settings.laser_damage
        if ship.energy_current <= 0:
            stats.game_active = False
            pygame.mouse.set_visible(True)
        
def shot_asteroid(lasers1, lasers2, asteroids):
    collision1 = pygame.sprite.groupcollide(lasers1, asteroids, True, False)
    collision2 = pygame.sprite.groupcollide(lasers2, asteroids, True, False)
        
def reset_level(map, ship, enemies, lasers1, lasers2, hyperspeed, scoreboard):
    lasers1.empty()
    lasers2.empty()
    map.x = 0
    map.y = 0
    ship.rect.centerx = ship.screen_dimention.centerx
    ship.rect.bottom = ship.screen_dimention.centery
    ship.counter = ship.rect
    map.draw(ship, enemies, hyperspeed)
    scoreboard.prep_score()
    
def check_play_button(enemies, bosses,play_button, mouse_x, mouse_y, stats):
    global difficulty, bossPhase
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        enemies.empty()
        bosses.empty()
        bossPhase = True
        difficulty = 0

def generate_asteroids(game_settings, screen, asteroids):
    number_asteroids = game_settings.asteroids_amount
    
    for _ in range(number_asteroids):
        new_asteroid = Asteroid(game_settings, screen)
        new_asteroid.x = random.randint(100, game_settings.map_width_max-100)
        new_asteroid.y = random.randint(100, game_settings.map_height_max-100)
        new_asteroid.rect.x = new_asteroid.x
        new_asteroid.rect.y = new_asteroid.y
        new_asteroid.counterx = float(new_asteroid.rect.x)
        new_asteroid.countery = float(new_asteroid.rect.y)
        
        asteroids.add(new_asteroid)
        
def calculate_army_health(enemies):
    total = 0
    if len(enemies) > 0:
        for enemy in enemies:
            total += enemy.hit_points
    return total