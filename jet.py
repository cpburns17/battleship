import pygame
import random
import os
import time
import sys
import math

#Jet Dimensions
JET_WIDTH, JET_HEIGHT = 80, 50


class Jet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        from main import JET_IMAGE
        super().__init__()
        self.image = pygame.transform.scale(JET_IMAGE, (JET_WIDTH, JET_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed

