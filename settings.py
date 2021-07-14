import pygame

SCREEN_HEIGHT = 360
SCREEN_WIDTH = 300
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 255)
Blue = (0, 0, 255)
Midblue = (96, 96, 96)
HS_FILE = "highscore.txt"
model = pygame.image.load("player.png")
background = pygame.image.load("background.jpg")
new_platform = pygame.image.load("platform.png")
standing = pygame.image.load("player.png")
l_standing = pygame.transform.flip(pygame.image.load("player.png"), True, False)
dead = pygame.image.load("dead.png")


x = 150
pla_x = 0
y = 320
pla_y = 0
h = 100
FPS = 60
Font = 'arial'

PLATFORMS_LIST = [(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
                  (SCREEN_WIDTH/2 - 10, (SCREEN_HEIGHT * 3 / 4), 50, 10),
                  (125, SCREEN_HEIGHT - 250, 100, 20),
                  (200, 250, 100, 20),
                  (50, 150, 120, 20),
                  (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 80, 30)]
PLAYER_ACC = 0.7
PLAYER_FRI = -0.05
