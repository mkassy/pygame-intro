import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,500))
# screen_rect = screen.get_rect()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 50) # arguments: font type, font size

sky_surf = pygame.image.load('graphics/sky.png').convert() # convert alpha removes alpha values
soil_surf = pygame.image.load('graphics/soil.jpg').convert() # convert makes game run faster

score_surf = test_font.render('My game', False, (64,64,64)) # test, AA, color(RGB or hex_color)
score_rect = score_surf.get_rect(center = (400,50))

snail_surf = pygame.image.load('graphics/snail.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (800,400))

player_surf = pygame.image.load('graphics/hiker.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (40,400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print('collision')

    # draw all our elements 
    screen.blit(sky_surf, (0,0))
    screen.blit(soil_surf, (0,400))
    pygame.draw.rect(screen,'#c0e8ec', score_rect) # takes 3+ arguments
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) # 4th arg is line width, 5th is border rounding
    # pygame.draw.line(screen, 'gold', (0,0), pygame.mouse.get_pos(), width=5)
    # pygame.draw.ellipse(screen, 'brown', pygame.Rect(50,200,100,100)) # pygame.Rect() arguments: left, top, width, height

    screen.blit(score_surf, score_rect)
    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)
    player_rect.left += 2
    if player_rect.left > 800: player_rect.right = 40
    screen.blit(player_surf,player_rect) 

    # if player_rect.colliderect(snail_rect):
    #     collision_text = test_font.render('Collision!!!', False, 'red')
    #     screen.blit(collision_text, (200,300))

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse_pos)):
    #     print(pygame.mouse.get_pressed())


    # update everything
    pygame.display.update()
    clock.tick(60) # 60 frames per sec 