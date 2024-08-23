import pygame

from network import Network

width = 960
height = 540
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
        self.vel = 2

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect.topleft = (self.x, self.y)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def redrawWindow(win, player,player2, background_image):
    win.blit(background_image, (0, 0))
    player.draw(win)
    player2.draw(win)

    pygame.display.update()

def main():
    run = True
    player_image_path = "player.png"
    background_image_path = "background.jpg"
    n = Network()
    startPos = read_pos(n.getPos())
    p2 = Player(startPos[0], startPos[1], player_image_path)
    p = Player(50, 50, player_image_path)
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (width, height))

    clock = pygame.time.Clock()

    while run:
        clock.tick(240)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p,p2, background_image)

main()