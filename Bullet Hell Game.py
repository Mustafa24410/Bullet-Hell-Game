import pygame #Modules
from math import*
import sys
import os
import DATA.SCRIPTS.player as player
import DATA.SCRIPTS.expanding_enemy as exp_enemy

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

#Color Constants
BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
RED = (240, 70, 70)
YELLOW = (237, 229, 119)

pygame.init() #Initaization and clock and game loop condition
clock = pygame.time.Clock()
run = True

#Screen
size = (700, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Bullet Hell Game')
h = screen.get_height()
w = screen.get_width()

player.init(screen)
exp_enemy.init(screen)

player = player.Player(50, 300)

boundry_box = pygame.Rect(0, 100, w, 700)
do_score = True
lev3_alt = True
score = 0
shoot_once = True
level = 1
deaths = 0
level_text = [
    'Get to a hundred',
    'Looks like you got an admirer',
    'Cranking 90\'s',
    'Sinefield',
    'Gotta go fast',
    'Home coming',
    'Newton\'s 3rd Law: Stuff can bounce',
    'You spin me right round baby right round',
    'Lilypads in a pond']

enemy = exp_enemy.ExpandingEnemy(boundry_box.centerx, boundry_box.centery)
enemy_atk_rate = 2000
enemy_atk_next = 700

font1 = pygame.font.SysFont('ptmono', 25)
font2 = pygame.font.SysFont('ptmono', 27)
font3 = pygame.font.SysFont('ptmono', 32)

def draw_text(text, font, pos, color):
    text = font.render(text, False, color)
    rect = text.get_rect()
    rect.center = pos
    screen.blit(text, rect)

def reset():
    global score, enemy_atk_next, shoot_once
    score = 0
    shoot_once = True
    enemy_atk_next = current_time+700
    player.rect.topleft = [50, 300]
    enemy.bullet_rects = []
    enemy.time_delta = current_time
    enemy.parent_rect.center = [boundry_box.centerx, boundry_box.centery]

def bullet_shoot():
    global enemy_atk_next, enemy_atk_rate
    current_time = pygame.time.get_ticks()
    if enemy_atk_next <= current_time:
        enemy.bullet_attack()
        enemy_atk_next = current_time+enemy_atk_rate

def bullet_shoot_once():
    global enemy_atk_next, enemy_atk_rate, shoot_once
    current_time = pygame.time.get_ticks()
    if enemy_atk_next <= current_time and shoot_once:
        enemy.bullet_attack()
        shoot_once = False
        enemy.time_delta = current_time
        enemy_atk_next = current_time+enemy_atk_rate

def bullet_shoot_alternate():
    global enemy_atk_next, enemy_atk_rate, lev3_alt
    current_time = pygame.time.get_ticks()
    if enemy_atk_next <= current_time:
        if lev3_alt:
            enemy.bullet_attack_cardinal()
        else:
            enemy.bullet_attack_ordinal()
        lev3_alt = not lev3_alt
        enemy_atk_next = current_time+enemy_atk_rate

while run: #Game loop
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get(): #Event loop
        if event.type == pygame.QUIT:
            run = False
    
    if enemy.bullet_collide(player.rect):
        deaths += 1
        reset()
    if score >= 100:
        level += 1
        reset()

    player.move_vect = pygame.math.Vector2([0, 0])
    if level != 10:
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_vect.x += player.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_vect.x -= player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move_vect.y += player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move_vect.y -= player.speed
        player.rect.topleft += player.move_vect

    if player.rect.left <= boundry_box.left+5:
        player.rect.left = boundry_box.left+5
    if player.rect.right >= boundry_box.right-5:
        player.rect.right = boundry_box.right-5
    if player.rect.top <= boundry_box.top+5:
        player.rect.top = boundry_box.top+5
    if player.rect.bottom >= boundry_box.bottom-5:
        player.rect.bottom = boundry_box.bottom-5

    if level == 1:
        enemy_atk_rate = 2000
        enemy.bullet_speed = 4
        enemy.bullet_move()
        bullet_shoot()
    elif level == 2:
        enemy_atk_rate = 2000
        enemy.bullet_speed = 4
        enemy.follow_rect(player.rect)
        enemy.bullet_move()
        bullet_shoot()
    elif level == 3:
        enemy_atk_rate = 1000
        enemy.bullet_speed = 4
        enemy.bullet_move()
        bullet_shoot_alternate()
    elif level == 4:
        enemy_atk_rate = 0
        enemy.bullet_speed = 3
        enemy.sine_wave(80, 500, enemy.parent_rect.centerx, enemy.parent_rect.centery)
        bullet_shoot_once()
    elif level == 5:
        enemy_atk_rate = 1000
        enemy.bullet_speed = 8
        enemy.bullet_move()
        bullet_shoot()
    elif level == 6:
        enemy_atk_rate = 2000
        enemy.bullet_speed = 4
        enemy.bullet_move()
        enemy.homing_turn(player.rect)
        bullet_shoot()
    elif level == 7:
        enemy_atk_rate = 0
        enemy.bullet_speed = 6
        enemy.bullet_move()
        enemy.bullet_bounce(boundry_box.left, boundry_box.right, boundry_box.top, boundry_box.bottom)
        bullet_shoot_once()
    elif level == 8:
        enemy_atk_rate = 2000
        enemy.bullet_speed = 2
        enemy.circle_motion(1)
        bullet_shoot()
    elif level == 9:
        enemy_atk_rate = 0
        enemy.bullet_speed = 250
        enemy.sine_circle(1, 800)
        bullet_shoot_once()
    
    if player.rect.colliderect(enemy.parent_rect) and do_score:
        do_score = False
        score += 5
    elif not player.rect.colliderect(enemy.parent_rect):
        do_score = True

    screen.fill(BLACK)
    if level != 10:
        player.draw(RED)
        enemy.draw(YELLOW, WHITE)
        pygame.draw.rect(screen, WHITE, boundry_box, 5)
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, w, 100))
        draw_text(str(score), font1, enemy.parent_rect.center, BLACK)
        draw_text(level_text[level-1], font2, [w/2, 60], WHITE)
        draw_text('Level '+str(level), font3, [w/2, 25], WHITE)
    else:
        draw_text('YOU WIN', font3, [w/2, h/2], WHITE)
        draw_text('\^o^/', font2, [w/2, h/2+30], WHITE)
        draw_text('You died '+str(deaths)+' times', font3, [w/2, h/2+60], WHITE)

    enemy.update(boundry_box)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()