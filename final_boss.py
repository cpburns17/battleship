import pygame
import random
import os
import time
import sys
import math


#Final Boss Dimensions
BOSS_WIDTH, BOSS_HEIGHT = 400, 200


class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health = 100, max_health = 100) -> None:
        from main import final_boss
        super().__init__()
        self.image = pygame.transform.scale(final_boss, (BOSS_WIDTH, BOSS_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health
        self.max_health = max_health
        self.hits = 102
        self.should_remove = False
        self.destroyed = False
        self.lasers = []
        self.time_since_last_laser = 0
        self.laser_interval = 5

    def move(self):
        from laser import Laser
        from main import LAS_VEL, boss_explosion
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
