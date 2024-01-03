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
GRASS_BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'underwater.png'))
GRASS_BACKGROUND = pygame.transform.scale(GRASS_BACKGROUND_IMAGE, (1200, 800))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont('comicsans', 30)
# BORDER = pygame.Rect(WIDTH/2 -5, 0, 10, HEIGHT)

FPS = 60
VEL = 10
# LIVES = 3
RABBIT_VEL = 5
SHIP_VEL = 5
BATTLE_VEL = 5
SUB_VEL = 20
BULLET_VEL = 20
MAX_BULLETS = 500
DELAY_START = 1
SEC_DELAY_START = 5
SUB_DELAY_START = 5

#MY SHIP DIMENSIONS
MY_WIDTH, MY_HEIGHT = 25, 120

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
JET_IMAGE = pygame.image.load(
    os.path.join('Assets', 'jet.png')
)
JET = pygame.transform.scale(JET_IMAGE, (150, 150))

submarine_image = pygame.image.load(os.path.join('Assets', 'submarine.png'))
missile_image = pygame.image.load(os.path.join('Assets', 'missile.png'))
battleship_image = pygame.image.load(os.path.join('Assets', 'battleship.png'))
my_ship_image = pygame.image.load(os.path.join('Assets', 'ship.png'))


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

missile_image = pygame.image.load(os.path.join('Assets', 'missile.png'))
missile = Missile(1200, -200, 10, -35)


class Battleship:
    def __init__(self, x, y, speed, angle_degrees) -> None:
        self.image = pygame.transform.rotate(pygame.transform.scale(battleship_image, (BATTLESHIP_WIDTH, BATTLESHIP_HEIGHT)), 40)  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = math.radians(angle_degrees)
        self.hits = 50
        self.should_remove = False

        # Creates missile objects
        self.missiles = []
        self.time_since_last_missile = 0
        self.missile_interval = 10

        # Moves battleship at angle across screen
    def move(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

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
            print(f"Before  {self.rect.x}")
            missile.move()
            print(f"After {self.rect.x}")


        # This is for when Battleship hits are less than zero it will remove
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


def draw_window(my_ship, bullets, elapsed_time, rabbits, battleship, battleship2, missile, submarines, hits):
    LIVES = 3
    LIVES -= hits

    WIN.blit(GRASS_BACKGROUND, (0,0))

    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white')
    WIN.blit(time_text, (550, 10))

    lives_label = FONT.render(f"Lives: {LIVES}", 1, 'white')
    WIN.blit(lives_label, (10, 10))

    WIN.blit(my_ship.image, my_ship.rect)

    if battleship is not None and battleship.hits > 0:
        WIN.blit(battleship.image, battleship.rect)
        for missile in battleship.missiles:
            WIN.blit(missile.image, missile.rect)
            
        WIN.blit(battleship2.image, battleship2.rect)
    
    for submarine in submarines:
        WIN.blit(submarine.image, submarine.rect)

    for rabbit in rabbits:
        pygame.draw.rect(WIN, BLACK, rabbit)
        WIN.blit(JET, (rabbit.x -65, rabbit.y - 65))

    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and my_ship.rect.x - VEL >=0: #left
        my_ship.rect.x -= VEL 
    if keys[pygame.K_d]: #right
        my_ship.rect.x += VEL
    if keys[pygame.K_w] and my_ship.rect.y - VEL >= -10: #up
        my_ship.rect.y -= VEL
    if keys[pygame.K_s] and my_ship.rect.y + VEL <= 780: #down
        my_ship.rect.y += VEL


def handle_bullets(bullets, rabbits, battleship, submarines):
    bullets_to_remove = []

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
                    submarines.remove(submarine)
                
        for rabbit in rabbits[:]:
            if bullet.colliderect(rabbit):
                rabbits.remove(rabbit)
                bullets_to_remove.append(bullet)
                break

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

def main():
    run = True
    my_ship = My_Ship(400, 400, VEL)
    missile = Missile(1200, -200, 10, -35)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    rabbit_add_increment = 2000
    rabbit_count = 0

    rabbits = []
    bullets = []
    submarines = []
    hits = 0


    while run:
        clock.tick(FPS)
        rabbit_count += clock.tick(FPS)
        elapsed_time = time.time() - start_time

        if elapsed_time >= SUB_DELAY_START:
            if random.randint(0, 100) < 4:  # Adjust the probability as needed
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


# FOR NOW, rabbits are the jets 
        for rabbit in rabbits[:]:
            rabbit.x -= RABBIT_VEL
            if rabbit.x > WIDTH:
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

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        my_ship.rect.x + 70, my_ship.rect.y + MY_HEIGHT//9, 10, 5)
                    bullets.append(bullet)

        if elapsed_time >= DELAY_START:
            battleship.move()
            missile.move()

        if elapsed_time >= SEC_DELAY_START:
            battleship2.move2()


        handle_bullets(bullets, rabbits, battleship, submarines)

        draw_window(my_ship, bullets, elapsed_time, rabbits, battleship, battleship2, missile, submarines, hits)

    pygame.quit()



if __name__ == "__main__":
    main()