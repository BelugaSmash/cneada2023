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

# 이미지 변수들 초기화
cpath = os.path.dirname(__file__)
player_walk_img = [pygame.image.load(f"resource/pingu_walk/pingu_{str(i).zfill(2)}.png") for i in range(28)]
player_slide_img = pygame.image.load("resource/pingu_slide.png")
boss_hand = [pygame.image.load("resource/boss_hand_left.png"), pygame.image.load("resource/boss_hand_right.png")]
boss_img = pygame.image.load("resource/boss.png")
boss_attack_img = pygame.image.load("resource/boss_attack.png")
obs_img = [0, pygame.image.load("resource/obstacle1.png"), pygame.image.load("resource/obstacle2.png"), None]
laser_img = pygame.image.load("resource/laser.png")
missile_img = [pygame.image.load(f"resource/missile{i}.png") for i in range(2)]
bg_img = pygame.image.load("resource/bg.png")

floor_h = 200

# 화면 흔들림 구현 위해
sc_shake_x, sc_shake_y = 0, 0
shake_frame = 0

#플레이어 관련 변수 선언
player_w, player_h = 55, 55
player_y = screen_h - floor_h - player_h
player_anim_frame = 0
player_anim = 0
opy = player_y
gravity = 0 
sliding = False 
jumping = False
jump_cnt = 2

# 보스 관련 변수 선언
boss_hand_x = [830, 1000]
hand_y = screen_h - floor_h - 34 + 300
boss_x, boss_y = 810, screen_h - floor_h
hand_up = True

# 소리 관련 변수 설정
bgm = pygame.mixer.Sound("resource/it's just burning memory.wav")
jump_sound = pygame.mixer.Sound("resource/juuuuuump.wav")
boom_sound = pygame.mixer.Sound("resource/boom.wav")
m_boss_bgm = pygame.mixer.Sound("resource/m_boss.mp3")
jump_sound.set_volume(0.35)
bgm.set_volume(1)
m_boss_bgm.set_volume(0.7)
bgm.play(-1)

# 장애물 변수 선언
obs_x = [screen_w, screen_w * 4 / 3 + random.randint(100, 300), screen_w * 5 / 3 + random.randint(400, 600)]
obs_t = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
obs_w, obs_h = 55, 80
obs_y = 0
obs_speed = [8,8,8]

# 스테이지 관련 변수 선언
score = 0
m_boss_score = 5
boss_turn = 100
boss_attack = 0
missile_anim = 0
missile_fire = False
missile_x, missile_y = 100 + screen_w, screen_h - floor_h - 150 - screen_w / 2
mode = "normal"
font1 = pygame.font.SysFont('Sans', 30)

game_over = False

# FPS 설정을 위한 변수
clock = pygame.time.Clock()

# 좌표, 가로 크기, 세로 크기가 주어졌을 때 충돌 했는지 체크
def collide(x, y, w, h, x_, y_, w_, h_):
    return x < x_ + w_ and y < y_ + h_ and x + w > x_ and y + h > y_

