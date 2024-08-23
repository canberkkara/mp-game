import random
import pygame
from network import Network



global bossBeams
bossBeams = []




class Boss():
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (1600, 220))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.vel = 0
        self.beam_cooldown = 40
        self.beam_addition = 0
        self.bossHp = 150
        

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)
    

    def shoot(self,X):    
        if self.beam_cooldown > 0:
            self.beam_cooldown -= 1
        elif self.beam_cooldown == 0:
            random.seed(X + self.beam_addition)
            Y = random.randint(0,1600)
            bossBeam = BossBeam(Y, 151)
            bossBeams.append(bossBeam)
            self.beam_cooldown = 2 
            self.beam_addition += 1
            


    

class BossBeam():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("bossbeam.png")
        self.image = pygame.transform.scale(self.image, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 6
        self.lifetime = 2 

    def move(self):
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)
        self.lifetime -= 1 / 240 

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

    