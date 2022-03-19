import pygame as pg
import os


WIDTH = 1280
HEIGHT = 720
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Star Defender")
clock = pg.time.Clock()

game_folder = os.path.dirname(__file__)
print(game_folder)
img_folder = os.path.join(game_folder, 'img')
player_img = pg.image.load(os.path.join(img_folder, 'starship.png')).convert()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pg.key.get_pressed()

        if keystate[pg.K_w]:
            self.speedy = -10

        if keystate[pg.K_a]:
            self.speedx = -10

        if keystate[pg.K_s]:
            self.speedy = 10

        if keystate[pg.K_d]:
            self.speedx = 10

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.top < 0:
            self.rect.top = 0

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)
    all_sprites.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()

