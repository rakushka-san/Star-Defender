import pygame as pg
import random
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
meteor_img = pg.image.load(os.path.join(img_folder, 'meteor.png')).convert()
bullet_img = pg.image.load(os.path.join(img_folder, 'bullet.png')).convert()
bg_img = pg.image.load(os.path.join(img_folder, 'background.png')).convert()
bg_rect = bg_img.get_rect()


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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4, 10)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

mobs = pg.sprite.Group()
bullets = pg.sprite.Group()

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

running = True
while running:
    clock.tick(FPS)
    all_sprites.update()

    hits_player = pg.sprite.spritecollide(player, mobs, False)
    if hits_player:
        running = False

    hits_mobs = pg.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits_mobs:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()


    screen.fill(BLACK)
    screen.blit(bg_img, bg_rect)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()

