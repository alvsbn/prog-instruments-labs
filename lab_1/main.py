import os
import random

import pygame
from pygame import RLEACCEL, KEYDOWN


pygame.init()

size = WIDTH, HEIGHT = (600, 150)
win = pygame.display.set_mode(size)
pygame.display.set_caption("Dino Run")

black = (0, 0, 0)
white = (255, 255, 255)
background_col = (235, 235, 235)

jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')

high_score = 0
FPS = 60
gravity = 0.6

clock = pygame.time.Clock()


def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('.', 'sprites', name)
    image = pygame.image.load(fullname).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())


def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex=-1,
        scaley=-1,
        colorkey=None,
        ):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width / nx
    sizey = sheet_rect.height / ny

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j * sizex, i * sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


def extractDigits(number):
    if number > -1:
        digits = []

        while(number / 10 != 0):
            digits.append(number % 10)
            number = int(number / 10)

        digits.append(number % 10)
        for i in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits


class Ground():
    def __init__(self, sizex=-1, sizey=-1, speed=-5):
        self.image, self.rect = load_image(
            "ground.png", sizex, sizey, -1)
        self.image1, self.rect1 = load_image(
            "ground.png", sizex, sizey, -1)
        self.rect.left = 0
        self.rect1.left = self.rect.right
        self.rect.bottom = HEIGHT
        self.rect1.bottom = HEIGHT
        self.speed = speed

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed
        if self.rect.right <= 0:
            self.rect.left = self.rect1.right
        elif self.rect1.right <= 0:
            self.rect1.left = self.rect.right

    def draw(self):
        win.blit(self.image, self.rect)
        win.blit(self.image1, self.rect1)
        self.update()


class Cloud:
    def __init__(self, x_pos, y_pos=random.randrange(0, 60), speed=-2):
        self.image, self.rect = load_image(
            'cloud.png', int(90 * 30 / 42), 30, -1)
        self.rect.left = x_pos
        self.rect.top = y_pos
        self.speed = speed

    def draw(self):
        win.blit(self.image, self.rect)

    def update(self):
        self.rect.left += self.speed


