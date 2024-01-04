import pygame
import random
import os
import time
import sys
import math

# from pygame.sprite import _Group
pygame.font.init()

#WIN means WINDOW
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PROJECT MAYHEM")

MOWER_HIT = pygame.USEREVENT +1

#WATER BACKGROUND
BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'water1.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (1200, 800))

# Page colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont('comicsans', 30)


FPS = 60
VEL = 12
# LIVES = 3
RABBIT_VEL = 5
SHIP_VEL = 5
BATTLE_VEL = 1
SUB_VEL = 12
BULLET_VEL = 20
MAX_BULLETS = 500
DELAY_START = 45
SEC_DELAY_START = 80
SUB_DELAY_START = 10

#MY SHIP DIMENSIONS
MY_WIDTH, MY_HEIGHT = 25, 120

#Explosion Dimensions
EXPLODE_WIDTH, EXPLODE_HEIGHT = 58, 58

#JET DIMENSIONS
RABBIT_WIDTH, RABBIT_HEIGHT = 10, 30

# #Battleship Dimensions
BATTLESHIP_WIDTH, BATTLESHIP_HEIGHT = 240, 40
BATTLE_ANGLE = -35
BATTLE_ANGLE_2 = 45

# Missle Dimensions
MISSLE_WIDTH, MISSLE_HEIGHT = 90, 90

#Subarine Dimensions
SUBMARINE_WIDTH, SUBMARINE_HEIGHT = 35, 15

#JET 
JET_IMAGE = pygame.image.load(os.path.join('Assets', 'jet.png'))
JET = pygame.transform.scale(JET_IMAGE, (150, 150))

submarine_image = pygame.image.load(os.path.join('Assets', 'submarine.png'))
missile_image = pygame.image.load(os.path.join('Assets', 'missile.png'))
battleship_image = pygame.image.load(os.path.join('Assets', 'battleship.png'))
my_ship_image = pygame.image.load(os.path.join('Assets', 'ship.png'))


# class Base():
#     def __init__(self, health = 100) -> None:
#         self.max_health = health
#         self.image = pygame.image.load(os.path.join('Assets', 'city.png'))

#     def draw(self, window):
#         self.healthbar(window)

#     def healthbar(self, window):
#         pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width(), 10))
#         pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width() * (self.health/self.max_health), 10))

# base = Base(100)

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



