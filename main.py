import sys

import pygame as pg
import random
import os
import json


WIDTH = 1280
HEIGHT = 720
PLAYZONE_WIDTH = 720
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Star Defender")
clock = pg.time.Clock()

game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, 'assets')
user_folder = os.path.join(game_folder, 'user')
img_folder = os.path.join(assets_folder, 'img')
fonts_folder = os.path.join(assets_folder, 'fonts')
snd_folder = os.path.join(assets_folder, 'snd')

player_img = pg.image.load(os.path.join(img_folder, 'starship.png')).convert()
player_img = pg.transform.scale(player_img, (96, 80))

bg_img = pg.image.load(os.path.join(img_folder, 'background.png')).convert()
bg_rect = bg_img.get_rect()
bg_rect.centery = 0

drops_img = {}
drops_img['health'] = pg.image.load(os.path.join(img_folder, 'health.png')).convert()
drops_img['up'] = pg.image.load(os.path.join(img_folder, 'up.png')).convert()

explosion_anim = {}
explosion_anim['large'] = []
explosion_anim['small'] = []

for i in range(7):
    filename = 'expl' + str(i) + '.png'
    img = pg.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pg.transform.scale(img, (62, 62))
    img_small = pg.transform.scale(img, (31, 31))
    explosion_anim['large'].append(img_large)
    explosion_anim['small'].append(img_small)

ebullet_img = pg.image.load(os.path.join(img_folder, 'ebullet.png')).convert()
bullet_img = []
for i in range(4):
    bullet_img.append(pg.image.load(os.path.join(img_folder, 'bullet' + str(i) + '.png')).convert())

asteroid_img = []
for i in range(4):
    asteroid_img.append(pg.transform.scale(pg.image.load(os.path.join(img_folder, 'asteroid' + str(i) + '.png')).convert(), (20 * (i + 1), 20 * (i + 1))))

enemy_img = []

for i in range(3):
    enemy_group = []
    for j in range(3):
        enemy_group.append(pg.transform.scale(pg.image.load(os.path.join(img_folder, 'enemy' + str(i) + str(j) + '.png')).convert(), (50, 50)))

    enemy_img.append(enemy_group)

select_snd = pg.mixer.Sound(os.path.join(snd_folder, 'select.wav'))
shoot_snd = pg.mixer.Sound(os.path.join(snd_folder, 'shoot.wav'))
heal_snd = pg.mixer.Sound(os.path.join(snd_folder, 'heal.wav'))
pwrup_snd = pg.mixer.Sound(os.path.join(snd_folder, 'pwrup.wav'))
alert_snd = pg.mixer.Sound(os.path.join(snd_folder, 'alert.wav'))
menu_music = pg.mixer.Sound(os.path.join(snd_folder, 'menu_music.wav'))
music = pg.mixer.Sound(os.path.join(snd_folder, 'music.wav'))

expl_sounds = []
for snd in ['expl1.wav', 'expl2.wav']:
    expl_sounds.append(pg.mixer.Sound(os.path.join(snd_folder, snd)))


save_path = os.path.join(user_folder, 'save.txt')
config_path = os.path.join(user_folder, 'config.txt')

lvl0 = 'asteroid'

lvl1 = '011101110n' \
      '111111111n' \
      '011111110n' \
      '001111100n' \
      '000111000n' \
      '000010000'

lvl2 = '111111111n' \
       '111111111n' \
       '111111111'

lvl3 = '101010101n' \
       '010101010n' \
       '101010101n' \
       '010101010n' \
       '101010101'

lvl4 = '100010111n' \
       '100010010n' \
       '111110010n' \
       '100010010n' \
       '100010111'

lvl5 = '011000110n' \
       '100001001n' \
       '111000111n' \
       '100100001n' \
       '011000110'

lvl6 = '000111000n' \
       '001101100n' \
       '001000100n' \
       '000111000n' \
       '000111000'

