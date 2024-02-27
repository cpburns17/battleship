import pygame
import random
import os
import time
import sys
import math



# #Battleship Dimensions
BATTLESHIP_WIDTH, BATTLESHIP_HEIGHT = 240, 40
BATTLE_ANGLE = -35
BATTLE_ANGLE_2 = 45

class Battleship:
    def __init__(self, x, y, speed, angle_degrees) -> None:
        from main import battleship_image
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
        from missile import Missile
        from main import MISS_VEL, big_explosion
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

