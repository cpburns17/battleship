import pygame
import random
import os
import time
import sys
import math



#Patrol Dimensions
PATROL_WIDTH, PATROL_HEIGHT = 170, 30
Patrol_angle = 45

class Patrol(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle_degrees) -> None:
        from main import patrol
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
        self.rocket_interval = 10

    def move(self):
        from main import ROCKET_VEL
        from rockets import Rockets
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
