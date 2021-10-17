from enum import Enum

import pygame
import random
import math
import time
import keyboard
from shuffleimages import shuffle
from pygame import mixer
from pynput.keyboard import Key, Controller


class Type(Enum):
    BOMB = 0
    DOG = 1
    DOG_SICK = 2
    CAT = 3


class Animal():
    def __init__(self, height):
        self.type = random.randint(0, 3)
        # self.img = pygame.image.load(shuffle())
        self.img = pygame.image.load(self.get_img())
        # self.score = 1
        self.score = self.get_score()
        self.location_x = random.randint(100, 700)
        self.location_y = height
        self.location_x_change = 0
        self.location_y_change = 2.5  #ความเร็วสัตว์ตก

    def get_img(self):
        images = ['assets/bomb.png', 'assets/dog.png', 'assets/dog-yellow.png', 'assets/cat.png']
        return images[self.type]

    def get_score(self):
        if self.type == Type.BOMB.value:
            return -9999
        elif self.type == Type.DOG_SICK.value:
            return -2
        else:
            return 1


class Player():
    def __init__(self):
        self.img = pygame.image.load('assets/basket.png')
        self.location_x = 350
        self.location_y = 480
        self.location_x_change = 0


# Initialize the pygame #เซทค่าเริ่มต้นเกม
pygame.init()

# Set game screen #เซทหน้าจอเกมกว้าง,สูงพิกเซล
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
# playerImg = pygame.image.load('assets/basket.png')

# Position basket at bottom centre
# playerX = 350
# playerY = 480
# playerX_change = 0
player = Player()

# CAT/DOG
total_animal_rain = 2
animals = []
# animalImg = []
# animalX = []amount
# animalY = []
# animalX_change = []
# animalY_change = []
height = 0

keyboard = Controller()
key = "a"
# keyboard.press(key)
# keyboard.release(key)

for i in range(total_animal_rain):
    # url = shuffle()
    # animalImg.append(pygame.image.load(url))
    #  create object animal
    animal = Animal(height)
    animals.append(animal)
    # Position animal randomly at top
    # animalX.append(random.randint(100,700))
    # animalY.append(height)
    # animalX_change.append(0)
    # animalY_change.append(3) #ความเร็วสัตว์ตก

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

    x_distance = abs(player.location_x - animal.location_x)
    y_distance = abs(player.location_y - animal.location_y)

    if distance < 60:
        return True
    elif x_distance < 80 and y_distance < 40:
        return True
    else:
        return False


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

    if (seconds < 10):
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
        animals[i].location_y = 2000


def game_over_text():
    game_over = over_font.render("GAME OVER", True, (10, 10, 10))
    screen.blit(game_over, (200, 380))
    mixer.music.stop()



# Game loop (persistence of game screen)
running = True

while running:  # ขึ้นหน้าจอเกมหลังจากrunบรรทัดที่150-->184-->185-->186-->189
    
    # Background (R,G,B)
    screen.fill((26, 152, 201))
    screen.blit(background, (0, 0))  # เรียกbackgroundมาแสดงเริ่มจากจุด0,0
    # Defining every possible event occurence in game screen
    for event in pygame.event.get():  # วนลูปเพื่อตรวจสอบว่ามีeventใดเกิดขึ้นแล้วให้ทำงานตามeventนั้นๆ
       
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
    # playerX += playerX_change
    player.location_x += player.location_x_change
    
    # Adding boundaries
    # if playerX <= 0:
    #     playerX = 0
    if player.location_x <= 0:
        player.location_x = 0

    # if playerX >= 670:
    #     playerX = 670
    if player.location_x >= 670:
        player.location_x = 670

    for i in range(total_animal_rain):
        # Updating animal direction vertically
        # if animalY[i] <= 536:
        #     animalY[i] += animalY_change[i]
        animal = animals[i]
        if animal.location_y <= 536:
            animal.location_y += animal.location_y_change

        # Collision
        collision = isCollision(animal, player)

        if collision:  # สัตว์ชนตระกร้า
            # score_value +=1
            if animal.type == Type.BOMB.value:
                game_over()
            else:
                score_value += animal.score

                score_sound = mixer.Sound('assets/PointScore.wav')
                score_sound.play()

                # animalX[i] = random.randint(0,736)  #ชนแล้วเกิดใหม่สุ่มx
                # animalY[i] = 30  #เกิดใหม่ที่y=30
                animals[i] = Animal(30)

        # TIMER
        if (animal.location_y < 534):
            updated_time = int(time.time() - startTime)

        # GameOver
        if 534 <= animal.location_y < 534 + animal.location_y_change:
            if animal.type in [Type.BOMB.value, Type.DOG_SICK.value]:
                animals[i] = Animal(30)
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
