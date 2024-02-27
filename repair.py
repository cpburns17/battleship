import pygame
import random
import os
import time
import sys
import math


#Repair Dimensions
REP_WIDTH, REP_HEIGHT = 31, 31


class Repair(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        from main import repair_image
        super().__init__()
        self.image = pygame.transform.scale(repair_image, (REP_WIDTH, REP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed