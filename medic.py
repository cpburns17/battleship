import pygame
import random
import os
import time
import sys
import math


#Medic Dimensions
HEALTH_WIDTH, HEALTH_HEIGHT = 50, 50

class Medic(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        from main import medic_health
        super().__init__()
        self.image = pygame.transform.scale(medic_health, (HEALTH_WIDTH, HEALTH_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed