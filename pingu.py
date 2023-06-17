import pygame
import sys
import os
import random

# 파이게임 초기화
pygame.init()

# 창 제목 설정
pygame.display.set_caption("Pingu's Adventure II")

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
gravity = 0 
sliding = False 
jumping = False
jumpCnt = 2

# 장애물 변수 선언
obs_x = [screen_w, screen_w * 3 / 2]
obs_t = [random.randint(1, 2), random.randint(1, 2)]
obs_w, obs_h = 55, 80
obs_speed = 8

# FPS 설정을 위한 변수
clock = pygame.time.Clock()
while 1:
    # FPS를 60으로 설정
    clock.tick(60)
    # 파이게임 기본 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if jumpCnt > 0:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    gravity = 20
                    jumping = True
                    jumpCnt -= 1
            if event.key == pygame.K_DOWN:
                sliding = True
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_DOWN:
                sliding = False

    # 플레이어 움직이기
    player_y -= gravity
    if player_y >= opy:
        player_y = opy
        jumping = False
        jumpCnt = 2
    gravity -= 1.2
    
    # 장애물 움직이기
    for i in range(2): 
        obs_x[i] -= obs_speed
        if obs_x[i] + obs_w <= 0:
            px = obs_x[abs(1 - i)] + screen_w / 2 + random.randint(0, 700)
            obs_t[i] = random.randint(1, 2)
            obs_x[i] += px
    
    screen.fill((50, 150, 200))
    # 바닥 그리기
    pygame.draw.rect(screen, (100, 70, 70), [0, screen_h - floor_h, screen_w, floor_h])
    pygame.draw.rect(screen, (0, 200, 0), [0, screen_h - floor_h, screen_w, 30])
    # 플레이어 그리기
    pygame.draw.rect(screen, (0, 0, 255), [100, player_y + (player_h / 2 if sliding and not jumping else 0), player_w, player_h / (2 if sliding and not jumping  else 1)])
    # 장애물 그리기
    for i in range(2):
        pygame.draw.rect(screen, (255, 0, 0), [obs_x[i], screen_h - floor_h - obs_h * obs_t[i], obs_w, obs_h * obs_t[i]])
    pygame.display.update()

# 2초 기다리고 게임을 끈다.
pygame.time.delay(2000)
sys.exit()
