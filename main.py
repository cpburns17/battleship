import pygame
import random
import os
import time
import sys
import math


pygame.font.init()

#WIN means WINDOW
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PROJECT MAYHEM")

#WATER BACKGROUND
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'water1.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (1200, 800))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (77, 144, 195)
RED = (255, 0, 0)
FONT = pygame.font.SysFont('comicsans', 30)
title_text = FONT.render(f'Welcome to BattleShip', 1, 'white')
MOWER_HIT = pygame.USEREVENT +1
FPS = 60

#Velocity 
VEL = 12
JET_VEL = 5
SUB_VEL = 11
BATTLE_VEL = 1
MISS_VEL = 10
BULLET_VEL = 20
MEDIC_VEL = 6
REP_VEL = 6
BOSS_VEL = 1
LAS_VEL = 30
PAT_VEL = 1
ROCKET_VEL = 25
MAX_BULLETS = 500

#Start times
MEDIC_DELAY_START = 20
REP_DELAY_START = 25
SUB_DELAY_START = 8
BATTLE_DELAY_START = 55
PATROL_DELAY_START = 5
BOSS_DELAY_START = 80

#My Ship Dimensions
MY_WIDTH, MY_HEIGHT = 25, 120

#Final Boss Dimensions
BOSS_WIDTH, BOSS_HEIGHT = 400, 200

#Laser Dimensions
LASER_WIDTH, LASER_HEIGHT = 70, 20

#Explosion Dimensions
EXPLODE_WIDTH, EXPLODE_HEIGHT = 58, 58
EXPLODE_WIDTH_2, EXPLODE_HEIGHT_2 = 100, 100

#Health Dimensions
HEALTH_WIDTH, HEALTH_HEIGHT = 50, 50

#Repair Dimensions
REP_WIDTH, REP_HEIGHT = 35, 35

#Jet Dimensions
JET_WIDTH, JET_HEIGHT = 10, 30

#Patrol Dimensions
PATROL_WIDTH, PATROL_HEIGHT = 170, 30
Patrol_angle = 45

#Rocket Dimensions
ROCK_WIDTH, ROCK_HEIGHT = 13, 5

# #Battleship Dimensions
BATTLESHIP_WIDTH, BATTLESHIP_HEIGHT = 240, 40
BATTLE_ANGLE = -35
BATTLE_ANGLE_2 = 45

# Missle Dimensions
MISSLE_WIDTH, MISSLE_HEIGHT = 100, 100

# Subarine Dimensions
SUBMARINE_WIDTH, SUBMARINE_HEIGHT = 35, 15

#JET 
JET_IMAGE = pygame.image.load(os.path.join('Assets', 'jet.png'))
JET = pygame.transform.scale(JET_IMAGE, (150, 150))

# Object Images
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
repair_image = pygame.image.load(os.path.join ('Assets', 'repair.png'))
beach = pygame.image.load(os.path.join ('Assets', 'beach2.png'))
city = pygame.image.load(os.path.join ('Assets', 'city.png'))
city1 = pygame.transform.scale(city, (500, 900))
patrol = pygame.image.load(os.path.join ('Assets', 'patrol.png'))
rocket_image = pygame.image.load(os.path.join ('Assets', 'rocket2.png'))


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle1, angle2) -> None:   
        super().__init__()   
        self.image = pygame.transform.scale(laser_image, (LASER_WIDTH, LASER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(random.randint(angle1, angle2))
        self.hits = 1

    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health = 100, max_health = 100) -> None:
        super().__init__()
        self.image = pygame.transform.scale(final_boss, (BOSS_WIDTH, BOSS_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health
        self.max_health = max_health
        self.hits = 102
        self.should_remove = False
        self.destroyed = False
        self.lasers = []
        self.time_since_last_laser = 0
        self.laser_interval = 5

    def move(self):
        self.rect.x -= self.speed

        self.time_since_last_laser += 1
        if self.time_since_last_laser >= self.laser_interval:
            laser = Laser(
                self.rect.x + 70, self.rect.y + self.rect.height // 9, LAS_VEL, -22, 22)
            self.lasers.append(laser)
            self.time_since_last_laser = 0

        for laser in self.lasers:
            laser.move()

        if 0 < self.hits <= 3:
            self.image = pygame.transform.scale(boss_explosion, (400, 400))
        elif self.hits <= 0:
            self.should_remove = True

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y + self.image.get_height() - 250, self.image.get_width(), 7))
        pygame.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y + self.image.get_height() - 250, self.image.get_width() * (self.health/self.max_health), 7))

