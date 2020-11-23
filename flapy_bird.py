import pygame, sys, random

def draw_base():
    screen.blit(base, (base_x_pos, 590))
    screen.blit(base, (base_x_pos+500, 590))

def create_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(600,random_pipe))
    top_pipe = pipe_surface.get_rect(midtop=(600, random_pipe-500))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 500:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            can_score = True
            collision.play()
            return False
    if bird_rect.top <=-5 or bird_rect.bottom >= 580:
        can_score = True
        collision.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*5, 1)
    return new_bird

def bird_animation():
    new_bird = bird_animations[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "play":
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center=(245,20))
        screen.blit(score_surface,score_rect)
    if game_state == "over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(245, 20))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(245, 500))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score >= high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score, can_score, score_counter
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 2
                score_counter -= 1
                if score_counter<0:
                    score_sound.play()
                    score_counter = 100
                can_score = False
            if pipe.centerx <= 0:
                can_score=True


pygame.init()
screen = pygame.display.set_mode((500,650))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',30)

#game variables
gravity = 0.08
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
score_counter =100
#backgrounds
background = pygame.image.load('images/background-day2.jpg').convert()
middle = pygame.image.load('images/middle.jpg').convert()
base = pygame.image.load('images/base.jpg').convert()

#move base
base_x_pos = 0

#bird
bird_downflap = pygame.image.load('images/redbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('images/redbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('images/redbird-upflap.png').convert_alpha()
bird_animations = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_animations[bird_index]
bird_rect = bird_surface.get_rect(center=(100,325))
Birdflap = pygame.USEREVENT+1
pygame.time.set_timer(Birdflap,300)

#add pipes
pipe_surface = pygame.image.load('images/pipe-green.png').convert()
pipe_list = []
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1000)
pipe_height = [270, 300, 320, 350, 400, 500]

#game over surgace
game_over_surface = pygame.image.load('images/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(250,280))

#sounds
flip_sound = pygame.mixer.Sound('audio/wing.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
collision = pygame.mixer.Sound('audio/hit.wav')
score_sound_count = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flip_sound.play()
                bird_movement=0
                bird_movement-=3
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                score = 0
                bird_rect.center = (100,325)
                score_counter = 100
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == Birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    screen.blit(background, (0,0))
    screen.blit(middle, (0, 580))
    if game_active:
        #bird movements control
        bird_movement+=gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird, bird_rect)
        check_collision(pipe_list)

        #pipes
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #score
        pipe_score_check()
        score_display("play")
        #print(score_sound_count)


        game_active = check_collision(pipe_list)
    else:
        screen.blit(game_over_surface, game_over_rect)

        suggesion = game_font.render("PRESS SPACE TO RESTART", True, (255, 255, 255))
        suggesion_rect = suggesion.get_rect(center=(250, 350))
        screen.blit(suggesion, suggesion_rect)

        high_score = update_score(score, high_score)
        score_display("over")

    #floor
    base_x_pos-=1                           #moving base
    draw_base()                             #function for draw and move base
    if base_x_pos<=-500:
        base_x_pos=0
    pygame.display.update()
    clock.tick(100)