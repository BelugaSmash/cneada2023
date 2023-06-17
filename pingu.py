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
jump_cnt = 2

# bgm 설정
bgm = pygame.mixer.Sound("resource/it's just burning memory.wav")
bgm.set_volume(0.5)
bgm.play(-1)

# 장애물 변수 선언
obs_x = [screen_w, screen_w * 3 / 2]
obs_t = [random.randint(1, 3), random.randint(1, 3)]
obs_w, obs_h = 55, 80
obs_speed = 8

game_over = False

# FPS 설정을 위한 변수
clock = pygame.time.Clock()

# 좌표, 가로 크기, 세로 크기가 주어졌을 때 충돌 했는지 체크
def collide(x, y, w, h, x_, y_, w_, h_):
    return x < x_ + w_ and y < y_ + h_ and x + w > x_ and y + h > y_

def game_restart(): 
    global player_y, gravity, sliding, jumping, jump_cnt, obs_x, obs_t, game_over 
    player_y = opy
    gravity = 0 
    sliding = False
    jumping = False
    jump_cnt = 2
    obs_x = [screen_w, screen_w * 3 / 2]
    obs_t = [random.randint(1, 3), random.randint(1, 3)]
    game_over = False
    bgm.play()

while 1:
    # FPS를 60으로 설정
    clock.tick(60)
    # 파이게임 기본 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over:
                game_restart()
            else:
                if jump_cnt > 0:
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        gravity = 20
                        jumping = True
                        jump_cnt -= 1
                if event.key == pygame.K_DOWN:
                    sliding = True
        if event.type == pygame.KEYUP:
            if not game_over: 
                if event.key == pygame.K_DOWN:
                    sliding = False

    if not game_over:
        # 플레이어 움직이기
        player_y -= gravity
        if player_y >= opy:
            player_y = opy
            jumping = False
            jump_cnt = 2
        gravity -= 1.2
        
    
        # 장애물 움직이기
        for i in range(2): 
            obs_x[i] -= obs_speed
            if obs_x[i] + obs_w <= 0:
                px = obs_x[abs(1 - i)] + screen_w / 2 + random.randint(0, 700)
                obs_t[i] = random.randint(1, 3)
                obs_x[i] += px
    
    screen.fill((50, 150, 200))
    # 바닥 그리기
    pygame.draw.rect(screen, (100, 70, 70), [0, screen_h - floor_h, screen_w, floor_h])
    pygame.draw.rect(screen, (0, 200, 0), [0, screen_h - floor_h, screen_w, 30])
    # 플레이어 그리기
    player_rect = [100, player_y + (player_h / 2 if sliding and not jumping else 0), player_w, player_h / (2 if sliding and not jumping  else 1)]
    pygame.draw.rect(screen, (0, 0, 255), player_rect)
    # 장애물 그리기
    for i in range(2):
        obs_rect = []
        if obs_t[i] == 3:
            obs_rect =  [obs_x[i], screen_h - floor_h - player_h * 4 / 5 - obs_h * obs_t[i], obs_w, obs_h * obs_t[i]]
        else:
            obs_rect = [obs_x[i], screen_h - floor_h - obs_h * obs_t[i], obs_w, obs_h * obs_t[i]]
        pygame.draw.rect(screen, (255, 0, 0), obs_rect)
        if collide(*player_rect, *obs_rect) and not game_over:
            bgm.stop()
            game_over = True
    pygame.display.update()

# 2초 기다리고 게임을 끈다.
pygame.time.delay(2000)
sys.exit()
