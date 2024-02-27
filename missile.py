import pygame
import random
import os
import time
import sys
import math


# Missle Dimensions
MISSLE_WIDTH, MISSLE_HEIGHT = 35, 17


class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle1, angle2) -> None:  
        from main import missile_image 
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