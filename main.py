import pygame
import random
import os
import time
import sys
import math

from laser import Laser
from final_boss import FinalBoss
from repair import Repair, REP_HEIGHT
from medic import Medic, HEALTH_HEIGHT
from submarine import Submarine, SUBMARINE_HEIGHT
from missile import Missile
from battleship import Battleship, BATTLE_ANGLE
from rockets import Rockets
from patrol import Patrol, Patrol_angle
from my_ship import My_Ship, MY_HEIGHT
from jet import Jet


pygame.font.init()

#WIN means WINDOW
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PROJECT MAYHEM")

#WATER BACKGROUND
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'water1.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (1200, 800))

#PAGE SETUP
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (77, 144, 195)
RED = (255, 0, 0)
FONT = pygame.font.SysFont('comicsans', 30)
title_text = FONT.render(f'Welcome to BattleShip', 1, 'white')
# MOWER_HIT = pygame.USEREVENT +1
FPS = 60

#VELOCITY
VEL = 12
JET_VEL = 5
SUB_VEL = 11
BATTLE_VEL = 1
MISS_VEL = 10
BULLET_VEL = 20
MEDIC_VEL = 4
REP_VEL = 4
BOSS_VEL = 1
LAS_VEL = 30
PAT_VEL = 1
ROCKET_VEL = 25
MAX_BULLETS = 500

#Start times
MEDIC_DELAY_START = 15
REP_DELAY_START = 25
SUB_DELAY_START = 8
BATTLE_DELAY_START = 55
PATROL_DELAY_START = 25
BOSS_DELAY_START = 90


#Bullet Dimensions
BUL_WIDTH, BUL_HEIGHT = 20, 10

#Explosion Dimensions
EXPLODE_WIDTH, EXPLODE_HEIGHT = 58, 58
EXPLODE_WIDTH_2, EXPLODE_HEIGHT_2 = 100, 100


# Object Images
JET_IMAGE = pygame.image.load(os.path.join('Assets', 'jet.png'))
submarine_image = pygame.image.load(os.path.join('Assets', 'submarine.png'))
missile_image = pygame.image.load(os.path.join('Assets', 'missile.png'))
battleship_image = pygame.image.load(os.path.join('Assets', 'battleship.png'))
my_ship_image = pygame.image.load(os.path.join('Assets', 'ship.png'))
missile_image = pygame.image.load(os.path.join('Assets', 'missile.png'))
explosion_image = pygame.image.load(os.path.join('Assets', 'explosion.png'))
explosion_image_2 = pygame.image.load(os.path.join('Assets', 'explosion2.png'))
explosion_image_3 = pygame.image.load(os.path.join ('Assets', 'explode3.png'))
boss_explosion = pygame.image.load(os.path.join ('Assets', 'bigexplosion.png'))
big_explosion = pygame.image.load(os.path.join ('Assets', 'bigexplode.png'))
final_boss = pygame.image.load(os.path.join ('Assets', 'finalboss.png'))
laser_image = pygame.image.load(os.path.join ('Assets', 'laser.png'))
medic_health = pygame.image.load(os.path.join ('Assets', 'medic.png'))
repair_image = pygame.image.load(os.path.join ('Assets', 'heart.png'))
beach = pygame.image.load(os.path.join ('Assets', 'beach2.png'))
city = pygame.image.load(os.path.join ('Assets', 'city.png'))
city1 = pygame.transform.scale(city, (500, 900))
patrol = pygame.image.load(os.path.join ('Assets', 'patrol.png'))
rocket_image = pygame.image.load(os.path.join ('Assets', 'rocket2.png'))
bullet_img = pygame.image.load(os.path.join ('Assets', 'bullet1.png'))



# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y, speed) -> None:
#         super().__init__()
#         self.image = pygame.transform.scale(bullet_img, (BUL_WIDTH, BUL_HEIGHT))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.speed = speed

#     def move(self):
#         self.rect.x += self.speed


