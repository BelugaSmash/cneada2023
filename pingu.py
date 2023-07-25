import pygame
import sys
import os
import math
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
obs_img = [0] + [pygame.image.load(f"resource/obstacle{i + 1}.png") for i in range(3)]
laser_img = pygame.image.load("resource/laser.png")
missile_img = [pygame.image.load(f"resource/missile{i}.png") for i in range(2)]
tuna_img = pygame.image.load("resource/tuna.png")
spike_img = pygame.image.load("resource/spike.png")
floor_img = [pygame.image.load("resource/floor.png"), pygame.image.load("resource/floor2.png")]
bg_img = [pygame.image.load(f"resource/bg{i + 1}.png").convert() for i in range(2)]

floor_h = 200

# 화면 흔들림 구현 위해
sc_shake_x, sc_shake_y = 0, 0
shake_frame = 0

#플레이어 관련 변수 선언
player_w, player_h = 55, 55
player_x = 100
player_y = screen_h - floor_h - player_h
player_speed = 5
player_pushed = False
move_x = 0
player_anim_frame = 0
attack_cool_frame = 0
player_attack = []
player_anim = 0
opy = player_y
gravity = 0 
sliding = False 
jumping = False
jump_cnt = 2
bullet_speed = 20

# 보스 관련 변수 선언
boss_hand_x = [830, 1000]
hand_y = screen_h - floor_h - 34 + 300
boss_x, boss_y = 810, screen_h - floor_h
hand_up = True
tuna_y = -10
tuna_up = False

# 소리 관련 변수 설정
bgm = pygame.mixer.Sound("resource/it's just burning memory.wav")
jump_sound = pygame.mixer.Sound("resource/juuuuuump.wav")
boom_sound = pygame.mixer.Sound("resource/boom.wav")
m_boss_bgm = pygame.mixer.Sound("resource/m_boss.wav")
m_boss_end_bgm = pygame.mixer.Sound("resource/peaceful.wav")
f_boss_bgm = pygame.mixer.Sound("resource/f_boss.mp3")
jump_sound.set_volume(0.35)
bgm.set_volume(1)
m_boss_bgm.set_volume(0.4)
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
m_boss_df = 0
boss_turn = 100
boss_attack = 0
boss_hp = 10
boss_p = 50
attack_frame = 0
laser_shot = False
spike_up = False
spike_x, spike_y = 0, 0
missile_anim = 0
missile_fire = False
missile_x, missile_y = 100 + screen_w, screen_h - floor_h - 150 - screen_w / 2
floor_x = 0
floor_speed = 8
mode = "normal"
pressed_key = []

# 점수표시 등을 위한 폰트 불러오기
font1 = pygame.font.SysFont('Sans', 30)

# 게임오버 관련 변수
game_over = False
game_over_frame = 0

# FPS 설정을 위한 변수
clock = pygame.time.Clock()

# 좌표, 가로 크기, 세로 크기가 주어졌을 때 충돌 했는지 체크
def collide(x, y, w, h, x_, y_, w_, h_):
    return x < x_ + w_ and y < y_ + h_ and x + w > x_ and y + h > y_

# 게임 시작할때 변수 선언
def game_restart():
    global player_x, player_y, gravity, sliding, jumping, jump_cnt, obs_x, obs_t, game_over, score, mode, hand_up, obs_y, sc_shake_x, sc_shake_y, shake_frame, \
        hand_y, boss_y, boss_x, missile_x, missile_y, missile_fire, attack_frame, laser_shot, boss_attack, game_over_frame, boss_hp, m_boss_df, player_pushed, \
        spike_up
    player_x = 100
    player_y = opy
    gravity = 0 
    sliding = False
    jumping = False
    hand_up = True
    player_pushed = False
    obs_y = 0
    jump_cnt = 2
    score = 0
    hand_y = screen_h - floor_h - 34 + 300
    boss_x, boss_y = 810, screen_h - floor_h
    m_boss_df = 0
    boss_attack = 0
    missile_x, missile_y = 100 + screen_w, screen_h - floor_h - 150 - screen_w / 2
    missile_fire = False
    laser_shot = False
    spike_up = False
    sc_shake_x = sc_shake_y = 0
    shake_frame = 0
    attack_frame = 0
    game_over_frame = 0
    boss_hp = 400
    mode = "normal"
    obs_x = [screen_w, screen_w * 4 / 3 + random.randint(0, 200), screen_w * 5 / 3 + random.randint(200, 400)]
    obs_t = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
    game_over = False
    bgm.play()
    m_boss_bgm.stop()
    f_boss_bgm.stop()

