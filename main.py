import pygame
import random
import math
import time
# from shuffleimages import shuffle
from pygame import mixer
from enum import Enum


# class(Enum)ปกด.nameกับvalue ใช้ใน random_animal()
class Type(Enum):
    BOMB = 0
    CAT = 1
    DOG = 2
    DOG_SICK = 3


class Animal:
    def __init__(self, height):
        self.location_x = random.randint(100, 700)  # สุ่มตน.xที่จะตก
        self.location_y = height  # ตน.yที่สัตว์จะตก
        self.location_x_change = 0
        self.location_y_change = 2.5  # ความเร็วสัตว์ตก
        self.img = pygame.image.load(self.get_img())
        self.score = self.get_score()

    def get_img(self):
        images = ['assets/cat.png', 'assets/dog.png']
        return images[random.randint(0, 1)] #return str

    def get_score(self):
        return 1


class Bomb(Animal):
    def __init__(self, height):
        super().__init__(height)
        self.location_y_change = 3.5  # ความเร็วสัตว์ตก
        self.img = pygame.image.load(self.get_img())
        self.score = self.get_score()

    def get_img(self):
        images = 'assets/bomb.png'
        return images

    def get_score(self):
        return 0


class SickAnimal(Animal):
    def __init__(self, height):
        super().__init__(height)
        self.img = pygame.image.load(self.get_img())
        self.score = self.get_score()

    def get_img(self):
        images = 'assets/dog-yellow.png'
        return images

    def get_score(self):
        return -2


class Player:
    def __init__(self):
        self.img = pygame.image.load('assets/basket.png')
        self.location_x = 350
        self.location_y = 480
        self.location_x_change = 0


# Initialize the pygame # เซทค่าเริ่มต้นเกม
pygame.init()

# Set game screen # เซทหน้าจอเกมกว้าง,สูงพิกเซล
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/sky.jpg')

# Background sound
mixer.music.load('assets/GameMusicTheme.wav')
mixer.music.play(-1)

# Title and Icon เริ่มมีเสียงเกม
pygame.display.set_caption("Raining Cats and Dogs")  # ชื่อเกมที่จะแสดงบนแถบ

icon = pygame.image.load('assets/rain.png')  # กำหนดตัวแปรเพื่อโหลดรูปที่จะแสดงบนไอคอน
pygame.display.set_icon(icon)  # แสดงรูปบนไอคอน

# PLAYER
# Position basket at bottom centre
player = Player()

# CAT/DOG
total_animal_rain = 2
animals = []
height = 0


def random_animal(height):
    animal_type = random.randint(0, 3)
    if animal_type == Type.BOMB.value:
        animal = Bomb(height)  # สร้าง
    elif animal_type == Type.DOG_SICK.value:
        animal = SickAnimal(height)
    else:
        animal = Animal(height)
    return animal


for i in range(total_animal_rain):
    animal = random_animal(height)
    animals.append(animal)  # เอา animal ที่สุ่มได้ใส่ลงไปใน []

    height += 200


def render_player(player):
    # blit(image, coordinates) to print player onto game screen
    # screen.blit(playerImg, (x, y))
    screen.blit(player.img, (player.location_x, player.location_y))


def render_animal(animal):
    # blit(image, coordinates) to print animal onto game screen
    screen.blit(animal.img, (animal.location_x, animal.location_y))


def isCollision(animal, player):
    # distance = math.sqrt(math.pow(animal.location_x - playerX, 2) + math.pow(animal.location_y - playerY, 2))
    distance = math.sqrt(math.pow(animal.location_x - player.location_x, 2) + math.pow(animal.location_y - player.location_y, 2))

    x_distance = abs(player.location_x - animal.location_x)  # หาระยะห่างของตะกร้ากับสัตว์
    y_distance = abs(player.location_y - animal.location_y)

    if distance < 60: #ระยะระหว่าง animal กับ player
        return True  #ชนกัน
    elif x_distance < 80 and y_distance < 40:
        return True
    else:
        return False  # ไม่ชนตะกร้า


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 40)
textX = 10
textY = 10