def game_restart():
    global player_y, gravity, sliding, jumping, jump_cnt, obs_x, obs_t, game_over, score, mode, hand_up, obs_y, sc_shake_x, sc_shake_y, shake_frame, \
        hand_y, boss_y, boss_x, missile_x, missile_y, missile_fire
    player_y = opy
    gravity = 0 
    sliding = False
    jumping = False
    hand_up = True
    obs_y = 0
    jump_cnt = 2
    score = 0
    hand_y = screen_h - floor_h - 34 + 300
    boss_x, boss_y = 810, screen_h - floor_h
    missile_x, missile_y = 100 + screen_w, screen_h - floor_h - 150 - screen_w / 2
    missile_fire = False
    sc_shake_x = sc_shake_y = 0
    shake_frame = 0
    mode = "normal"
    obs_x = [screen_w, screen_w * 4 / 3 + random.randint(0, 200), screen_w * 5 / 3 + random.randint(200, 400)]
    obs_t = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
    game_over = False
    bgm.play()
    m_boss_bgm.stop()

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
                        jump_sound.play()
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
        for i in range(3): 
            obs_x[i] -= obs_speed[i]
            if obs_x[i] + obs_w <= 0:
                px = obs_x[i-1] + screen_w / 3 + random.randint(100, 300)
                obs_t[i] = random.randint(1, 3)
                obs_x[i] += px
                if score < m_boss_score:
                    score += 1
                    if score == m_boss_score:
                        mode = "m boss appear"
                        bgm.stop()
                #obs_speed[i] = random.randint(5,20)
        player_anim_frame += 1
        if player_anim_frame == 3:
            player_anim += 1
            player_anim_frame = 0
        
        # 중간보스 등장
        if mode == "m boss appear":
            if hand_up:
                hand_y -= 3
                if hand_y <= screen_h - floor_h - 34 - 150:
                    hand_up = False
            else:
                hand_y += 20
                if hand_y >= screen_h - floor_h - 14:
                    hand_y = screen_h - floor_h - 16
                    mode = "m boss"
                    shake_frame = 30
                    boom_sound.play()
                    m_boss_bgm.play()
        if not hand_up:
            obs_y -= 50
            if boss_y >= screen_h - floor_h - 260:
                boss_y -= 3

        if mode == "m boss":
            boss_turn -= 1
            if boss_turn == 0:
                boss_turn = 60 * 6
                boss_attack = random.randint(1, 2)
                if boss_attack == 1:
                    shake_frame = 10

        if boss_attack == 1:
            if shake_frame > 0:
                boss_x -= 20
            boss_x -= 10
            if boss_x == 810:
                boss_attack = 0
            if boss_x <= -309:
                boss_x += screen_w + 200

        if boss_attack == 2:
            if hand_y >= screen_h - floor_h - 34 - 150:
                hand_y -= 3
            else:
                hand_y = screen_h - floor_h - 16
                shake_frame = 30
                missile_fire = True
                missile_anim = 0
                missile_x, missile_y = 100 + screen_w, screen_h - floor_h - 150 - screen_w / 2
                boss_attack = 0
        
        if missile_fire:
            if missile_y >= screen_h - floor_h - 30 - 175:
                missile_x -= 2
                missile_anim = 1
            else:
                missile_x -= 40
                missile_y += 20
                    
        if shake_frame > 0:
            shake_frame -= 1
            sc_shake_x = random.randint(-50, 50)
            sc_shake_y = random.randint(-50, 50)
        else:
            sc_shake_x = sc_shake_y = 0

    # 화면(배경) 채우기
    bg_color = (50, 150, 200)
    if mode == "normal" or mode == "m boss appear":
        screen.fill(bg_color)
    elif mode == "m boss":
        screen.blit(bg_img, (0,0))
    if hand_up:
        # 중간 보스 그리기
        screen.blit(boss_hand[0], (boss_hand_x[0] + sc_shake_x, hand_y + sc_shake_y))
        screen.blit(boss_hand[1], (boss_hand_x[1] + sc_shake_x, hand_y + sc_shake_y))
    boss_rect = [boss_x + sc_shake_x, boss_y + sc_shake_y, 309, 800]
    boss_hitbox = [boss_x + 100 + sc_shake_x, boss_y + 50  + sc_shake_y, 309 - 200, 750]
    pygame.draw.rect(screen, (0, 255, 0), boss_hitbox)
    if boss_attack == 0:
        screen.blit(boss_img, boss_rect)
    elif boss_attack == 1 or boss_attack == 2:
        screen.blit(boss_attack_img, boss_rect)
    #screen.blit(laser_img, (0, 0))
    # 바닥 그리기
    pygame.draw.rect(screen, (100, 70, 70), [0 + sc_shake_x, screen_h - floor_h + sc_shake_y, screen_w, floor_h * 2])
    pygame.draw.rect(screen, (0, 200, 0), [0 + sc_shake_x, screen_h - floor_h + sc_shake_y, screen_w, 30])
    if not hand_up:
        # 중간 보스 그리기
        screen.blit(boss_hand[0], (boss_hand_x[0] + sc_shake_x, hand_y + sc_shake_y))
        screen.blit(boss_hand[1], (boss_hand_x[1] + sc_shake_x, hand_y + sc_shake_y))
    # 미사일(보스 공격) 그리기
    missile_hitbox = [missile_x + 20 + sc_shake_x, missile_y + 75 + sc_shake_y, 100, 75]
    pygame.draw.rect(screen, (255, 0, 0), missile_hitbox) # 히트박스 그리기
    screen.blit(missile_img[missile_anim], (missile_x + sc_shake_x, missile_y + sc_shake_y))
    # 플레이어 그리기
    player_rect = [100 + sc_shake_x, player_y + (player_h / 2 if sliding and not jumping else 0) + sc_shake_y, player_w, player_h / (2 if sliding and not jumping  else 1)]
    if jumping or not sliding:
        screen.blit(player_walk_img[player_anim % 28], player_rect)
    else:
        screen.blit(player_slide_img, player_rect)
    # pygame.draw.rect(screen, (0, 0, 255), player_rect)
    if (collide(*player_rect, *boss_hitbox) or collide(*player_rect, *missile_hitbox)) and not game_over:
        bgm.stop()
        game_over = True
    # 장애물 그리기
    for i in range(3):
        obs_rect = []
        if obs_t[i] == 3:
            obs_rect =  [obs_x[i] + sc_shake_x, screen_h - floor_h - player_h * 4 / 5 - obs_h * obs_t[i] + obs_y + sc_shake_y, obs_w, obs_h * obs_t[i]]
        else:
            obs_rect = [obs_x[i] + sc_shake_x, screen_h - floor_h - obs_h * obs_t[i] + obs_y + sc_shake_y, obs_w, obs_h * obs_t[i]]
        if obs_img[obs_t[i]] == None:
            pygame.draw.rect(screen, (255, 0, 0), obs_rect)
        else:
            screen.blit(obs_img[obs_t[i]], obs_rect)
        if collide(*player_rect, *obs_rect) and not game_over and (mode == "normal" or mode == "m boss appear"):
            bgm.stop()
            game_over = True
    
    score_color = (0, 0, 0)
    if mode == "m boss":
        score_color = (255, 255, 255)
    scoretxt = font1.render('Score: ' + str(score), True, score_color)
    screen.blit(scoretxt, (10, 10))

    pygame.display.update()

# 2초 기다리고 게임을 끈다.
pygame.time.delay(2000)
sys.exit()