class Missile:
    def __init__(self, x, y, speed, angle_degrees) -> None:      
        self.image = pygame.transform.rotate(pygame.transform.scale(missile_image, (MISSLE_WIDTH, MISSLE_HEIGHT)), 10)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(angle_degrees)
        self.hits = 1

    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

    def move2(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

missile_image = pygame.image.load(os.path.join('Assets', 'missile.png'))



class Battleship:
    def __init__(self, x, y, speed, angle_degrees) -> None:
        self.image = pygame.transform.rotate(pygame.transform.scale(battleship_image, (BATTLESHIP_WIDTH, BATTLESHIP_HEIGHT)), 40)  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(angle_degrees)
        self.hits = 100
        self.should_remove = False

# Creates missile objects
        self.missiles = []
        self.time_since_last_missile = 0
        self.missile_interval = 70

# Moves battleship at angle across screen
    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

# This is how missiles are fired/move across screen
        self.time_since_last_missile += 1
        if self.time_since_last_missile >= self.missile_interval:
            missile = Missile(
                self.rect.x + 70, self.rect.y + self.rect.height // 9, 10, -5)
            self.missiles.append(missile)
            self.time_since_last_missile = 0

        for missile in self.missiles:
            missile.move()

        if self.hits <= 0:
            self.should_remove = True
# MOVE 2
    def move2(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

        # This is how missiles are fired/move across screen
        self.time_since_last_missile += 1
        if self.time_since_last_missile >= self.missile_interval:
            missile = Missile(
                self.rect.x + 70, self.rect.y + self.rect.height // 9, 10, -5)
            self.missiles.append(missile)
            self.time_since_last_missile = 0

        for missile in self.missiles:
            missile.move()

        if self.hits <= 0:
            self.should_remove = True

battleship = Battleship(1200 , -200, BATTLE_VEL, BATTLE_ANGLE)
battleship2 = Battleship(100, 1000, BATTLE_VEL, BATTLE_ANGLE_2)



class My_Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(my_ship_image, (MY_WIDTH, MY_HEIGHT)), 270)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
my_ship = My_Ship(400, 400, VEL)

explosion_image = pygame.image.load(os.path.join('Assets', 'explosion.png'))
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center) -> None:
        super().__init__()
        self.image = pygame.transform.scale(explosion_image, (EXPLODE_WIDTH, EXPLODE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.creation_time = time.time()



def draw_window(my_ship, bullets, elapsed_time, rabbits, battleship, battleship2, missile, submarines, hits, health, explosions):
    LIVES = 3
    LIVES -= hits
    # HEALTH = 10

    WIN.blit(BACKGROUND, (0,0))
    # WIN.blit(base.image, (-440, 20))

    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white')
    WIN.blit(time_text, (550, 10))

    lives_label = FONT.render(f"Lives: {LIVES}", 1, 'white')
    WIN.blit(lives_label, (10, 10))

    WIN.blit(my_ship.image, my_ship.rect)

    if battleship is not None and battleship.hits > 0:
        WIN.blit(battleship.image, battleship.rect)
        WIN.blit(battleship2.image, battleship2.rect)
        for missile in battleship.missiles:
            WIN.blit(missile.image, missile.rect)
            missile.move()
            missile.move2()
            
    for submarine in submarines:
        WIN.blit(submarine.image, submarine.rect)

    for rabbit in rabbits:
        pygame.draw.rect(WIN, BLACK, rabbit)
        WIN.blit(JET, (rabbit.x -65, rabbit.y - 65))

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


def handle_bullets(bullets, rabbits, battleship, submarines, explosions):
    bullets_to_remove = []
    explosions_to_remove = []

    for bullet in bullets:
        bullet.x += BULLET_VEL

        if battleship is not None and bullet.colliderect(battleship.rect):
            battleship.hits -= 1
            bullets_to_remove.append(bullet)

        for submarine in submarines[:]:
            if bullet.colliderect(submarine.rect):
                submarine.hits -= 1
                bullets_to_remove.append(bullet)

                if submarine.hits <= 0:
                    explosion = Explosion(submarine.rect.center)
                    explosions.add(explosion)
                    submarines.remove(submarine)
                    
    for rabbit in rabbits[:]:
        for bullet in bullets[:]:
            if bullet.colliderect(rabbit):
                rabbits.remove(rabbit)
                bullets_to_remove.append(bullet)
                explosion = Explosion(rabbit.center)
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


    my_ship = My_Ship(400, 400, VEL)
    missile = Missile(1200, -200, 10, -35)
    explosions = pygame.sprite.Group() 


    rabbit_add_increment = 2000
    rabbit_count = 0
    rabbits = []
    bullets = []
    submarines = []
    hits = 0
    health = 10

# RUNNING GAME
    while run:
        clock.tick(FPS)
        rabbit_count += clock.tick(FPS)
        elapsed_time = time.time() - start_time

        
# SUBMARINES
        if elapsed_time >= SUB_DELAY_START:
            if random.randint(0, 100) < 2:  
                submarine_y = random.randint(0, HEIGHT - SUBMARINE_HEIGHT)
                submarine = Submarine(WIDTH, submarine_y, SUB_VEL)
                submarines.append(submarine)

            for submarine in submarines[:]:
                submarine.move()
                if pygame.sprite.collide_rect(submarine, my_ship):
                    submarines.remove(submarine)
                    print("hit by sub")
                    hits +=1
                    break


# JETS (rabbits)
        for rabbit in rabbits[:]:
            rabbit.x -= RABBIT_VEL
            if rabbit.x > WIDTH:
                health -= 1
                rabbits.remove(rabbit)
            elif rabbit.colliderect(my_ship):
                rabbits.remove(rabbit)
                hits +=1
                break

        if hits >= 3:
            lost_text = FONT.render('You lost!', 1, 'white')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        if rabbit_count > rabbit_add_increment:
            for _ in range(1):
                rabbit_x = random.randint(WIDTH, WIDTH)
                rabbit_y = random.randint(0, HEIGHT - RABBIT_WIDTH)
                rabbit = pygame.Rect(rabbit_x, rabbit_y, RABBIT_HEIGHT, RABBIT_WIDTH + 10)
                rabbits.append(rabbit)
            
            rabbit_add_increment = max(200, rabbit_add_increment -40)
            rabbit_count = 0

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
        if elapsed_time >= DELAY_START:
            battleship.move()
            missile.move()

        if elapsed_time >= SEC_DELAY_START:
            battleship2.move2()
            missile.move2()

# Handle Functions
        handle_bullets(bullets, rabbits, battleship, submarines, explosions)

        draw_window(my_ship, bullets, elapsed_time, rabbits, battleship, battleship2, missile, submarines, hits, health, explosions)

    pygame.quit()



if __name__ == "__main__":
    main()