while 1:
    # FPS를 60으로 설정
    clock.tick(60)

    # 파이게임 기본 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # 마우스를 누른 경우        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if game_over_frame >= 60:
                    game_restart()
            else:
                mouse_pos = pygame.mouse.get_pos()
                if (mode == "m boss" or mode == "f boss") and attack_cool_frame <= 0:
                    distance = math.sqrt((player_x + 20 - mouse_pos[0]) ** 2 + (player_y + player_w / 2 - mouse_pos[1]) ** 2)
                    direction = (mouse_pos[0] - player_x - 20, mouse_pos[1] - player_y - player_h / 2)
                    normalized = (direction[0] / distance, direction[1] / distance)
                    move_vector = (normalized[0] * bullet_speed, normalized[1] * bullet_speed)
                    player_attack.append([player_x + 20, player_y + player_h / 2, move_vector])
                    attack_cool_frame = 10
        
        # 키를 누른 경우
        if event.type == pygame.KEYDOWN:
            if game_over:
                if game_over_frame >= 60:
                    game_restart()
            else:
                # 남은 점프 횟수가 있고
                if jump_cnt > 0:
                    # 위쪽 방향키/스페이스키를 눌렀다면 점프 하고 점프 횟수 한개 줄이기
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        gravity = 20
                        jumping = True
                        jump_cnt -= 1
                        jump_sound.play()
                # 아래 방향키 눌렀다면 슬라이딩 중으로 바꾸기
                if event.key == pygame.K_s:
                    sliding = True
                # 현재 중간보스이고, x키를 눌렀다면 총알 발사
                if event.key == pygame.K_x and (mode == "m boss" or mode == "f boss") and attack_cool_frame <= 0:
                    player_attack.append([player_x + 20, player_y + player_w / 2])
                    attack_cool_frame = 10
                if event.key == pygame.K_a:
                    pressed_key.append("left")
                if event.key == pygame.K_d:
                    pressed_key.append("right")
        # 키를 뗀 경우
        if event.type == pygame.KEYUP:
            # 아래 방향키를 뗐다면 슬라이딩 중을 아님으로 바꾸기
            if not game_over:
                if event.key == pygame.K_s:
                    sliding = False
                if event.key == pygame.K_a:
                    pressed_key.remove("left")
                if event.key == pygame.K_d:
                    pressed_key.remove("right")

    # 게임 오버가 아니라면
    if not game_over:
        # 플레이어 움직이기
        player_y -= gravity
        if player_y >= opy:
            player_y = opy
            jumping = False
            jump_cnt = 2
        gravity -= 1.2

        move_x = (player_speed if "right" in pressed_key else 0) + (-player_speed if "left" in pressed_key else 0)

        floor_x -= floor_speed

        # 플레이어 공격 쿨타임 확인
        attack_cool_frame -= 1        
    
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
        
        # 플레이어 걷는 애니메이션 처리
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
                    m_boss_bgm.play(-1)
        
        # 손으로 바닥 쿵 찍으면서 장애물 올라가고, 보스 나오는 부분
        if not hand_up:
            obs_y -= 50
            if boss_y >= screen_h - floor_h - 260:
                boss_y -= 3

        # 중간보스일때
        if mode == "m boss":
            boss_turn -= 1
            # 보스가 공격할 시간일떄
            if boss_turn <= 0:
                # 얼마나 뒤에 보스 공격을 한번 더할껀지
                boss_turn = 60 * 6
                # 공격 패턴 정하기(중간보스: 1~3번, 최종보스 4~4번)
                boss_attack = random.randint(1, 3)
                # 1번 패턴이면 화면 흔들고
                if boss_attack == 1:
                    shake_frame = 10
                # 3번 패턴이면 레이저 발사 준비
                elif boss_attack == 3:
                    attack_frame = 160

        # 최종 
        if mode == "f boss":
            boss_turn -= 1
            # 보스가 공격할 시간일떄
            if boss_turn <= 0:
                # 얼마나 뒤에 보스 공격을 한번 더할껀지
                boss_turn = 60 * 6
                # 공격 패턴 정하기(중간보스: 1~3번, 최종보스 4~4번)
                boss_attack = random.randint(4, 4)
                # 4번 패턴이면 화면 흔들고
                if boss_attack == 4:
                    attack_frame = 160

        # 1번 패턴이면 화면 흔드는 동알 빨리 이동, 화면 안흔들릴시 천천히 이동하고 제자리 돌아오면 공격 끝내기
        if boss_attack == 1:
            if shake_frame > 0:
                boss_x -= 20
            boss_x -= 10
            if boss_x == 810:
                boss_attack = 0
            if boss_x <= -309:
                boss_x += screen_w + 200

        # 2번 패턴이면 손위로 올린후 내려 찍으며 미사일 발사
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
        
        # 3번 패턴일때 40 프레임마다 번갈아가며 레이저 껐다 켰다
        if boss_attack == 3:
            attack_frame -= 1
            if attack_frame % 40 == 0:
                laser_shot = not laser_shot
                # 레이저 켜지면 화면 흔들기
                if laser_shot:
                    shake_frame = 30
            # 레이저 발사 시간 끝나면 공격 끝내기
            if attack_frame == 0:
                boss_attack = 0
        
        # 4번 패턴일때 40 프레임마다 번갈아가며 레이저 껐다 켰다
        if boss_attack == 4:
            if not spike_up:
                spike_x = player_x - (500 - player_w) / 2
                spike_y = screen_h - floor_h + 20
            attack_frame -= 1
            if attack_frame % 40 == 0:
                spike_up = not spike_up
                # 가시 올라오면 화면 흔들기
                if spike_up:
                    shake_frame = 10
            if attack_frame == 0:
                boss_attack = 0

        if spike_up:
            spike_y -= 20
            if spike_y <= screen_h - floor_h - 60:
                spike_y = screen_h - floor_h - 60
        else:
            spike_y += 10
        
        # 미사일을 발사하면
        if missile_fire:
            # 플레이어가 슬라이딩 해야할 높이까지 내려왔다면 왼쪽으로만 이동하고, 아니면 아래쪽으로도 이동
            if missile_y >= screen_h - floor_h - 30 - 175:
                missile_x -= 2
                missile_anim = 1
            else:
                missile_x -= 40
                missile_y += 20
        
        if mode == 'm boss disappear':
            hand_up = True
            m_boss_df += 1
            if not hand_y >= screen_h - floor_h - 34 + 300:
                hand_y += 10
                boss_y += 10
            if m_boss_df >= 5 * 60:
                mode = 'f boss appear'
                boss_turn = 60 * 6

        if mode == 'f boss appear':
            player_x += 4   
            if hand_up:
                hand_y -= 3
                if hand_y <= screen_h - floor_h - 34 - 150:
                    hand_up = False
            else:
                hand_y += 20
                if hand_y >= screen_h - floor_h - 14:
                    hand_y = screen_h - floor_h - 16
                    mode = "f boss"
                    shake_frame = 30
                    m_boss_end_bgm.stop()
                    boom_sound.play()
                    f_boss_bgm.play(-1)

        if mode == 'f boss':
            if not player_pushed:
                player_x -= 20
                if player_x <= 100:
                    player_pushed = True
                    player_x = 100
            else:
                player_x += move_x
                if player_x <= 0:
                    player_x = 0
                elif player_x + player_w >= screen_w:
                    player_x = screen_w - player_w

        if tuna_up:
            tuna_y -= 1
            if tuna_y == -10:
                tuna_up = False
        else:
            tuna_y += 1
            if tuna_y == 10:
                tuna_up = True

        # 화면 흔들기 효과 지속시간이 남았다면 sc_shake 변수 설정해 화면 흔들기(더 쎄게 흔들려면 -50, 50을 절댓값이 더 큰수로 바꾸면 됨)       
        if shake_frame > 0:
            shake_frame -= 1
            sc_shake_x = random.randint(-50, 50)
            sc_shake_y = random.randint(-50, 50)
        else:
            sc_shake_x = sc_shake_y = 0
    # 게임 오버 상태라면 게임 오버 후 몇프레임 지났는지 확인
    else:
        game_over_frame += 1
    
    # 화면(배경) 채우기
    bg_idx = 0
    if mode == "m boss" or mode == "m boss disappear" or mode == "f boss appear" or mode == 'f boss':
        bg_idx = 1
    screen.blit(bg_img[bg_idx], (0,0))
    
    if hand_up:
        # 중간 보스 손 그리기
        screen.blit(boss_hand[0], (boss_hand_x[0] + sc_shake_x, hand_y + sc_shake_y))
        screen.blit(boss_hand[1], (boss_hand_x[1] + sc_shake_x, hand_y + sc_shake_y))
    
    # 보스 화면에 보여질 위치와 히트박스 설정
    boss_rect = [boss_x + sc_shake_x, boss_y + sc_shake_y, 309, 800]
    boss_hitbox = [boss_x + 100 + sc_shake_x, boss_y + 50  + sc_shake_y, 309 - 200, 750]
    pygame.draw.rect(screen, (0, 255, 0), boss_hitbox)
     
    # 레이저 히트박스 설정
    laser_hitbox = [810 - screen_w + 100 + sc_shake_x, screen_h - floor_h - 75 + sc_shake_y, 1280, 50]
    # 레이저 발사 전이라면
    if boss_attack == 3 and not laser_shot and (attack_frame // 5) % 2 == 0:
        # 레이저 경고 표시 그리기
        pygame.draw.rect(screen, (200, 50, 50), laser_hitbox)
    # 레이저 발사중이라면
    if laser_shot:
        # 레이저(보스 공격) 그리기
        screen.blit(laser_img, (810 - screen_w + 100 + sc_shake_x, screen_h - floor_h - 100 + sc_shake_y))

    
    spike_hitbox = [spike_x + sc_shake_x, spike_y + sc_shake_y, 500, 80]
    spike_warn = [spike_x + sc_shake_x, screen_h - floor_h - 60 + sc_shake_y, 500, 80]
    # 가시 올라오기전
    if boss_attack == 4 and not spike_up and (attack_frame // 5) % 2 == 0:
        # 경고 표시 그리기
        pygame.draw.rect(screen, (200, 50, 50), spike_warn)
    if spike_up:
        # 가시(보스 공격) 그리기
        screen.blit(spike_img, spike_hitbox)


    # 참치 그리기
    if mode == 'm boss disappear' or mode == 'f boss appear' or mode == 'f boss':
        screen.blit(tuna_img, (850, screen_h - floor_h - 200 + tuna_y))

    # 보스 공격 패턴에 따라 중간보스 그리기
    if boss_attack == 0:
        screen.blit(boss_img, boss_rect)
    elif boss_attack == 1 or boss_attack == 2:
        screen.blit(boss_attack_img, boss_rect)
    elif boss_attack == 3 or boss_attack == 4:
        screen.blit(boss_img if not laser_shot and not spike_up else boss_attack_img, boss_rect)
    
    # 바닥 그리기
    floor_idx = bg_idx
    pygame.draw.rect(screen, (0, 0, 0), [0, screen_h - floor_h + 50, 1280, floor_h - 50])
    screen.blit(floor_img[floor_idx], (floor_x % (screen_w * 2) - screen_w + sc_shake_x, screen_h - floor_h - 50 + sc_shake_y))
    screen.blit(floor_img[floor_idx], (((floor_x + screen_w) % (screen_w * 2) - screen_w + sc_shake_x, screen_h - floor_h - 50 + sc_shake_y)))

    if not hand_up:
        # 중간 보스 손 그리기
        screen.blit(boss_hand[0], (boss_hand_x[0] + sc_shake_x, hand_y + sc_shake_y))
        screen.blit(boss_hand[1], (boss_hand_x[1] + sc_shake_x, hand_y + sc_shake_y))

    # 미사일 히트박스 설정
    missile_hitbox = [missile_x + 20 + sc_shake_x, missile_y + 75 + sc_shake_y, 100, 75]
    # 히트박스 그리기
    pygame.draw.rect(screen, (255, 0, 0), missile_hitbox)
    # 미사일(보스 공격) 그리기
    screen.blit(missile_img[missile_anim], (missile_x + sc_shake_x, missile_y + sc_shake_y))

    # 플레이어 총알이 화면 밖으로 나가거나 보스에 맞아 없어질 공격 저장할 리스트
    remove_t = []
    # 모들 플레이어 총알 확인
    for atk in player_attack:
        # 보스 쪽으로 발사
        atk[0] += atk[2][0]
        atk[1] += atk[2][1]
        # 화면에 보여질 위치 설정
        atk_rect = [atk[0] + sc_shake_x, atk[1] + sc_shake_y, 10, 10]
        # 화면 밖으로 나갔다면 remove_t 리스트에 추가
        if atk[0] >= screen_w:
            remove_t.append(atk)
        # 보스에 공격이 맞았다면 보스 체력 깍고 remove_t 에 추가
        elif collide(*atk_rect, *boss_hitbox):
            if boss_attack != 1:
                boss_hp -= 1
            remove_t.append(atk)
        # 플레이어 공격 그리기
        pygame.draw.rect(screen, (0, 0, 255), atk_rect)

    # remove_t에 있는 총알 player_attack에서 삭제
    for r in remove_t:
        player_attack.remove(r)

    if mode == 'm boss' and boss_hp <= 0:
        m_boss_bgm.stop()
        m_boss_end_bgm.play()
        boss_hp = 800
        mode = "m boss disappear"
        boss_attack = 0
        attack_frame = 0
        missile_fire = False
        missile_x -= 1000
        missile_y += 2000
        laser_shot = False
        boss_turn = 10 * 60

    # 히트박스 설정(슬라이딩 상태라면) 세로 길이를 반으로
    player_rect = [player_x + sc_shake_x, player_y + (player_h / 2 if sliding and not jumping else 0) + sc_shake_y, player_w, player_h / (2 if sliding and not jumping  else 1)]
    if jumping or not sliding:
        # 점프중이거나 걷는 상태라면 움직이는 모습으로 그리기
        screen.blit(player_walk_img[player_anim % 28], player_rect)
    else:
        # 슬라이딩 중이라면 슬라이딩 하는 모습으로 그리기
        screen.blit(player_slide_img, player_rect)

    # 플레이어가 보스에 닿았거나, 미사일, 레이저에 닿았다면 게임 오버 처리
    if (collide(*player_rect, *boss_hitbox) or \
        collide(*player_rect, *missile_hitbox) or \
        (collide(*player_rect, *laser_hitbox) and laser_shot) or \
        (collide(*player_rect, *spike_hitbox) and spike_up)) and \
        not game_over:
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

        # 플레이어가 장애물에 닿았다면 게임 오버 처리
        if collide(*player_rect, *obs_rect) and not game_over and (mode == "normal" or mode == "m boss appear"):
            bgm.stop()
            game_over = True
    
    # 점수 표시
    score_color = (0, 0, 0)
    # 중간보스일 경우 색을 흰색으로
    if mode == "m boss" or mode == "m boss disappear" or mode == 'f boss appear' or mode == 'f boss':
        score_color = (255, 255, 255)
    scoretxt = font1.render('Score: ' + str(score), True, score_color)
    screen.blit(scoretxt, (10, 10))

    # 보스 체력 표시
    if mode == 'm boss':
        pygame.draw.rect(screen, (200, 200, 200), [screen_w / 2 - 202, 18, 404, 24])
        pygame.draw.rect(screen, (200, 50, 70), [screen_w / 2 - 200, 20, boss_hp, 20])
        score_color = (200, 50, 70)
        scoretxt = font1.render('Boss', True, score_color)
        screen.blit(scoretxt, (screen_w / 2 - 300, 10))
    if mode == 'f boss':
        pygame.draw.rect(screen, (200, 200, 200), [screen_w / 2 - 202, 18, 404, 24])
        pygame.draw.rect(screen, (200, 50, 70), [screen_w / 2 - 200, 20, boss_hp / 2, 20])
        score_color = (200, 50, 70)
        scoretxt = font1.render('Boss', True, score_color)
        screen.blit(scoretxt, (screen_w / 2 - 300, 10))

    # 화면 업데이트
    pygame.display.update()

# 2초 기다리고 게임을 끈다.
pygame.time.delay(2000)
sys.exit()
