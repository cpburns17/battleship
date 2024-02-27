import pygame
import random
import os
import time
import sys
import math


#My Ship Dimensions
MY_WIDTH, MY_HEIGHT = 25, 120


class My_Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health = 100, max_health = 100) -> None:
        from main import my_ship_image
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

