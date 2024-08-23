import pygame

width = 1920
height = 1080
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
        self.is_shooting = False
        self.beam_cooldown = 0

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

        self.rect.topleft = (self.x, self.y)

        # Handle beam cooldown
        if self.beam_cooldown > 0:
            self.beam_cooldown -= 1

        if keys[pygame.K_f] and self.beam_cooldown == 0:
            self.shoot()

    def shoot(self):
        beam = Beam(self.x + self.rect.width / 2, self.y)
        beams.append(beam)
        self.beam_cooldown = 20

class Beam():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("beam.png")
        self.image = pygame.transform.scale(self.image, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 5
        self.lifetime = 2

    def move(self):
        self.y -= self.vel
        self.rect.topleft = (self.x, self.y)
        self.lifetime -= 1 / 240

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

def redrawWindow(win, player, background_image):
    win.blit(background_image, (0, 0))
    player.draw(win)
    for beam in beams:
        beam.move()
        if beam.lifetime > 0:
            beam.draw(win)
    pygame.display.update()

def main():
    run = True
    player_image_path = "player.png"
    background_image_path = "background.jpg"
    p = Player(50, 50, player_image_path)
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (width, height))

    clock = pygame.time.Clock()

    global beams
    beams = []

    while run:
        clock.tick(240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()

        beams = [beam for beam in beams if beam.lifetime > 0]

        redrawWindow(win, p, background_image)

if __name__ == "__main__":
    pygame.init()
    main()

