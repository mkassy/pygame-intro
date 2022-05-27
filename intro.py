from turtle import end_fill
import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # gets time in milliseconds
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect) # surface, and then pos
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 400: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(bird_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 400: 
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
        # walk
    # play walking animation if the player is on the floor
    # display the jump surface when the player is not on the floor

pygame.init()
screen = pygame.display.set_mode((800,500))
# screen_rect = screen.get_rect()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 50) # arguments: font type, font size
game_active = False
start_time = 0
score = 0

# Loading background images 
sky_surf = pygame.image.load('graphics/sky.png').convert() # convert alpha removes alpha values
ground_surf = pygame.image.load('graphics/ground3.png').convert() # convert makes game run faster
ground_surf = pygame.transform.scale(ground_surf, (1000,100))
# score_surf = test_font.render('My game', False, (64,64,64)) # test, AA, color(RGB or hex_color)
# score_rect = score_surf.get_rect(center = (400,50))

# Obstacles

# Snail
snail_surf = pygame.image.load('graphics/snail.png').convert_alpha()

# Bird
bird_fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
bird_fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
# bird_fly_1 = pygame.transform.rotozoom(bird_fly_1,0,0.1)
# bird_fly_2 = pygame.transform.rotozoom(bird_fly_2,0,0.1)
# bird_fly_1 = pygame.transform.flip(bird_fly_1,True,False)
# bird_fly_2 = pygame.transform.flip(bird_fly_2,True,False)

bird_list = [bird_fly_1, bird_fly_2]
bird_frames = []

for frame in bird_list:
    frame = pygame.transform.rotozoom(frame,0,0.1)
    frame = pygame.transform.flip(frame,True,False)
    bird_frames.append(frame)


bird_frame_index = 0
bird_surf = bird_frames[bird_frame_index]

obstacle_rect_list = []


player_walk_1 = pygame.image.load('graphics/png/cat/Walk (1).png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/png/cat/Walk (2).png').convert_alpha()
player_walk_1 = pygame.transform.rotozoom(player_walk_1,0,0.15)
player_walk_2 = pygame.transform.rotozoom(player_walk_2,0,0.15)
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/png/cat/Jump (8).png').convert_alpha()
player_jump = pygame.transform.rotozoom(player_jump,0,0.15)

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,400))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/png/cat/Run (7).png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,0.5)
player_stand_rect = player_stand.get_rect(center = (400, 250))

game_name = test_font.render("Leo's Fun Adventure!",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 35)
game_message = game_message_font.render('Actions: Press the space bar to hop!', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 420))

press_key_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 25)
press_key = press_key_font.render('Press space to continue.', False, 'orange')
press_key_rect = press_key.get_rect(center = (400,450))

# Timer
obstacle_timer = pygame.USEREVENT + 1 # always add plus 1 
pygame.time.set_timer(obstacle_timer,1600) # 2 arguments (what event you want to trigger, how many ms)

bird_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bird_animation_timer,300)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 400:
                    player_gravity = -20
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 400:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1200),400)))
                else:
                    obstacle_rect_list.append(bird_surf.get_rect(bottomright = (randint(900,1200),310)))

            if event.type == bird_animation_timer:
                if bird_frame_index == 0: bird_frame_index = 1
                else: bird_frame_index = 0
                bird_surf = bird_frames[bird_frame_index]


    if game_active:
        # draw all our elements   
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,400))
        # pygame.draw.rect(screen,'#c0e8ec', score_rect) # takes 3+ arguments
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) # 4th arg is line width, 5th is border rounding
        # pygame.draw.line(screen, 'gold', (0,0), pygame.mouse.get_pos(), width=5)
        # pygame.draw.ellipse(screen, 'brown', pygame.Rect(50,200,100,100)) # pygame.Rect() arguments: left, top, width, height
        
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # Snail
        # snail_rect.x -= 4
        # if snail_rect.right <= -100: snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        # player_rect.x += 1
        # if player_rect.left >= 800: player_rect.right = 0 
        if player_rect.bottom >= 400: player_rect.bottom = 400
        player_animation()
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear() # clears obstacles after game is done
        player_rect.midbottom = (80,400) # restarts player position
        player_gravity = 0 # restarts gravity at 0

        score_message = game_message_font.render(f"Your score is: {score}",False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,420))
        screen.blit(game_name,game_name_rect)
        screen.blit(press_key,press_key_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)
            
        

    # update everything
    pygame.display.update()
    clock.tick(60) # 60 frames per sec 



# Background Image Source: https://www.freevector.com/mountain-and-sky-landscape-18616
# Ground Image Source: https://gallery.yopriceville.com/Free-Clipart-Pictures/Grass-Grounds-Coverings-PNG-Clipart/Ground_PNG_Clip_Art_Image#.Yo5iBGDMKJE
# Bunny Image Source: https://www.pngitem.com/middle/ohxhiT_rabbit-cartoon-png-bunny-cartoon-png-transparent-png/
# Bee Image Source: https://www.pngitem.com/middle/JTTTJb_bee-555px-bumble-bee-animation-hd-png-download/
# Bee Image Source: https://www.pngitem.com/middle/hmRwhRi_teaching-and-learning-resources-honey-bee-animated-png/
# Bee Image Source: https://www.pngitem.com/middle/JTThii_cute-bee-png-cute-bee-clipart-transparent-png/
# Snail Image Source: https://www.pngitem.com/middle/wJiToo_cartoon-snail-public-domain-image-hd-photo-clipart/
