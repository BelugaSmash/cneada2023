import pygame
import sys
import os

# 파이게임 초기화
pygame.init()

# 창 제목 설정
pygame.display.set_caption("Pingu's Adventure")

# 파이게임 화면 크기 설정
screen_w, screen_h = 1280, 720
screen = pygame.display.set_mode((screen_w, screen_h))

# 변수들 초기화
cpath = os.path.dirname(__file__)
#player_img = pygame.image.load("resources/pingu2.png")

floor_h = 200
player_w, player_h = 55, 55
player_y = screen_h - floor_h - player_h
opy = player_y

# FPS 설정을 위한 변수
clock = pygame.time.Clock()
while 1:
    # FPS를 60으로 설정
    clock.tick(60)
    # 파이게임 기본 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill((50, 150, 200))
    pygame.draw.rect(screen, (100, 70, 70), [0, screen_h - floor_h, screen_w, floor_h])
    pygame.draw.rect(screen, (0, 200, 0), [0, screen_h - floor_h, screen_w, 30])
    pygame.draw.rect(screen, (0, 0, 255), [100, player_y, player_w, player_h])
    pygame.display.update()

# 2초 기다리고 게임을 끈다.
pygame.time.delay(2000)
sys.exit()
