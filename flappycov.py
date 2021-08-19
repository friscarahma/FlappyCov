__author__ = "Kelompok B"

import pygame
import os
import random

pygame.init()

#mengganti nama caption program dan logo program
pygame.display.set_caption('Flappy Cov')
ICON = pygame.image.load("Assets/Other/icon.png")
pygame.display.set_icon(ICON)

#mengatur ukuran layar
SCREEN_HEIGHT = 550
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#memanggil memanggil assets sprite, sound, dan tile
RUNNING = [pygame.image.load(os.path.join("Assets/Satgas", "satgas1.png")),
           pygame.image.load(os.path.join("Assets/Satgas", "satgas2.png")),
           pygame.image.load(os.path.join("Assets/Satgas", "satgas3.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Satgas", "lompat.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Satgas", "jongkok1.png")),
           pygame.image.load(os.path.join("Assets/Satgas", "jongkok2.png"))]

SMALL_COVID = [pygame.image.load(os.path.join("Assets/Covid", "virus.png")),
                pygame.image.load(os.path.join("Assets/Covid", "virus_mid_blue.png")),
                pygame.image.load(os.path.join("Assets/Covid", "virus_mid_green.png"))]
                
LARGE_COVID = [pygame.image.load(os.path.join("Assets/Covid", "virus_big.png")),
                pygame.image.load(os.path.join("Assets/Covid", "virus_big_purple.png")),
                pygame.image.load(os.path.join("Assets/Covid", "virus_big_grey.png")),
                 pygame.image.load(os.path.join("Assets/Covid", "virus_big_blue.png")),
                  pygame.image.load(os.path.join("Assets/Covid", "virus_big_green.png"))]

FLYCOVID = [pygame.image.load(os.path.join("Assets/Cov", "virus_big_purple.png")),
        pygame.image.load(os.path.join("Assets/Cov", "virus_mid_purple.png"))]

CLOUD = [pygame.image.load(os.path.join("Assets/Other", "awan1.png")),
pygame.image.load(os.path.join("Assets/Other", "awan2.png")),
pygame.image.load(os.path.join("Assets/Other", "awan3.png")),
pygame.image.load(os.path.join("Assets/Other", "awan_matahari.png"))]
       

BG = pygame.image.load(os.path.join("Assets/Other", "road.png"))

#SOUND
GAMEOVER = pygame.mixer.Sound("Assets/Other/gameover.wav")
INTRO = pygame.mixer.Sound("Assets/Other/intro.wav")
SOUND_JUMP = pygame.mixer.Sound("Assets/Other/jump.wav")

# class satgas untuk mengatur posisi sprite player satgas dan menambah logic menunduk, lari dan lompat
class Satgas:
    X_POS = 80
    Y_POS = 440
    Y_POS_DUCK = 460
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.satgas_duck = False
        self.satgas_run = True
        self.satgas_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.satgas_rect = self.image.get_rect()
        self.satgas_rect.x = self.X_POS
        self.satgas_rect.y = self.Y_POS

    def update(self, userInput):
        if self.satgas_duck:
            self.duck()
        if self.satgas_run:
            self.run()
        if self.satgas_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.satgas_jump:
            self.satgas_duck = False
            self.satgas_run = False
            self.satgas_jump = True
            SOUND_JUMP.play()
        elif userInput[pygame.K_SPACE] and not self.satgas_jump:
            self.satgas_duck = False
            self.satgas_run = False
            self.satgas_jump = True
            sound_jmp = pygame.mixer.Sound("Assets/Other/jump.wav")
            sound_jmp.play()
        elif userInput[pygame.K_DOWN] and not self.satgas_jump:
            self.satgas_duck = True
            self.satgas_run = False
            self.satgas_jump = False
        elif not (self.satgas_jump or userInput[pygame.K_DOWN]):
            self.satgas_duck = False
            self.satgas_run = True
            self.satgas_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.satgas_rect = self.image.get_rect()
        self.satgas_rect.x = self.X_POS
        self.satgas_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.satgas_rect = self.image.get_rect()
        self.satgas_rect.x = self.X_POS
        self.satgas_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.satgas_jump:
            self.satgas_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.satgas_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.satgas_rect.x, self.satgas_rect.y))

# Untuk memunculkan awan dan membuat awan berjalan
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(1, 100)
        self.image = CLOUD[random.randint(0, 3)]
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

#untuk memunculkan Covid dan Covid yg terbang
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCovid(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 469


class LargeCovid(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 455


class flyCovid(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 400
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

# menyimpan semua class dan variable
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    INTRO.stop()
    run = True
    clock = pygame.time.Clock()
    player = Satgas()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 315
    points = 0
    font = pygame.font.Font('Assets/Other/BaksoSapi.otf', 20)
    obstacles = []
    death_count = 0
  
    

#menambah score dan menambah kecepatan
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Skor: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

# memunculkan tile/ lantai secara terus menerus
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        SCREEN.fill((132, 228, 247))
        userInput = pygame.key.get_pressed()
        
        background()
        player.draw(SCREEN)
        player.update(userInput)

        #logic musuh apa yang selanjutnya muncul
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCovid(SMALL_COVID))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCovid(LARGE_COVID))
            elif random.randint(0, 2) == 2:
                obstacles.append(flyCovid(FLYCOVID))
       #mengecek apakah satgas dan corona bertabrakan kalai bertabrakan muncul game over
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.satgas_rect.colliderect(obstacle.rect):
                pygame.time.delay(900)
                death_count += 1
                menu(death_count)
              

        

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

#menu awal dan game over ketika terjadi tabrakan antara covid dan satgas maka muncul game over
def menu(death_count):
    global points
    run = True
    sound_over = True
    sound_intro = True
    while run:
         #screen start and game over color
        SCREEN.fill((132, 228, 247))
        font = pygame.font.Font('Assets/Other/BaksoSapi.otf', 30)
      
        if death_count == 0:
            if sound_intro:
                INTRO.play(-1)
                sound_intro = False
            text = font.render("Tekan Tombol apa saja untuk Mulai", True, (0, 0, 0))
            background_menu = pygame.image.load(os.path.join("Assets/Other", "opening.png"))
            SCREEN.blit(background_menu, (0,0))
            SCREEN.blit(RUNNING[1], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        elif death_count > 0:
            text = font.render("Tekan Tombol apa saja untuk ulang", True, (0, 0, 0))
            score = font.render("Skor Kamu: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            if sound_over:
                GAMEOVER.play()
                sound_over = False
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(LARGE_COVID[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            SCREEN.blit(score, scoreRect)
            background_over = pygame.image.load(os.path.join("Assets/Other", "gameover.png"))
            SCREEN.blit(background_over, (0,0))
        

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main()
                
               

menu(death_count=0)