lvl7 = '000111000n' \
       '111111111n' \
       '011111110n' \
       '001111100n' \
       '001101100'

lvl8 = '100000001n' \
       '010000010n' \
       '001000100n' \
       '000101000n' \
       '000010000'

lvl9 = '111111111n' \
       '000000001n' \
       '111111111n' \
       '100000000n' \
       '111111111'

lvl10 = '111111111n' \
       '100000000n' \
       '111111111n' \
       '000000001n' \
       '111111111'

lvls = []
lvls.append(lvl0)
lvls.append(lvl1)
lvls.append(lvl2)
lvls.append(lvl3)
lvls.append(lvl4)
lvls.append(lvl5)
lvls.append(lvl6)
lvls.append(lvl7)
lvls.append(lvl8)
lvls.append(lvl9)
lvls.append(lvl10)

data_elem = {
    'name': 'player',
    'score': 0
}

name = ''
score = 0
powerups = 0
type_symbols = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m", "й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "ё"}

with open(config_path) as config_file:
    config = json.load(config_file)

with open(save_path) as save_file:
    save_data = json.load(save_file)

volume = config['volume']
controls = config['controls']

##########################################


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.75)/2)
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

        if keystate[pg.key.key_code(controls['up'])]:
            self.speedy = -10

        if keystate[pg.key.key_code(controls['left'])]:
            self.speedx = -10

        if keystate[pg.key.key_code(controls['down'])]:
            self.speedy = 10

        if keystate[pg.key.key_code(controls['right'])]:
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

            state = 0
            if player.dmg >= 300:
                state = 3
            elif player.dmg >= 200:
                state = 2
            elif player.dmg >= 100:
                state = 1

            bullet = Bullet(self.rect.centerx, self.rect.top, state)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_snd.play()


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, type, color):
        pg.sprite.Sprite.__init__(self)
        self.image = enemy_img[type][color]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = -500
        self.y = y
        self.radius = int((self.rect.width * 0.85) / 2)
        self.last_update = pg.time.get_ticks()
        self.shoot_delay = 1000 - int(score * 0.05)
        if self.shoot_delay <= 350:
            self.shoot_delay = 350
        self.health = 50 + int(0.15 * score)
        self.dmg = 30

    def update(self):
        if self.y - self.rect.top >= 5:
            self.rect.top += 5
        else:
            self.rect.top = self.y

        if self.rect.top == self.y:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.shoot_delay:
            self.last_update = now
            if random.random() > 0.9:
                ebullet = EnemyBullet(self.rect.centerx, self.rect.top)
                all_sprites.add(ebullet)
                ebullets.add(ebullet)
                shoot_snd.play()


class Asteroid(pg.sprite.Sprite):
    def __init__(self, k):
        pg.sprite.Sprite.__init__(self)
        self.type = random.randrange(0, 4)
        self.image_orig = asteroid_img[self.type]
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.85) / 2)
        self.rect.x = random.randrange(PLAYZONE_WIDTH - self.rect.width)
        self.rect.y = - (500 + 400 * k + random.randrange(20, 200))
        self.speedy = random.randrange(4, 6)
        self.rotation = 0
        self.rotation_speed = random.randrange(-5, 5)
        self.last_update = pg.time.get_ticks()
        self.health = 25 * self.type + int(score * 0.05)
        self.dmg = 10 * (self.type + 1)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


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
    def __init__(self, x, y, state):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img[state]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = ebullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


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

##########################################


