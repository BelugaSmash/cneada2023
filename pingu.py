import pygame
import sys
import os

# 파이게임 초기화
pygame.init()

# 창 제목 설정
pygame.display.set_caption("Pingu's Adventure")

# 파이게임 화면 크기 설정
screen = pygame.display.set_mode((1280, 720))

# 변수들 초기화
cpath = os.path.dirname(__file__)
#player_img = pygame.image.load("resources/pingu2.png")

# FPS 설정을 위한 변수
clock = pygame.time.Clock()
while 1:
    # FPS를 60으로 설정
    clock.tick(60)
    # 파이게임 기본 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

# 2초 기다리고 게임을 끈다.
pygame.time.delay(2000)
sys.exit()