def showScore(x, y):
    score = font.render("SCORE: " + str(score_value), True, (10, 10, 10))
    screen.blit(score, (x, y))


# Time
startTime = time.time()


def showTime(time):
    minutes = time // 60
    seconds = time % 60

    if seconds < 10:
        time = font.render("TIME " + str(minutes) + ":0" + str(seconds), True, (10, 10, 10))
    else:
        time = font.render("TIME " + str(minutes) + ":" + str(seconds), True, (10, 10, 10))
    screen.blit(time, (10, 50))


# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    gameover_sound = mixer.Sound('assets/GameOver.flac')
    gameover_sound.play()
    for i in range(total_animal_rain):
        animals[i].location_y = 2000  # สัตว์ตกลงไปแล้ว


def game_over_text():
    text = over_font.render("GAME OVER", True, (10, 10, 10))
    screen.blit(text, (200, 380))
    mixer.music.stop()


# Press any key to start
press_font = pygame.font.Font('freesansbold.ttf', 48)

# Game loop
wait = True
running = True

while wait:
    # Background (R,G,B)
    screen.fill((26, 152, 201))
    screen.blit(background, (0, 0))  # เรียก bg

    text = press_font.render("PRESS ANY KEY TO START", True, (10, 10, 10))
    screen.blit(text, (80, 400))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # ถ้ามีการปิดหน้าต่างจะสั่งให้เกมจบลง
            running = False
            wait = False
        if event.type == pygame.KEYDOWN:
            wait = False

    # Continually update game screen
    pygame.display.update()

while running:  # ขึ้นหน้าจอเกม
    
    # Background (R,G,B)
    screen.fill((26, 152, 201))
    screen.blit(background, (0, 0))  # เรียก background มาแสดงเริ่มจากจุด0,0
    # Defining every possible event occurence in game screen
    for event in pygame.event.get():  # วนลูปเพื่อตรวจสอบว่ามี event ใดเกิดขึ้นแล้วให้ทำงานตามeventนั้นๆ
       
        # Quitting application ขึ้นหน้าจอสีดำ
        if event.type == pygame.QUIT:  # ถ้ามีการปิดหน้าต่างจะสั่งให้เกมจบลง
            running = False  # หยุดลูป

        # Checking keystrokes (pressing down a key)
        if event.type == pygame.KEYDOWN:
                
            # Left key pressed
            if event.key == pygame.K_LEFT:
                # playerX_change = -8
                player.location_x_change = -8

            # Right key pressed
            if event.key == pygame.K_RIGHT:
                # playerX_change = +8
                player.location_x_change = 8

        # Checking keystrokes (releasing a key)
        if event.type == pygame.KEYUP:

            # Key released
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                # playerX_change = 0
                player.location_x_change = 0

    # Updating basket position horizontally
    player.location_x += player.location_x_change
    
    # Adding boundaries
    if player.location_x <= 0:
        player.location_x = 0

    if player.location_x >= 670:
        player.location_x = 670

    for i in range(total_animal_rain):
        # Updating animal direction vertically
        animal = animals[i]
        if animal.location_y <= 536:
            animal.location_y += animal.location_y_change  #เปลี่ยนตำแหน่งสิ่งของในแกนy

        # Collision
        collision = isCollision(animal, player)

        if collision:  # สัตว์ชนตระกร้า ดูว่า return ได้อะไรออกมาจาก def isCollision ; collision = True
            # score_value +=1
            if isinstance(animal, Bomb):  # check ว่า animal = Bomb
                game_over()
            else:
                score_value += animal.score

                score_sound = mixer.Sound('assets/PointScore.wav')
                score_sound.play()

                animals[i] = random_animal(30)

        # TIMER
        if (animal.location_y < 534):
            updated_time = int(time.time() - startTime)

        # GameOver
        if 534 <= animal.location_y < 534 + animal.location_y_change:
            if isinstance(animal, Bomb) or isinstance(animal, SickAnimal):
                animals[i] = random_animal(30)
            else:
                game_over()

        if animal.location_y >= 2000:
            game_over_text()

        render_animal(animal)

    render_player(player)
    showScore(textX, textY)
    showTime(updated_time)

    # Continually update game screen
    pygame.display.update()