def draw_text(surf, color, text, size, x, y, pos):
    font = pg.font.Font(os.path.join(fonts_folder, 'OutlinePixel7.ttf'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if pos == 'topleft':
        text_rect.topleft = (x, y)
    elif pos == 'center':
        text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)


def new_asteroid(k):
    m = Asteroid(k)
    all_sprites.add(m)
    mobs.add(m)


def new_enemy(x, y, type, color):
    e = Enemy(x, y, type, color)
    all_sprites.add(e)
    mobs.add(e)


def draw_health_bar(surf, x, y, health):
    if health < 0:
        health = 0
    color = (0, 200, 0)
    if health <= 30:
        color = (196, 0, 5)
    length = 520
    height = 26
    fill = (health / 100) * length
    outline_rect = pg.Rect(x, y, length, height)
    fill_rect = pg.Rect(x, y, fill, height)
    pg.draw.rect(surf, color, fill_rect)
    pg.draw.rect(surf, color, outline_rect, 2)


def build_lvl(lvl):
    x = 25
    y = 25
    type = random.randrange(0, 3)
    color = random.randrange(0, 3)
    for i in lvl:
        if i == '1':
            new_enemy(x, y, type, color)
        x += 72
        if i == 'n':
            y += 72
            x = 25
            type = random.randrange(0, 3)
            color = (color + 1) % 3


def asteroid_lvl():
    count = 0
    while count < 16:
        for i in range(12):
            new_asteroid(count)
        count += 1


def update_master_volume():
    global volume
    expl_volume = 0.5
    shoot_volume = 0.25
    select_volume = 0.5

    alert_snd.set_volume(volume/100)
    heal_snd.set_volume(volume/100)
    pwrup_snd.set_volume(volume/100)
    shoot_snd.set_volume(shoot_volume * volume/100)
    select_snd.set_volume(select_volume * volume/100)
    for i in range(len(expl_sounds)):
        expl_sounds[i].set_volume(expl_volume * volume/100)
    pg.mixer.music.set_volume(volume/100)


def show_save():
    global name
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill(BLACK)
    surf_rect = surf.get_rect()
    screen.blit(surf, surf_rect)
    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
    draw_text(screen, WHITE, "Введите имя:", 36, WIDTH / 2, HEIGHT / 4 + 100, 'center')
    draw_text(screen, WHITE, name, 36, WIDTH / 2, HEIGHT / 4 + 150, 'center')

    pg.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.blit(surf, surf_rect)
        draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
        draw_text(screen, WHITE, "Введите имя:", 36, WIDTH / 2, HEIGHT / 4 + 100, 'center')
        draw_text(screen, WHITE, name, 36, WIDTH / 2, HEIGHT / 4 + 150, 'center')
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                keystate = pg.key.get_pressed()
                if keystate[pg.K_SPACE]:
                    select_snd.play()

                    data_elem['name'] = name
                    data_elem['score'] = score
                    save_data['data'].append(data_elem)

                    n = len(save_data['data'])
                    for i in range(n - 1):
                        for j in range(n - i - 1):
                            if save_data['data'][j]['score'] < save_data['data'][j + 1]['score']:
                                save_data['data'][j], save_data['data'][j + 1] = save_data['data'][j + 1], save_data['data'][j]

                    with open(save_path, 'w') as save_file:
                        json.dump(save_data, save_file)

                    draw_text(screen, WHITE, "Сохранено!", 36, WIDTH / 2, HEIGHT * 3/4, 'center')
                    pg.display.flip()

                    start = pg.time.get_ticks()
                    while True:
                        now = pg.time.get_ticks()
                        if now - start > 1000:
                            break

                    waiting = False
                elif keystate[pg.K_BACKSPACE]:
                    select_snd.play()
                    name = name[:-1]
                elif len(name) < 8 and event.unicode in type_symbols:
                    select_snd.play()
                    name += event.unicode


def show_gameover():
    options = ['Да', 'Нет']
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill(BLACK)
    surf_rect = surf.get_rect()
    screen.blit(surf, surf_rect)
    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
    draw_text(screen, WHITE, "Ваш счет: " + str(score), 36, WIDTH / 2, HEIGHT / 4 + 100, 'center')
    draw_text(screen, WHITE, "Сохранить?", 36, WIDTH / 2, HEIGHT / 4 + 150, 'center')
    draw_text(screen, GREEN, options[0], 36, WIDTH / 2 - 100, HEIGHT / 4 + 200, 'center')
    draw_text(screen, WHITE, options[1], 36, WIDTH / 2 + 100, HEIGHT / 4 + 200, 'center')

    pg.display.flip()

    option = 0
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                keystate = pg.key.get_pressed()
                if keystate[pg.K_SPACE]:
                    select_snd.play()
                    if options[option] == 'Да':
                        show_save()
                    waiting = False

                if keystate[pg.K_a]:
                    if option == 1:
                        draw_text(screen, WHITE, options[option], 36, WIDTH / 2 + 100, HEIGHT / 4 + 200, 'center')
                        draw_text(screen, GREEN, options[option - 1], 36, WIDTH / 2 - 100, HEIGHT / 4 + 200, 'center')

                    option = 0

                    pg.display.flip()
                    select_snd.play()

                if keystate[pg.K_d]:
                    if option == 0:
                        draw_text(screen, GREEN, options[option + 1], 36, WIDTH / 2 + 100, HEIGHT / 4 + 200, 'center')
                        draw_text(screen, WHITE, options[option], 36, WIDTH / 2 - 100, HEIGHT / 4 + 200, 'center')

                    option = 1

                    pg.display.flip()
                    select_snd.play()


def show_controls():
    options = ['Вверх: ', 'Вниз: ', 'Влево: ', 'Вправо: ', 'Назад']
    controls_names = ['up', 'down', 'left', 'right']
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill(BLACK)
    surf_rect = surf.get_rect()
    screen.blit(surf, surf_rect)
    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
    draw_text(screen, GREEN, options[len(options) - 1], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (len(options)), 'center')

    for i in range(0, len(options) - 1):
        draw_text(screen, WHITE, options[i] + controls[controls_names[i]], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1), 'center')

    pg.display.flip()

    option = len(options) - 1
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                keystate = pg.key.get_pressed()
                if keystate[pg.K_SPACE]:
                    select_snd.play()
                    if options[option] == 'Назад':
                        waiting = False
                    else:
                        screen.blit(surf, surf_rect)
                        draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
                        draw_text(screen, WHITE, options[len(options) - 1], 36, WIDTH / 2,
                                  HEIGHT / 4 + 100 + 50 * (len(options)), 'center')

                        for i in range(0, len(options) - 1):
                            if i == option:
                                continue
                            draw_text(screen, WHITE, options[i] + controls[controls_names[i]], 36, WIDTH / 2,
                                      HEIGHT / 4 + 100 + 50 * (i + 1), 'center')

                        draw_text(screen, WHITE, options[option] + ' ', 36, WIDTH / 2,
                                  HEIGHT / 4 + 100 + 50 * (option + 1), 'center')

                        draw_text(screen, WHITE, "Нажмите клавишу...", 36, WIDTH / 2, HEIGHT - 100, 'center')
                        pg.display.flip()

                        waiting_key = True
                        while waiting_key:
                            clock.tick(FPS)
                            for event in pg.event.get():
                                if event.type == pg.QUIT:
                                    pg.quit()
                                    sys.exit(0)

                                if event.type == pg.KEYDOWN:
                                    controls[controls_names[option]] = pg.key.name(event.key)
                                    waiting_key = False

                        config['controls'] = controls
                        with open(config_path, 'w') as config_file:
                            json.dump(config, config_file)

                        screen.blit(surf, surf_rect)
                        draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
                        draw_text(screen, WHITE, options[len(options) - 1], 36, WIDTH / 2,
                                  HEIGHT / 4 + 100 + 50 * (len(options)), 'center')

                        for i in range(0, len(options) - 1):
                            if i == option:
                                continue
                            draw_text(screen, WHITE, options[i] + controls[controls_names[i]], 36, WIDTH / 2,
                                      HEIGHT / 4 + 100 + 50 * (i + 1), 'center')

                        draw_text(screen, GREEN, options[option] + controls[controls_names[option]], 36, WIDTH / 2,
                                  HEIGHT / 4 + 100 + 50 * (option + 1), 'center')

                        pg.display.flip()

                if keystate[pg.K_s]:
                    if option == len(options) - 1:
                        draw_text(screen, WHITE, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    else:
                        draw_text(screen, WHITE, options[option] + controls[controls_names[option]], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    option += 1
                    if option > len(options) - 1:
                        option = len(options) - 1

                    if option == len(options) - 1:
                        draw_text(screen, GREEN, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1),
                                  'center')
                    else:
                        draw_text(screen, GREEN, options[option] + controls[controls_names[option]], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')

                    pg.display.flip()
                    select_snd.play()

                if keystate[pg.K_w]:
                    if option == len(options) - 1:
                        draw_text(screen, WHITE, options[option], 36, WIDTH / 2,
                                  HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    else:
                        draw_text(screen, WHITE, options[option] + controls[controls_names[option]], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    option -= 1
                    if option < 0:
                        option = 0
                    draw_text(screen, GREEN, options[option] + controls[controls_names[option]], 36, WIDTH / 2,
                              HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    pg.display.flip()
                    select_snd.play()


def show_options():
    global volume
    options = ['Громкость: ', 'Управление', 'Сбросить рекорды', 'Назад']
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill(BLACK)
    surf_rect = surf.get_rect()
    screen.blit(surf, surf_rect)
    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
    draw_text(screen, GREEN, options[len(options) - 1], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (len(options)), 'center')
    for i in range(0, len(options) - 1):
        if options[i] == 'Громкость: ':
            draw_text(screen, WHITE, options[i] + str(volume), 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1), 'center')
        else:
            draw_text(screen, WHITE, options[i], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1), 'center')

    pg.display.flip()

    option = len(options) - 1
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                keystate = pg.key.get_pressed()
                if keystate[pg.K_SPACE]:
                    select_snd.play()
                    match options[option]:
                        case 'Управление':
                            show_controls()
                            screen.blit(surf, surf_rect)
                            draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
                            draw_text(screen, GREEN, options[len(options) - 1], 36, WIDTH / 2,
                                      HEIGHT / 4 + 100 + 50 * (len(options)), 'center')
                            for i in range(0, len(options) - 1):
                                if options[i] == 'Громкость: ':
                                    draw_text(screen, WHITE, options[i] + str(volume), 36, WIDTH / 2,
                                              HEIGHT / 4 + 100 + 50 * (i + 1), 'center')
                                else:
                                    draw_text(screen, WHITE, options[i], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1),
                                              'center')

                            pg.display.flip()
                            option = len(options) - 1

                        case 'Сбросить рекорды':

                            save_data = {
                                'data': []
                            }

                            with open(save_path, 'w') as save_file:
                                json.dump(save_data, save_file)

                            with open(save_path) as save_file:
                                save_data = json.load(save_file)

                        case 'Назад':
                            config['volume'] = volume
                            with open(config_path, 'w') as config_file:
                                json.dump(config, config_file)
                            waiting = False

                if keystate[pg.K_a] and option == 0:
                    volume -= 10
                    if volume < 0:
                        volume = 0

                    update_master_volume()

                    screen.blit(surf, surf_rect)
                    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
                    draw_text(screen, GREEN, options[option] + str(volume), 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    for i in range(1, len(options)):
                        draw_text(screen, WHITE, options[i], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1), 'center')
                    pg.display.flip()
                    select_snd.play()

                if keystate[pg.K_d] and option == 0:
                    volume += 10
                    if volume > 100:
                        volume = 100

                    update_master_volume()

                    screen.blit(surf, surf_rect)
                    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
                    draw_text(screen, GREEN, options[option] + str(volume), 36, WIDTH / 2,
                              HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    for i in range(1, len(options)):
                        draw_text(screen, WHITE, options[i], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1), 'center')
                    pg.display.flip()
                    select_snd.play()

                if keystate[pg.K_s]:
                    if options[option] == 'Громкость: ':
                        draw_text(screen, WHITE, options[option] + str(volume), 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    else:
                        draw_text(screen, WHITE, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    option += 1
                    if option > len(options) - 1:
                        option = len(options) - 1
                    draw_text(screen, GREEN, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    pg.display.flip()
                    select_snd.play()

                if keystate[pg.K_w]:
                    if options[option] == 'Громкость: ':
                        draw_text(screen, WHITE, options[option] + str(volume), 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    else:
                        draw_text(screen, WHITE, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    option -= 1
                    if option < 0:
                        option = 0
                    if options[option] == 'Громкость: ':
                        draw_text(screen, GREEN, options[option] + str(volume), 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    else:
                        draw_text(screen, GREEN, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    pg.display.flip()
                    select_snd.play()


def show_rules():
    rules = ['Правила игры',
             'Игрок управляет космическим судном. Противниками',
             'выступают вражеские космические корабли и астероиды.',
             'Игрок может управлять положением персонажа при по-',
             'мощи клавиш на клавиатуре (по умолчанию W, A, S, D).',
             'Задача игрока - уклоняться от вражеских атак и унич-',
             'тожать врагов при помощи стрельбы. Целью игры является',
             'набор максимального количества очков. За каждого',
             'убитого врага начисляется 20 очков. На месте гибели',
             'врагов могут появляться аптечки и усиления. Изначаль-',
             'ное количество ОЗ игрока равно 100. Аптечки восстанав-',
             'ливают ОЗ при подборе, усиления увеличивают урон кос-',
             'мического корабля игрока. Количество ОЗ противников',
             'зависит от набранных игроком очков.']

    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill(BLACK)
    surf_rect = surf.get_rect()
    screen.blit(surf, surf_rect)
    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
    for i in range(len(rules)):
        draw_text(screen, WHITE, rules[i], 24, WIDTH / 2, HEIGHT / 4 + 48 + 24 * (i + 1), 'center')

    draw_text(screen, GREEN, "Назад", 36, WIDTH / 2, HEIGHT - 100, 'center')

    pg.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                keystate = pg.key.get_pressed()
                if keystate[pg.K_SPACE]:
                    select_snd.play()
                    waiting = False


def show_menu():
    options = ['Играть', 'Настройки', 'Правила', 'Выход']
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill(BLACK)
    surf_rect = surf.get_rect()
    screen.blit(surf, surf_rect)
    draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
    draw_text(screen, GREEN, options[0], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50, 'center')
    for i in range(1, len(options)):
        draw_text(screen, WHITE, options[i], 36, WIDTH/2, HEIGHT/4 + 100 + 50*(i + 1), 'center')

    pg.display.flip()

    option = 0
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                keystate = pg.key.get_pressed()
                if keystate[pg.K_SPACE]:
                    select_snd.play()
                    match options[option]:
                        case 'Играть':
                            waiting = False

                        case 'Настройки':
                            show_options()
                            screen.blit(surf, surf_rect)
                            option = 0
                            draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
                            draw_text(screen, GREEN, options[0], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50, 'center')
                            for i in range(1, len(options)):
                                draw_text(screen, WHITE, options[i], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1), 'center')
                            pg.display.flip()

                        case 'Правила':
                            show_rules()
                            screen.blit(surf, surf_rect)
                            option = 0
                            draw_text(screen, WHITE, "Star Defender", 64, WIDTH / 2, HEIGHT / 4, 'center')
                            draw_text(screen, GREEN, options[0], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50, 'center')
                            for i in range(1, len(options)):
                                draw_text(screen, WHITE, options[i], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (i + 1), 'center')
                            pg.display.flip()

                        case 'Выход':
                            waiting = False
                            pg.quit()
                            sys.exit(0)


                if keystate[pg.K_s]:
                    draw_text(screen, WHITE, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    option += 1
                    if option > len(options) - 1:
                        option = len(options) - 1
                    draw_text(screen, GREEN, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    pg.display.flip()
                    select_snd.play()

                if keystate[pg.K_w]:
                    draw_text(screen, WHITE, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    option -= 1
                    if option < 0:
                        option = 0
                    draw_text(screen, GREEN, options[option], 36, WIDTH / 2, HEIGHT / 4 + 100 + 50 * (option + 1), 'center')
                    pg.display.flip()
                    select_snd.play()

##########################################


update_master_volume()

game_stop = True
running = True
while running:
    if game_stop:
        pg.mixer.music.stop()
        pg.mixer.music = menu_music
        pg.mixer.music.play(loops=-1)
        update_master_volume()

        show_menu()

        score = 0
        powerups = 0

        all_sprites = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)

        mobs = pg.sprite.Group()
        bullets = pg.sprite.Group()
        ebullets = pg.sprite.Group()
        drops = pg.sprite.Group()

        pg.mixer.music.stop()
        pg.mixer.music = music
        pg.mixer.music.play(loops=-1)
        update_master_volume()

        build_lvl(lvl4)
        game_stop = False

    clock.tick(FPS)
    all_sprites.update()

    hits = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.dmg
        explosion = Explosion(hit.rect.center, 'small')
        all_sprites.add(explosion)
        random.choice(expl_sounds).play()
        alert_snd.play()
        if player.health <= 0:
            death_explosion = Explosion(player.rect.center, 'large')
            all_sprites.add(death_explosion)
            random.choice(expl_sounds).play()
            player.kill()

    hits = pg.sprite.spritecollide(player, ebullets, True, pg.sprite.collide_circle)
    for hit in hits:
        player.health -= 31
        explosion = Explosion(hit.rect.center, 'small')
        all_sprites.add(explosion)
        random.choice(expl_sounds).play()
        alert_snd.play()
        if player.health <= 0:
            death_explosion = Explosion(player.rect.center, 'large')
            all_sprites.add(death_explosion)
            random.choice(expl_sounds).play()
            player.kill()

    if not player.alive() and not death_explosion.alive():
        show_gameover()
        game_stop = True

    hits = pg.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        hit.health -= player.dmg
        if hit.health <= 0:
            explosion = Explosion(hit.rect.center, 'large')
            all_sprites.add(explosion)
            random.choice(expl_sounds).play()
            hit.kill()
            score += 20
            if random.random() > 0.85:
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

    if not bool(mobs):
        lvl = random.randrange(0, len(lvls))
        if lvl == 0:
            asteroid_lvl()
        else:
            build_lvl(lvls[lvl])

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(BLACK)
    bg_rect.centery += 1
    if bg_rect.centery == HEIGHT:
        bg_rect.centery = 0
    screen.blit(bg_img, bg_rect)
    all_sprites.draw(screen)
    draw_text(screen, WHITE,  "Счет: " + str(score), 52, PLAYZONE_WIDTH + 20, 20, 'topleft')
    draw_text(screen, WHITE, "Урон: " + str(player.dmg), 52, PLAYZONE_WIDTH + 20, 72, 'topleft')
    draw_text(screen, WHITE, "Рекорды:", 52, PLAYZONE_WIDTH + 20, 124, 'topleft')

    with open(save_path) as save_file:
        save_data = json.load(save_file)

    items = len(save_data['data'])
    if items > 12:
        items = 12
    for i in range(items):
        record_name = save_data['data'][i]['name']
        record_score = save_data['data'][i]['score']
        spacing = 21 - len(record_name) - len(str(record_score))
        draw_text(screen, WHITE, record_name + '.' * spacing + str(record_score), 36, PLAYZONE_WIDTH + 20, 176 + 36 * i, 'topleft')

    draw_text(screen, WHITE, "Здоровье:", 52, PLAYZONE_WIDTH + 20, HEIGHT - 98, 'topleft')

    draw_health_bar(screen, PLAYZONE_WIDTH + 20, HEIGHT - 46, player.health)
    pg.display.flip()

pg.quit()
