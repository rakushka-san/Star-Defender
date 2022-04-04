import pygame as pg
import random
import os


WIDTH = 1280
HEIGHT = 720
PLAYZONE_WIDTH = 720
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
assets_folder = os.path.join(game_folder, 'assets')
img_folder = os.path.join(assets_folder, 'img')
fonts_folder = os.path.join(assets_folder, 'fonts')
snd_folder = os.path.join(assets_folder, 'snd')

player_img = pg.image.load(os.path.join(img_folder, 'starship.png')).convert()
player_img = pg.transform.scale(player_img, (100, 100))

meteor_img = pg.image.load(os.path.join(img_folder, 'meteor.png')).convert()
bullet_img = pg.image.load(os.path.join(img_folder, 'bullet.png')).convert()

bg_img = pg.image.load(os.path.join(img_folder, 'background.png')).convert()
bg_rect = bg_img.get_rect()
bg_rect.centery = 0

expl_sounds = []
for snd in ['expl1.wav', 'expl2.wav']:
    expl_sounds.append(pg.mixer.Sound(os.path.join(snd_folder, snd)))
shoot_snd = pg.mixer.Sound(os.path.join(snd_folder, 'shoot.wav'))
heal_snd = pg.mixer.Sound(os.path.join(snd_folder, 'heal.wav'))
pwrup_snd = pg.mixer.Sound(os.path.join(snd_folder, 'pwrup.wav'))
alert_snd = pg.mixer.Sound(os.path.join(snd_folder, 'alert.wav'))
pg.mixer.music.load(os.path.join(snd_folder, 'music.wav'))

explosion_anim = {}
explosion_anim['large'] = []
explosion_anim['small'] = []

for i in range(9):
    filename = 'explosion' + str(i) + '.png'
    img = pg.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pg.transform.scale(img, (82, 80))
    img_small = pg.transform.scale(img, (41, 40))
    explosion_anim['large'].append(img_large)
    explosion_anim['small'].append(img_small)

drops_img = {}
drops_img['health'] = pg.image.load(os.path.join(img_folder, 'health.png')).convert()
drops_img['up'] = pg.image.load(os.path.join(img_folder, 'up.png')).convert()

score = 0
powerups = 0

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.6)/2)
        # pg.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.rect.centerx = PLAYZONE_WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.dmg = 40

    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.shoot()

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

        if self.rect.right > PLAYZONE_WIDTH:
            self.rect.right = PLAYZONE_WIDTH

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_snd.set_volume(0.5)
            shoot_snd.play()


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = meteor_img
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.85) / 2)
        # pg.draw.circle(self.image, BLACK, self.rect.center, self.radius)
        self.rect.x = random.randrange(PLAYZONE_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4, 10)
        self.rotation = 0
        self.rotation_speed = random.randrange(-10, 10)
        self.last_update = pg.time.get_ticks()
        self.health = 50 + int(0.1 * score)

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
            new_mob()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Drop(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['health', 'up'])
        self.image = drops_img[self.type]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

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

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(os.path.join(fonts_folder, 'OutlinePixel7.ttf'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    color = (0, 200, 0)
    if pct <= 30:
        color = (196, 0, 5)
    BAR_LENGTH = 520
    BAR_HEIGHT = 26
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, color, fill_rect)
    pg.draw.rect(surf, color, outline_rect, 2)

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.anim_speed = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.anim_speed:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

mobs = pg.sprite.Group()
bullets = pg.sprite.Group()
drops = pg.sprite.Group()

for i in range(8):
    new_mob()

pg.mixer.music.play(loops=-1)

running = True
while running:
    clock.tick(FPS)
    all_sprites.update()

    hits = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_circle)
    for hit in hits:
        player.health -= 31
        explosion = Explosion(hit.rect.center, 'small')
        all_sprites.add(explosion)
        random.choice(expl_sounds).play()
        alert_snd.play()
        new_mob()
        if player.health <= 0:
            running = False


    hits = pg.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        hit.health -= player.dmg
        if hit.health <= 0:
            explosion = Explosion(hit.rect.center, 'large')
            all_sprites.add(explosion)
            random.choice(expl_sounds).play()
            hit.kill()
            score += 50
            new_mob()
            if random.random() > 0.9:
                drop = Drop(hit.rect.centerx, hit.rect.centery)
                all_sprites.add(drop)
                drops.add(drop)

        if hit.health > 0:
            explosion = Explosion(hit.rect.center, 'small')
            all_sprites.add(explosion)
            random.choice(expl_sounds).play()

    hits = pg.sprite.spritecollide(player, drops, True)
    for hit in hits:
        if hit.type == 'health':
            player.health += 33
            if player.health >= 100:
                player.health = 100
            heal_snd.play()
        if hit.type == 'up':
            powerups += 1
            pwrup_snd.play()
            player.dmg += 40

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    screen.fill(BLACK)
    bg_rect.centery += 1
    if bg_rect.centery == HEIGHT:
        bg_rect.centery = 0
    screen.blit(bg_img, bg_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Счет: " + str(score), 52, PLAYZONE_WIDTH + 20, 20)
    draw_text(screen, "Урон: " + str(player.dmg), 52, PLAYZONE_WIDTH + 20, 72)
    draw_text(screen, "Здоровье:", 52, PLAYZONE_WIDTH + 20, HEIGHT - 98)
    draw_health_bar(screen, PLAYZONE_WIDTH + 20, HEIGHT - 46, player.health)
    pg.display.flip()

pg.quit()

