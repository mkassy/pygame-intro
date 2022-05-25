import pygame
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # gets time in milliseconds
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect) # surface, and then pos
    return current_time

pygame.init()
screen = pygame.display.set_mode((800,500))
# screen_rect = screen.get_rect()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 50) # arguments: font type, font size
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('graphics/sky.png').convert() # convert alpha removes alpha values
soil_surf = pygame.image.load('graphics/soil.jpg').convert() # convert makes game run faster

# score_surf = test_font.render('My game', False, (64,64,64)) # test, AA, color(RGB or hex_color)
# score_rect = score_surf.get_rect(center = (400,50))

snail_surf = pygame.image.load('graphics/snail.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (800,400))

player_surf = pygame.image.load('graphics/cute_bunny.png').convert_alpha()
player_surf = pygame.transform.rotozoom(player_surf,0,0.1)
player_rect = player_surf.get_rect(midbottom = (40,400))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/cute_bunny.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,0.5)
player_stand_rect = player_stand.get_rect(center = (400, 250))

game_name = test_font.render('Bunny Hopper',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 35)
game_message = game_message_font.render('Actions: Press the space bar to hop!', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 420))

press_key_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 25)
press_key = press_key_font.render('Press space to continue.', False, 'orange')
press_key_rect = press_key.get_rect(center = (400,450))


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
                snail_rect.left = 800
                player_rect.right = 0
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # draw all our elements   
        screen.blit(sky_surf, (0,0))
        screen.blit(soil_surf, (0,400))
        # pygame.draw.rect(screen,'#c0e8ec', score_rect) # takes 3+ arguments
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) # 4th arg is line width, 5th is border rounding
        # pygame.draw.line(screen, 'gold', (0,0), pygame.mouse.get_pos(), width=5)
        # pygame.draw.ellipse(screen, 'brown', pygame.Rect(50,200,100,100)) # pygame.Rect() arguments: left, top, width, height
        
        # screen.blit(score_surf, score_rect)
        score = display_score()

        snail_rect.x -= 4
        if snail_rect.right <= -100: snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 400: player_rect.bottom = 400
        player_rect.left += 2
        if player_rect.left > 800: player_rect.right = 40
        screen.blit(player_surf,player_rect)

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)

        score_message = game_message_font.render(f"Your score is: {score}",False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,420))
        screen.blit(game_name,game_name_rect)
        screen.blit(press_key,press_key_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)
            
        

    # update everything
    pygame.display.update()
    clock.tick(60) # 60 frames per sec 






# Bunny Image Source: https://www.pngitem.com/middle/ohxhiT_rabbit-cartoon-png-bunny-cartoon-png-transparent-png/