class Repair(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.image = pygame.transform.scale(repair_image, (REP_WIDTH, REP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed
            

class Medic(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.image = pygame.transform.scale(medic_health, (HEALTH_WIDTH, HEALTH_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed



class Submarine(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.image = pygame.transform.scale(submarine_image,(SUBMARINE_WIDTH, SUBMARINE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.hits = 1

    def move(self):
        self.rect.x -= self.speed



class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle1, angle2) -> None:   
        super().__init__()   
        self.image = pygame.transform.rotate(pygame.transform.scale(missile_image, (MISSLE_WIDTH, MISSLE_HEIGHT)), 10)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(random.randint(angle1, angle2))
        self.hits = 1

    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

    def move2(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)




class Battleship:
    def __init__(self, x, y, speed, angle_degrees) -> None:
        self.image = pygame.transform.rotate(pygame.transform.scale(battleship_image, (BATTLESHIP_WIDTH, BATTLESHIP_HEIGHT)), 40)  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(angle_degrees)
        self.hits = 45
        self.should_remove = False
        self.destroyed = False
        self.missiles = []
        self.time_since_last_missile = 0
        self.missile_interval = 25

    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

        self.time_since_last_missile += 1
        if self.time_since_last_missile >= self.missile_interval:
            missile = Missile(
                self.rect.x + 70, self.rect.y + self.rect.height // 9, MISS_VEL, -20, 20)
            self.missiles.append(missile)
            self.time_since_last_missile = 0

        for missile in self.missiles:
            missile.move()

        if 0 < self.hits <= 3:
            self.image = pygame.transform.scale(big_explosion, (300, 300))
        elif self.hits <= 0:
            self.should_remove = True



class Rockets(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle1, angle2) -> None:
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(rocket_image, (ROCK_WIDTH, ROCK_HEIGHT)), -5)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(random.randint(angle1, angle2))
        self.hits = 1

    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

    

class Patrol(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle_degrees) -> None:
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(patrol, (PATROL_WIDTH, PATROL_HEIGHT)), -50)  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(angle_degrees)
        self.hits = 25
        self.should_remove = False
        self.destroyed = False
        self.rockets = []
        self.time_since_last_rocket = 0
        self.rocket_interval = 5

    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)


        self.time_since_last_rocket += 1
        if self.time_since_last_rocket >= self.rocket_interval:
            rocket = Rockets(
                self.rect.x + 20, self.rect.y + self.rect.height // 5, ROCKET_VEL, -20, 20)
            self.rockets.append(rocket)
            self.time_since_last_rocket = 0

        for rocket in self.rockets:
            rocket.move()

        # if 0 < self.hits <= 3:
        #     self.image = pygame.transform.scale(boss_explosion, (400, 400))
        # elif self.hits <= 0:
        #     self.should_remove = True



class My_Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health = 100, max_health = 100) -> None:
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(my_ship_image, (MY_WIDTH, MY_HEIGHT)), 270)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health
        self.max_health = max_health

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y + self.image.get_height() + 10, self.image.get_width(), 8))
        pygame.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y + self.image.get_height() + 10, self.image.get_width() * (self.health/self.max_health), 8))

class Jet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.image = pygame.transform.scale(JET_IMAGE, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed


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

    for bullet in bullets.copy():
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


def draw_title_screen():
    WIN.fill((0, 0, 0))
    title_text = FONT.render('Welcome to BattleShip', 1, 'white')
    subtitle_text = FONT.render('Use "W, A, S, D" to control your battleship, press spacebar to shoot.', 1, 'red')
    subtitle_text2 = FONT.render('Protect your beach base from enemy fighter jets.', 1, 'white')
    subtitle_text3 = FONT.render('Missiles and lasers will damage your Battleship, but not your base.', 1, 'white')
    subtitle_text4 = FONT.render('Press Return key to begin... Good luck.', 1, 'white')
    subtitle_text5 = FONT.render('Medpacks (green) heal your ship and Repair icons (grey) add 1 life.', 1, 'white')
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

# Objects
    my_ship = My_Ship(100, 400, VEL)
    final_boss = FinalBoss(1300, 400, BOSS_VEL)
    laser = Laser(1300, 400, LAS_VEL, -20, 20)
    battleship = Battleship(1200 , -200, BATTLE_VEL, BATTLE_ANGLE)
    patrol = Patrol(1300, 850, PAT_VEL, Patrol_angle)
    missile = Missile(1200, -200, 10, -35, 5)
    rocket = Rockets(800, 800, ROCKET_VEL, -1, 1)
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

# MEDIC 
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

# REPAIR
                
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
# PATROL
        if patrol.rect.x < WIDTH - 1260:
            patrol_hit += 1
            patrol.kill()
            if patrol_hit == 1 and patrol.hits > 0:
                hits += 1
                explosion = Explosion3(patrol.rect.center)
                explosions.add(explosion) 

# ROCKETS
                
        for rocket in patrol.rockets[:]:
            if pygame.sprite.collide_rect(rocket, my_ship):
                patrol.rockets.remove(rocket)
                explosion = Explosion(my_ship.rect.center)
                explosions.add(explosion)
                my_ship.health -= 2
                break

# LASERS
                
        for laser in final_boss.lasers[:]:
            if pygame.sprite.collide_rect(laser, my_ship):
                final_boss.lasers.remove(laser)
                explosion = Explosion2(my_ship.rect.center)
                explosions.add(explosion)
                my_ship.health -= 10
                break

# MISSILES
        for missile in battleship.missiles[:]:
            if pygame.sprite.collide_rect(missile, my_ship):
                battleship.missiles.remove(missile)
                explosion = Explosion2(my_ship.rect.center)
                explosions.add(explosion)
                my_ship.health -= 20
                break
        
# SUBMARINES
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

# JETS
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



# Delay Start

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

# Handle Functions
        handle_bullets(bullets, jets, battleship, patrol, submarines, explosions, final_boss)
        draw_window(my_ship, bullets, elapsed_time, jets, battleship, patrol, rocket, missile, submarines, hits, explosions, medics, final_boss, laser, repairs)

    pygame.quit()



if __name__ == "__main__":
    main()