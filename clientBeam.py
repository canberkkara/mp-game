
import time
import pygame
import threading
from boss import *

from network import Network


######## iki oyuncunun da cooldownunu aynı anda başlatmazsan iki oyuncu da farklı beamler görür


width = 1600
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

class Player():
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 8
        self.isBeamShotPlayer = 0
        self.beam_cooldown = 2
        self.hp = 1
    

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

    def move(self,currentPlayer):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]and self.x < 1470:
            self.x += self.vel

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel

        if keys[pygame.K_UP] and self.y > 150:
            self.y -= self.vel

        if keys[pygame.K_DOWN]and self.y < 770:
            self.y += self.vel
        
        if self.beam_cooldown > 0:
            self.beam_cooldown -= 1
        
        if keys[pygame.K_SPACE] and self.beam_cooldown == 0 and self.hp != 0 and currentPlayer == 2:
            self.isBeamShotPlayer = 1
            self.beam_cooldown = 60
        else: 
            self.isBeamShotPlayer = 0
            
        
        

        self.update()

    def shoot(self):
        beam = Beam(self.x + self.rect.width / 2, self.y)
        beams.append(beam)
        self.beam_cooldown = 20
        ##self.isBeamShot = 0    

    def update(self):
        self.rect.topleft = (self.x, self.y)
        if self.isBeamShotPlayer == 1:
            self.shoot()

class Beam():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("beam.png")
        self.image = pygame.transform.scale(self.image, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 10
        self.lifetime = 2

    def move(self):
        self.y -= self.vel
        self.rect.topleft = (self.x, self.y)
        self.lifetime -= 1 / 60

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4]), int(str[5]), int(str[6])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])+ "," + str(tup[2])+ "," + str(tup[3])+ "," + str(tup[4])+ "," + str(tup[5])+ "," + str(tup[6])

def redrawWindow(win, player,player2,boss, background_image):
    win.blit(background_image, (0, 0))
    if player.hp != 0:
        player.draw(win)
    if player2.hp != 0:
        player2.draw(win)
    boss.draw(win)
    for beam in beams:
        if player.hp != 0: 
            beam.move()
            if beam.y <= 150 and beam.y >= 0:
                boss.bossHp -= 1
                beam.y = -500
                del beam
            else :
                beam.draw(win)
    for beam in beams2:
        if player2.hp != 0: 
            beam.move()
            if beam.y <= 150 and beam.y >= 0:
                #boss.bossHp -= 1
                beam.y = -500
                del beam
            else :
                beam.draw(win)
    for bossbeam in bossBeams:
        bossbeam.move()
        if -40 <= ( bossbeam.y -120 - player.y + 65  ) < 40 and -20 <= (bossbeam.x + -120 - player.x + 65) < 20:   
            player.hp = 0
        if bossbeam.lifetime > 0:
            bossbeam.draw(win)
    pygame.display.update()
    return boss.bossHp


def redrawWindowWin(win, background_image):
    win.blit(background_image, (0, 0))
    pygame.display.update()
    
def redrawWindowLose1(win, background_image):
    win.blit(background_image, (0, 0))
    pygame.display.update()
    

def main():
    run = True
    player_image_path = "player.png"
    player2_image_path = "player2.png" 
    boss_image_path = "boss.png"
    background_image_path = "background.jpg"
    win_image_path = "drip_goku.png"
    lose1_image_path = "loser.png"
    n = Network()
   
    startPos = read_pos(n.getPos())
    p2 = Player(startPos[0], startPos[1], player2_image_path)
    p = Player(startPos[0] , startPos[1], player_image_path)
    b = Boss(boss_image_path)

    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (width, height))
    win_image = pygame.image.load(win_image_path)
    win_image = pygame.transform.scale(win_image, (width, height))
    lose1_image = pygame.image.load(lose1_image_path)
    lose1_image = pygame.transform.scale(lose1_image, (width, height))
    

    clock = pygame.time.Clock()

    global bossHp, bossBeamX
    global beams
    global beams2
    beams = []
    beams2 = []
    

    bossBeamX = 31
    currentPlayer = 0
    singleTimeCooldown = 240
    bossHp = 150
    

    while run:
        clock.tick(60)
        

        p2Pos = read_pos(n.send(make_pos((p.x, p.y,p.isBeamShotPlayer,b.bossHp,p.hp,bossBeamX,currentPlayer))))
        
        if(bossHp < p2Pos[3]):
             b.bossHp = bossHp
        else:
           b.bossHp = p2Pos[3]

        if (p.hp != 0 or p2.hp != 0) and (b.bossHp != 0):
            b.bossHp = redrawWindow(win, p,p2,b, background_image)

        elif p.hp == 0 and p2.hp == 0:
            redrawWindowLose1(win,lose1_image)

        elif b.bossHp == 0:
            redrawWindowWin(win,win_image)
        
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.isBeamShotPlayer = p2Pos[2]
        bossBeamX = p2Pos[5]
        currentPlayer = p2Pos[6]
        
        p2.hp = p2Pos[4]
        if(currentPlayer == 2):
            singleTimeCooldown -= 1
            if(singleTimeCooldown <= 0):
                b.shoot(bossBeamX)
        p2.update()
        if p2.isBeamShotPlayer == 1 and p2.beam_cooldown == 0:
            p2.shoot()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move(currentPlayer)

        beams = [beam for beam in beams if beam.lifetime > 0]

       
        bossHp = b.bossHp

        print("Player1 HP: " + str(p.hp))
        print("Player2 HP: " + str(p2.hp))
        print("Boss HP: " + str(b.bossHp))


       

main()