# EXPLOSIONS
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center) -> None:
        super().__init__()
        self.image = pygame.transform.scale(explosion_image, (EXPLODE_WIDTH, EXPLODE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.creation_time = time.time()

class Explosion2(pygame.sprite.Sprite):
    def __init__(self, center) -> None:
        super().__init__()
        self.image = pygame.transform.scale(explosion_image_2, (EXPLODE_WIDTH + 50, EXPLODE_HEIGHT + 50))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.creation_time = time.time()

class Explosion3(pygame.sprite.Sprite):
    def __init__(self, center) -> None:
        super().__init__()
        self.image = pygame.transform.scale(explosion_image_3, (EXPLODE_WIDTH_2, EXPLODE_HEIGHT_2))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.creation_time = time.time()


#DRAW WINDOW
def draw_window( my_ship, bullets, elapsed_time, jets, battleship, patrol, rocket, missile, submarines, hits, explosions, medics, final_boss, laser, repairs):
    LIVES = 3
    LIVES -= hits

    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(beach, (-270, 0) )
    WIN.blit(city1, (-490, 0))

    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white')
    WIN.blit(time_text, (550, 10))

    lives_label = FONT.render(f"Base Lives: {LIVES}", 1, 'white')
    WIN.blit(lives_label, (10, 10))

    WIN.blit(my_ship.image, my_ship.rect)
    my_ship.healthbar(WIN)


    if battleship is not None and battleship.hits > 0:
        WIN.blit(battleship.image, battleship.rect)
        for missile in battleship.missiles:
            WIN.blit(missile.image, missile.rect)
            missile.move()

    if patrol is not None and patrol.hits > 0:
        WIN.blit(patrol.image, patrol.rect)
        for rocket in patrol.rockets:
            WIN.blit(rocket.image, rocket.rect)
            rocket.move()
            
    for submarine in submarines:
        WIN.blit(submarine.image, submarine.rect)

    for medic in medics:
        WIN.blit(medic.image, medic.rect)

    for repair in repairs:
        WIN.blit(repair.image, repair.rect)

    if final_boss is not None and final_boss.hits > 0:
        WIN.blit(final_boss.image, final_boss.rect)
        final_boss.healthbar(WIN)
        for laser in final_boss.lasers:
            WIN.blit(laser.image, laser.rect)
            laser.move()

    for jet in jets:
        WIN.blit(jet.image, jet.rect)

    for bullet in bullets:
        # WIN.blit(bullet.image, bullet.rect)
        pygame.draw.rect(WIN, RED, bullet)

    for explosion in explosions:
        WIN.blit(explosion.image, explosion.rect)

    pygame.display.update()


# KEYS FOR SHIP
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and my_ship.rect.x - VEL >=0: #left
        my_ship.rect.x -= VEL 
    if keys[pygame.K_d]: #right
        my_ship.rect.x += VEL
    if keys[pygame.K_w] and my_ship.rect.y - VEL >= -10: #up
        my_ship.rect.y -= VEL
    if keys[pygame.K_s] and my_ship.rect.y + VEL <= 780: #down
        my_ship.rect.y += VEL


# HANDLE BULLETS
def handle_bullets(bullets, jets, battleship, patrol, submarines, explosions, final_boss):
    bullets_to_remove = []
    explosions_to_remove = []

    for bullet in bullets:
        bullet.x += BULLET_VEL

        if not battleship.destroyed and bullet.colliderect(battleship.rect):
            battleship.hits -= 1
            if battleship.hits == 0:
                battleship.destroyed = True
            else:
                explosion = Explosion(battleship.rect.center)
                explosions.add(explosion)
                bullets_to_remove.append(bullet)

        if not patrol.destroyed and bullet.colliderect(patrol.rect):
            patrol.hits -= 1
            if patrol.hits == 0:
                patrol.destroyed = True
            else:
                explosion = Explosion(patrol.rect.center)
                explosions.add(explosion)
                bullets_to_remove.append(bullet)

        if not final_boss.destroyed and bullet.colliderect(final_boss.rect):
            final_boss.hits -= 1
            final_boss.health -= 1
            if final_boss.hits == 0:
                final_boss.destroyed = True
            else:
                explosion = Explosion(final_boss.rect.center)
                explosions.add(explosion)
                bullets_to_remove.append(bullet)

        for submarine in submarines[:]:
            if bullet.colliderect(submarine.rect):
                submarine.hits -= 1
                bullets_to_remove.append(bullet)

                if submarine.hits <= 0:
                    explosion = Explosion(submarine.rect.center)
                    explosions.add(explosion)
                    submarines.remove(submarine)

    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
                    
    for jet in jets[:]:
        for bullet in bullets[:]:
            if bullet.colliderect(jet.rect):
                jets.remove(jet)
                bullets_to_remove.append(bullet)
                explosion = Explosion(jet.rect.center)
                explosions.add(explosion)
                break

    for explosion in explosions:
        if time.time() - explosion.creation_time >= 1:
            explosions_to_remove.append(explosion)

    for explosion in explosions_to_remove:
        explosions.remove(explosion)

# TITLE SCREEN
def draw_title_screen():
    WIN.fill((0, 0, 0))
    title_text = FONT.render('Welcome to BattleShip', 1, 'white')
    subtitle_text = FONT.render('Use "W, A, S, D" to control your battleship, press spacebar to shoot.', 1, 'red')
    subtitle_text2 = FONT.render('Protect your beach base from enemy fighter jets.', 1, 'white')
    subtitle_text3 = FONT.render('Missiles and lasers will damage your Battleship, but not your base.', 1, 'white')
    subtitle_text4 = FONT.render('Press Return key to begin... Good luck.', 1, 'white')
    subtitle_text5 = FONT.render('Medpacks (green) heal your ship and Hearts (red) add 1 life.', 1, 'white')
    WIN.blit(title_text, (WIDTH // 2- title_text.get_width() // 2, 150))
    WIN.blit(subtitle_text, (WIDTH // 6 - title_text.get_width() // 2, 490))
    WIN.blit(subtitle_text2, (WIDTH // 6 - title_text.get_width() // 2, 300))
    WIN.blit(subtitle_text3, (WIDTH // 6 - title_text.get_width() // 2, 350))
    WIN.blit(subtitle_text4, (WIDTH // 2.5 - title_text.get_width() // 2, 600))
    WIN.blit(subtitle_text5, (WIDTH // 6 - title_text.get_width() // 2, 400))
    pygame.display.update()



# MAIN    
def main():
    run = True
    clock = pygame.time.Clock()
    start_time = 0
    Title_screen = True

# OBJECTS
    my_ship = My_Ship(100, 400, VEL)
    final_boss = FinalBoss(1300, 400, BOSS_VEL)
    laser = Laser(1300, 400, LAS_VEL, -20, 20)
    battleship = Battleship(1200 , -200, BATTLE_VEL, BATTLE_ANGLE)
    patrol = Patrol(1300, 850, PAT_VEL, Patrol_angle)
    missile = Missile(1200, -200, 10, -35, 5)
    rocket = Rockets(800, 800, ROCKET_VEL, -1, 1)
    # bullet = Bullet(100, 400, BULLET_VEL)
    explosions = pygame.sprite.Group() 

# Incrementing & Lists
    jet_add_increment = 1100
    jet_count = 0
    jets = []
    bullets = []
    shooting = False
    submarines = []
    medics = []
    repairs = []
    missiles = []
    patrols = []
    hits = 0

    patrol_hit = 0

# RUNNING GAME
    while run:
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    Title_screen = False
                    start_time = time.time()

                if event.key == pygame.K_SPACE and not shooting:
                    bullet = pygame.Rect(
                        my_ship.rect.x + 70, my_ship.rect.y + MY_HEIGHT//9, 10, 5)
                    bullets.append(bullet)
                    shooting = True 

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shooting = False

        keys = pygame.key.get_pressed()

# Title Screen
        if Title_screen:
            elapsed_time = 0
            draw_title_screen()
            pygame.display.update()
            continue
            
        else:
            jet_count += clock.tick(FPS)
            elapsed_time = time.time() - start_time

# MEDIC MOVEMENT
        if elapsed_time >= MEDIC_DELAY_START:
            if random.randint(0, 600) < 1:  
                medic_y = random.randint(0, HEIGHT - HEALTH_HEIGHT)
                medic = Medic(WIDTH, medic_y, MEDIC_VEL)
                medics.append(medic)

            for medic in medics[:]:
                medic.move()
                if pygame.sprite.collide_rect(medic, my_ship):
                    medics.remove(medic)
                    my_ship.health = my_ship.max_health
                    break

# REPAIR MOVEMENT
        if elapsed_time >= REP_DELAY_START:
            if random.randint(0, 900) < 1:  
                repair_y = random.randint(0, HEIGHT - REP_HEIGHT)
                repair = Repair(WIDTH, repair_y, MEDIC_VEL)
                repairs.append(repair)

            for repair in repairs[:]:
                repair.move()
                if pygame.sprite.collide_rect(repair, my_ship):
                    hits -= 1
                    repairs.remove(repair)
                    break
# PATROL MOVEMENT
        if patrol.rect.x < WIDTH - 1260:
            patrol_hit += 1
            patrol.kill()
            if patrol_hit == 1 and patrol.hits > 0:
                hits += 1
                explosion = Explosion3(patrol.rect.center)
                explosions.add(explosion) 

# ROCKETS MOVEMENT
                
        for rocket in patrol.rockets[:]:
            if pygame.sprite.collide_rect(rocket, my_ship):
                patrol.rockets.remove(rocket)
                explosion = Explosion(my_ship.rect.center)
                explosions.add(explosion)
                my_ship.health -= 2
                break

# LASERS MOVEMENT
                
        for laser in final_boss.lasers[:]:
            if pygame.sprite.collide_rect(laser, my_ship):
                final_boss.lasers.remove(laser)
                explosion = Explosion2(my_ship.rect.center)
                explosions.add(explosion)
                my_ship.health -= 10
                break

# MISSILES MOVEMENT
        for missile in battleship.missiles[:]:
            if pygame.sprite.collide_rect(missile, my_ship):
                battleship.missiles.remove(missile)
                explosion = Explosion2(my_ship.rect.center)
                explosions.add(explosion)
                my_ship.health -= 20
                break
        
# SUBMARINES MOVEMENT
        for submarine in submarines[:]:
            submarine.move()
            if pygame.sprite.collide_rect(submarine, my_ship):
                submarines.remove(submarine)
                explosion = Explosion2(my_ship.rect.center)
                explosions.add(explosion)
                my_ship.health -= 20
                break

        if elapsed_time >= SUB_DELAY_START and elapsed_time < BOSS_DELAY_START:
            if random.randint(0, 90) < 2:  
                submarine_y = random.randint(0, HEIGHT - SUBMARINE_HEIGHT)
                submarine = Submarine(WIDTH, submarine_y, SUB_VEL)
                submarines.append(submarine)

# JETS MOVEMENT
        for jet in jets[:]:
            jet.move()
            if jet.rect.x < WIDTH - 1270:
                hits +=1
                jets.remove(jet)
                explosion = Explosion3(jet.rect.center)
                explosions.add(explosion) 
            elif pygame.sprite.collide_rect(jet, my_ship):
                my_ship.health -= 20
                explosion = Explosion2(my_ship.rect.center)
                explosions.add(explosion)
                jets.remove(jet)
                break

        if hits >= 3 or my_ship.health <= 0:
            lost_text = FONT.render('You lost!', 1, 'white')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        if jet_count > jet_add_increment:
            for _ in range(1):
                jet_y = random.randint(0, 700)
                jet = Jet(WIDTH, jet_y, JET_VEL)
                jets.append(jet)
            
            jet_add_increment = max(200, jet_add_increment -50)
            jet_count = 0
        elif elapsed_time >= BOSS_DELAY_START:
            jet_add_increment = 60000



# DELAY START
        if elapsed_time >= BOSS_DELAY_START:
            if final_boss.destroyed == False:
                final_boss.move()
                laser.move

        if elapsed_time >= PATROL_DELAY_START:
            if patrol.destroyed == False:
                patrol.move()
                rocket.move()

        if elapsed_time >= BATTLE_DELAY_START:
            if battleship.destroyed == False:
                battleship.move()
                missile.move()

# HANDLE FUNCTIONS
        handle_bullets(bullets, jets, battleship, patrol, submarines, explosions, final_boss)
        draw_window(my_ship, bullets, elapsed_time, jets, battleship, patrol, rocket, missile, submarines, hits, explosions, medics, final_boss, laser, repairs)

    pygame.quit()


if __name__ == "__main__":
    main()