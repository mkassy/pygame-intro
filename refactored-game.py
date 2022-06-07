import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # initializes the sprite class so we can access it 

        player_walk_1 = pygame.image.load('graphics/png/cat/Walk (1).png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/png/cat/Walk (2).png').convert_alpha()

        org_player_walk = [player_walk_1, player_walk_2]
        self.player_walk = []
        
        # Scaled images
        for player in org_player_walk:
            player = pygame.transform.rotozoom(player,0,0.2)
            self.player_walk.append(player)
  
        self.player_index = 0

        self.player_jump = pygame.image.load('graphics/png/cat/Jump (8).png').convert_alpha()
        self.player_jump = pygame.transform.rotozoom(self.player_jump,0,0.2)

        self.player_slide = pygame.image.load('graphics/png/cat/Slide (11).png').convert_alpha()
        self.player_slide = pygame.transform.rotozoom(self.player_slide,0,0.2)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,400))
        self.gravity = 0 

        self.jump_sound = pygame.mixer.Sound('jump.mp3')
        self.jump_sound.set_volume(0.5) # 1 is the highest volume 



    def make_player_jump(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom >= 400:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.gravity = -20
                self.jump_sound.play()

        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400


    def animation_state(self):
        if self.rect.bottom < 400:
            self.image = self.player_jump
        else: 
            self.make_player_walk()

        if (pygame.key.get_pressed()[pygame.K_DOWN]) and self.rect.bottom >= 400:
            self.make_player_slide() 


    def make_player_walk(self):
        self.player_index += 0.1

        if self.player_index >= len(self.player_walk):
            self.player_index = 0

        self.image = self.player_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom = (80,400))

    def make_player_slide(self):
        self.image = self.player_slide
        self.rect = self.image.get_rect(midbottom = (80,400))
    

    def update(self):
        self.make_player_jump()
        self.apply_gravity()
        self.animation_state()


    # Note: We cannot draw sprites by calling screen.blit so we must place them in a group or group single
    # When we call them, we must call the update method after 
    # player = pygame.sprite.GroupSingle()
    # player.add(Player())

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'bird':
            bird_fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            bird_fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()

            bird_list = [bird_fly_1, bird_fly_2]
            self.frames = []

            # Transforming bird images
            for frame in bird_list:
                frame = pygame.transform.rotozoom(frame,0,0.1)
                frame = pygame.transform.flip(frame,True,False)
                self.frames.append(frame)

            y_pos = 315

            self.bird_frame_index = 0
            self.image = self.frames[self.bird_frame_index]

        if type == 'snail':
            self.image = pygame.image.load('graphics/snail.png').convert_alpha()
            y_pos = 400
            
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))


    def animation_state(self):
        if type == 'bird':
            self.bird_frame_index += 0.1
            if self.bird_frame_index >= len(self.frames): self.bird_frame_index = 0 
            self.image = self.frames[int(self.bird_frame_index)]


    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # gets time in milliseconds
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect) # surface, and then pos
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 50) # arguments: font type, font size
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('music.wav')
bg_music.play(loops = -1) # -1 plays pygame to play this sound forever 

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# Loading background images 
sky_surf = pygame.image.load('graphics/sky.png').convert() # convert alpha removes alpha values
ground_surf = pygame.image.load('graphics/ground3.png').convert() # convert makes game run faster
ground_surf = pygame.transform.scale(ground_surf, (1000,100))

# Intro screen
player_stand = pygame.image.load('graphics/png/cat/Run (7).png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,0.5)
player_stand_rect = player_stand.get_rect(center = (400, 250))

game_name = test_font.render("Leo's Fun Adventure!",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 35)
game_message = game_message_font.render('Actions: Press the space bar to jump!', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 420))

press_key_font = pygame.font.Font('pixeltype/Pixeltype.ttf', 25)
press_key = press_key_font.render('Press space to continue.', False, 'orange')
press_key_rect = press_key.get_rect(center = (400,450))

# Timer
obstacle_timer = pygame.USEREVENT + 1 # always add plus 1 
pygame.time.set_timer(obstacle_timer,1600) # 2 arguments (what event you want to trigger, how many ms)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bird','snail', 'snail', 'snail']))) # 75% chance to get snail 
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:
        # draw all our elements   
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,400))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        game_active = collision_sprite()

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



# Background Image Source: https://www.freevector.com/mountain-and-sky-landscape-18616
# Ground Image Source: https://gallery.yopriceville.com/Free-Clipart-Pictures/Grass-Grounds-Coverings-PNG-Clipart/Ground_PNG_Clip_Art_Image#.Yo5iBGDMKJE
# Bunny Image Source: https://www.pngitem.com/middle/ohxhiT_rabbit-cartoon-png-bunny-cartoon-png-transparent-png/
# Bee Image Source: https://www.pngitem.com/middle/JTTTJb_bee-555px-bumble-bee-animation-hd-png-download/
# Bee Image Source: https://www.pngitem.com/middle/hmRwhRi_teaching-and-learning-resources-honey-bee-animated-png/
# Bee Image Source: https://www.pngitem.com/middle/JTThii_cute-bee-png-cute-bee-clipart-transparent-png/
# Snail Image Source: https://www.pngitem.com/middle/wJiToo_cartoon-snail-public-domain-image-hd-photo-clipart/
