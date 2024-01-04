import pygame
import random
import os
import time
import sys
import math

pygame.font.init()
from pygame.sprite import Sprite

#WIN means WINDOW
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PROJECT MAYHEM")

#WATER BACKGROUND
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'water1.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (1200, 800))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont('comicsans', 30)
MOWER_HIT = pygame.USEREVENT +1
FPS = 60

#Velocity 
VEL = 12
JET_VEL = 4
SUB_VEL = 9
BATTLE_VEL = 1
MISS_VEL = 15
BULLET_VEL = 20
MEDIC_VEL = 4
REP_VEL = 4
BOSS_VEL = 1
LAS_VEL = 30

MAX_BULLETS = 500

#Start times
BATTLE_DELAY_START = 40
SUB_DELAY_START = 6
MEDIC_DELAY_START = 10
BOSS_DELAY_START = 85

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
city = pygame.image.load(os.path.join ('Assets', 'city1.png'))
city1 = pygame.transform.scale(city, (500, 900))


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
        self.hits = 100
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
                self.rect.x + 70, self.rect.y + self.rect.height // 9, MISS_VEL, -10, 10)
            self.missiles.append(missile)
            self.time_since_last_missile = 0

        for missile in self.missiles:
            missile.move()

        if 0 < self.hits <= 3:
            self.image = pygame.transform.scale(big_explosion, (300, 300))
        elif self.hits <= 0:
            self.should_remove = True


# battleship = Battleship(1200 , -200, BATTLE_VEL, BATTLE_ANGLE)
# battleship2 = Battleship(100, 1000, BATTLE_VEL, BATTLE_ANGLE_2)



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



def draw_window(my_ship, bullets, elapsed_time, jets, battleship, missile, submarines, hits, explosions, medics, final_boss, laser, repairs):
    LIVES = 3
    LIVES -= hits

    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(beach, (-270, 0) )
    # WIN.blit(city1, (-200, 0))

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
        pygame.draw.rect(WIN, BLACK, jet)
        WIN.blit(JET, (jet.x -65, jet.y - 65))

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


def handle_bullets(bullets, jets, battleship, submarines, explosions, final_boss):
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
                    
    for jet in jets[:]:
        for bullet in bullets[:]:
            if bullet.colliderect(jet):
                jets.remove(jet)
                bullets_to_remove.append(bullet)
                explosion = Explosion(jet.center)
                explosions.add(explosion)
                break

    for explosion in explosions:
        if time.time() - explosion.creation_time >= 1:
            explosions_to_remove.append(explosion)

    for explosion in explosions_to_remove:
        explosions.remove(explosion)

    for bullet in bullets_to_remove:
        bullets.remove(bullet)
    

def main():
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0


    my_ship = My_Ship(100, 400, VEL)
    final_boss = FinalBoss(1300, 400, BOSS_VEL)
    laser = Laser(1300, 400, LAS_VEL, -20, 20)
    battleship = Battleship(1200 , -200, BATTLE_VEL, BATTLE_ANGLE)
    missile = Missile(1200, -200, 10, -35, 5)
    explosions = pygame.sprite.Group() 
    # medic = Medic()


    jet_add_increment = 2100
    jet_count = 0
    jets = []
    bullets = []
    submarines = []
    medics = []
    repairs = []
    missiles = []
    hits = 0

# RUNNING GAME
    while run:
        clock.tick(FPS)
        jet_count += clock.tick(FPS)
        elapsed_time = time.time() - start_time

# MEDIC 
        if elapsed_time >= MEDIC_DELAY_START:
            if random.randint(0, 500) < 1:  
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
                
        if elapsed_time >= MEDIC_DELAY_START:
            if random.randint(0, 500) < 1:  
                repair_y = random.randint(0, HEIGHT - REP_HEIGHT)
                repair = Repair(WIDTH, repair_y, MEDIC_VEL)
                repairs.append(repair)

            for repair in repairs[:]:
                repair.move()
                if pygame.sprite.collide_rect(repair, my_ship):
                    hits -= 1
                    repairs.remove(repair)
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
            if random.randint(0, 100) < 2:  
                submarine_y = random.randint(0, HEIGHT - SUBMARINE_HEIGHT)
                submarine = Submarine(WIDTH, submarine_y, SUB_VEL)
                submarines.append(submarine)

# JETS
        for jet in jets[:]:
            jet.x -= JET_VEL
            if jet.x < WIDTH - 1200:
                hits +=1
                jets.remove(jet)
                explosion = Explosion3(jet.center)
                explosions.add(explosion) 
            elif jet.colliderect(my_ship):
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
                jet_x = random.randint(WIDTH, WIDTH)
                jet_y = random.randint(0, HEIGHT - (JET_WIDTH + 5))
                jet = pygame.Rect(jet_x, jet_y, JET_HEIGHT, JET_WIDTH + 10)
                jets.append(jet)
            
            jet_add_increment = max(200, jet_add_increment -50)
            jet_count = 0
        elif elapsed_time >= BOSS_DELAY_START:
            jet_add_increment = 60000


# Pygame.event 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        my_ship.rect.x + 70, my_ship.rect.y + MY_HEIGHT//9, 10, 5)
                    bullets.append(bullet)

# Delay Start
        if elapsed_time >= BATTLE_DELAY_START:
            if battleship.destroyed == False:
                battleship.move()
                missile.move()

        if elapsed_time >= BOSS_DELAY_START:
            if final_boss.destroyed == False:
                final_boss.move()
                laser.move

# Handle Functions
        handle_bullets(bullets, jets, battleship, submarines, explosions, final_boss)
        # print(battleship)
        draw_window(my_ship, bullets, elapsed_time, jets, battleship, missile, submarines, hits, explosions, medics, final_boss, laser, repairs)

    pygame.quit()



if __name__ == "__main__":
    main()