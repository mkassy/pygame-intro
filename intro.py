import pygame
from sys import exit

def display_score():
    current_time = pygame.time.get_ticks() - start_time # gets time in milliseconds
    score_surf = test_font.render(f'{current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect) # surface, and then pos

pygame.init()
screen = pygame.display.set_mode((800,500))
# screen_rect = screen.get_rect()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 50) # arguments: font type, font size
game_active = True
start_time = 0

sky_surf = pygame.image.load('graphics/sky.png').convert() # convert alpha removes alpha values
soil_surf = pygame.image.load('graphics/soil.jpg').convert() # convert makes game run faster

# score_surf = test_font.render('My game', False, (64,64,64)) # test, AA, color(RGB or hex_color)
# score_rect = score_surf.get_rect(center = (400,50))

snail_surf = pygame.image.load('graphics/snail.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (800,400))

player_surf = pygame.image.load('graphics/bunny.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (40,400))
player_gravity = 0

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
                start_time = pygame.time.get_ticks()

    if game_active:
        # draw all our elements   
        screen.blit(sky_surf, (0,0))
        screen.blit(soil_surf, (0,400))
        # pygame.draw.rect(screen,'#c0e8ec', score_rect) # takes 3+ arguments
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) # 4th arg is line width, 5th is border rounding
        # pygame.draw.line(screen, 'gold', (0,0), pygame.mouse.get_pos(), width=5)
        # pygame.draw.ellipse(screen, 'brown', pygame.Rect(50,200,100,100)) # pygame.Rect() arguments: left, top, width, height

        # screen.blit(score_surf, score_rect)
        display_score()

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
        screen.fill('Yellow')
        game_over = test_font.render('GAME OVER!!!', False, 'red')
        press_keyfont = pygame.font.Font('pixeltype/Pixeltype.ttf', 30)
        press_key = press_keyfont.render('Press space to continue.', False, 'orange')
        screen.blit(game_over,(300,200))
        screen.blit(press_key,(270,400))

    # update everything
    pygame.display.update()
    clock.tick(60) # 60 frames per sec 