def collide(obj1, obj2):
    offset_x = int(obj2.rect.left - obj1.rect.left)
    offset_y = int(obj2.rect.top - obj1.rect.top)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Dino(pygame.sprite.Sprite):
    def __init__(self, sizex=-1, sizey=-1):
        self.images, self.rect = load_sprite_sheet(
            "dino.png", 5, 1, sizex, sizey, -1)
        self.images1, self.rect1 = load_sprite_sheet(
            "dino_ducking.png", 2, 1, sizex, sizey, -1)
        self.isJump = False
        self.isDuck = False
        self.isDead = False
        self.rect.left = WIDTH / 15
        self.rect.bottom = int(0.98 * HEIGHT)
        self.standing_pos = self.images[0]
        self.ducking_pos = self.images1[0]
        self.jumpCount = 17
        self.neg = -1
        self.mask = pygame.mask.from_surface(self.image())

    def update(self):
        if self.isJump:
            if self.jumpCount == 0:
                jump_sound.play()
                self.neg = 1
            self.rect.bottom += (self.jumpCount**2) * 0.05 * self.neg
            self.jumpCount -= 1
            if self.jumpCount <= -17:
                self.jumpCount = 17
                self.neg = -1
                self.isJump = False
                self.rect.bottom = int(0.98 * HEIGHT)

    def draw(self):
        self.update()
        win.blit(self.image(), self.rect)

    def image(self):
        if self.isDead:
            return self.images[4]
        elif self.isJump:
            if self.isDuck:
                return self.images1[0]
            else:
                return  self.images[0]
        elif self.isDuck:
            if pygame.time.get_ticks() % 125 >= 62:
                return  self.images1[0]
            else:
                return self.images1[1]
        else:
            if pygame.time.get_ticks() % 125 >= 62:
                return  self.images[2]
            else:
                return self.images[3]


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=-5, sizex=-1, sizey=-1):
        self.images1, self.rect1 = load_sprite_sheet(
            "cacti-small.png", 6, 1, sizex, sizey, -1)
        self.images2, self.rect2 = load_sprite_sheet(
            "cacti-small.png", 3, 1, sizex, sizey, -1)
        self.images3, self.rect3 = load_sprite_sheet(
            "cacti-big.png", 3, 1, 50, 50, -1)
        self.images4, self.rect4 = load_sprite_sheet(
            "cacti-small.png", 2, 1, 50, sizey, -1)
        self.speed = speed
        self.image, self.rect = self.image()
        self.rect.left = WIDTH
        self.rect.bottom = int(0.98 * HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.left += self.speed

    def draw(self):
        self.update()
        win.blit(self.image, self.rect)

    def image(self):
        ch = random.randint(0, 3)
        if ch == 0:
            return (self.images1[random.randint(0, 5)], self.rect1)
        elif ch == 1:
            return (self.images2[random.randint(0, 2)], self.rect2)
        elif ch == 2:
            return (self.images3[random.randint(0, 2)], self.rect3)
        elif ch == 3:
            return (self.images4[random.randint(0, 1)], self.rect4)


class Ptera(pygame.sprite.Sprite):
    def __init__(self, speed=-5):
        self.images, self.rect = load_sprite_sheet(
            "ptera.png", 2, 1, 46, 40, -1)
        self.rect.left = WIDTH
        self.rect.bottom = random.randrange(40, 130)
        self.speed = speed

        self.mask = pygame.mask.from_surface(self.image())

    def update(self):
        self.rect.left += self.speed

    def draw(self):
        self.update()
        win.blit(self.image(), self.rect)

    def image(self):
        if pygame.time.get_ticks() % 125 >= 62:
            return  self.images[0]
        else:
            return self.images[1]


class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet(
            'numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = WIDTH * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = HEIGHT * 0.1
        else:
            self.rect.top = y

    def draw(self):
        win.blit(self.image, self.rect)

    def update(self, score):
        score_digits = extractDigits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0


high_score_flag = False
last_score = 0
highsc = Scoreboard(WIDTH * 0.78)
temp_images, temp_rect = load_sprite_sheet(
    'numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
HI_image = pygame.Surface((22,int(11 * 6 / 5)))
HI_rect = HI_image.get_rect()
HI_image.fill(background_col)
HI_image.blit(temp_images[10], temp_rect)
temp_rect.left += temp_rect.width
HI_image.blit(temp_images[11], temp_rect)
HI_rect.top = HEIGHT * 0.1
HI_rect.left = WIDTH * 0.73


def main():
    global high_score, high_score_flag, HI_image, HI_rect, highsc, last_score
    run = True
    ground = Ground()
    dino = Dino(44, 47)
    frame_clock = 0
    cactuslist = []
    clouds = []
    ptera = []
    scb = Scoreboard()

    while run:
        win.fill(background_col)
        ground.draw()
        clock.tick(FPS)
        score = frame_clock / 30
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                dino.isDuck = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            dino.isJump = True
        if keys[pygame.K_DOWN]:
            dino.isDuck = True

        if not (frame_clock % 90):
            obj_probality = random.randint(0, 5)
            if obj_probality == 1:
                ptera.insert(0, Ptera())
            else:
                cactuslist.insert(0, Cactus(-5, 40, 40))

#-------------------Clouds-------------------------------
        obj_probality = random.randint(0, 120)
        if obj_probality == 1:
            obj = Cloud(random.randrange(
                WIDTH, WIDTH + WIDTH / 2))
            clouds.append(obj)
        for obj in clouds:
            obj.draw()
            obj.update()
            if obj.rect.right < 0:
                clouds.remove(obj)

#--------------------Cactus------------------------------
        for cact in cactuslist:
            cact.draw()
            if cact.rect.left < 0:
                cactuslist.pop()
            if collide(dino, cact):
                high_score_flag = True
                die_sound.play()
                run = False
                dino.isDead = True
                last_score = score

#--------------------Ptera-------------------------------
        for bird in ptera:
            bird.draw()
            if bird.rect.left < 0:
                ptera.pop()
            if collide(dino, bird):
                high_score_flag = True
                die_sound.play()
                run = False
                dino.isDead = True
                last_score = score

#-----------------highScore------------------------------
        if high_score_flag == True:
            if high_score < score:
                high_score = score
                highsc.update(int(high_score))
            if  score == last_score and dino.isDead == False:
                checkPoint_sound.play()

            win.blit(HI_image, HI_rect)
            highsc.draw()

#--------------------------------------------------------
        scb.update(int(score))
        scb.draw()
        dino.draw()
        frame_clock += 1
        pygame.display.flip()

    gameover, gameover_rect = load_image("game_over.png", 200, 15, -1)
    gameover_rect.left = WIDTH / 2 - gameover_rect.width / 2
    gameover_rect.top = HEIGHT / 2 - gameover_rect.height * 2
    win.blit(gameover, gameover_rect)
    replay, replay_rect = load_image("replay_button.png", 30, 30, -1)
    replay_rect.left = WIDTH / 2 - replay_rect.width / 2
    replay_rect.top = HEIGHT / 2
    win.blit(replay, replay_rect)
    pygame.display.flip()
    pygame.time.delay(2000)


win.fill(white)
logo, logo_rect = load_image("logo.png", 300, 140, -1)
logo_rect.centerx = WIDTH * 0.6
logo_rect.centery = HEIGHT * 0.6
temp_ground, temp_ground_rect = load_sprite_sheet(
    "ground.png", 15, 1, -1, -1, -1)
temp_ground_rect.left = WIDTH / 20
temp_ground_rect.bottom = HEIGHT
temp_dino = Dino(44, 47)
win.blit(temp_dino.standing_pos, temp_dino.rect)
win.blit(temp_ground[0], temp_ground_rect)
win.blit(logo, logo_rect)
pygame.display.flip()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if (event.key == pygame.K_SPACE or
                event.key == pygame.K_RETURN):
                main()
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if (event.key ==  pygame.K_SPACE or
                        event.key == pygame.K_RETURN):
                        run = True

pygame.quit()
