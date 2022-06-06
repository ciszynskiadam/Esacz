import pygame, random
from pygame.locals import *

pygame.init()

vec = pygame.math.Vector2
WIDTH = 500
HEIGHT = 500
FPS = 60
pygame.display.set_caption('ęśąćż')

red = (200,0,0)

ACC_1J = 0.75
ACC_2J = 0.5
GRND_ACC = 1
JUMP = 15
GRAV = 0.5
FRIC = -0.15
ATCK = 30

over = 0
menu = 1

menu_jump = 0
menu_jump_randomizer = random.randint(500, 10000)

msc = 1
sfx = 1

text_font = pygame.font.Font(r'font\PublicPixel.ttf', 15)
text_font2 = pygame.font.Font(r'font\PublicPixel.ttf', 10)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

sumo1_texture = pygame.image.load(r'textures\sumo.png').convert_alpha()
sumo1_l = pygame.image.load(r'textures\sumo_l.png').convert_alpha()
sumo1_r = pygame.image.load(r'textures\sumo_r.png').convert_alpha()
sumo1_d = pygame.image.load(r'textures\sumo_d.png').convert_alpha()

sumo2_texture = pygame.image.load(r'textures\sumo2.png').convert_alpha()
sumo2_l = pygame.image.load(r'textures\sumo2_l.png').convert_alpha()
sumo2_r = pygame.image.load(r'textures\sumo2_r.png').convert_alpha()
sumo2_d = pygame.image.load(r'textures\sumo2_d.png').convert_alpha()

background_texture = pygame.image.load(r'textures\background.png').convert_alpha()
darken_texture = pygame.image.load(r'textures\darken2.png').convert_alpha()
darken_texture2 = pygame.image.load(r'textures\darken.png').convert_alpha()
darken_menu = pygame.image.load(r'textures\darken3.png').convert_alpha()

logo = pygame.image.load(r'textures\logo.png').convert_alpha()
redw = pygame.image.load(r'textures\redw.png').convert_alpha()
bluew = pygame.image.load(r'textures\bluew.png').convert_alpha()

pygame.display.set_icon(sumo2_d)

sumo1_jump1_sound = pygame.mixer.Sound(r'sounds\sumo_jump1.wav')
sumo1_jump2_sound = pygame.mixer.Sound(r'sounds\sumo_jump2.wav')
sumo1_attack_sound = pygame.mixer.Sound(r'sounds\sumo_atk.wav')
sumo1_death_sound = pygame.mixer.Sound(r'sounds\sumo_death.wav')
sumo2_jump1_sound = pygame.mixer.Sound(r'sounds\sumo2_jump1.wav')
sumo2_jump2_sound = pygame.mixer.Sound(r'sounds\sumo2_jump2.wav')
sumo2_attack_sound = pygame.mixer.Sound(r'sounds\sumo2_atk.wav')
sumo2_death_sound = pygame.mixer.Sound(r'sounds\sumo2_death.wav')
pygame.mixer.music.load(r'sounds\soundtrack.ogg')

music_volume = 0.4

def mute_sfx():
    global sfx
    sumo1_jump1_sound.set_volume(0)
    sumo1_jump2_sound.set_volume(0)
    sumo1_attack_sound.set_volume(0)
    sumo1_death_sound.set_volume(0)
    sumo2_jump1_sound.set_volume(0)
    sumo2_jump2_sound.set_volume(0)
    sumo2_attack_sound.set_volume(0)
    sumo2_death_sound.set_volume(0)
    sfx = 0

def unmute_sfx():
    global sfx
    sumo1_jump1_sound.set_volume(0.3)
    sumo1_jump2_sound.set_volume(0.3)
    sumo1_attack_sound.set_volume(0.5)
    sumo1_death_sound.set_volume(1.5)
    sumo2_jump1_sound.set_volume(0.3)
    sumo2_jump2_sound.set_volume(0.15)
    sumo2_attack_sound.set_volume(0.5)
    sumo2_death_sound.set_volume(1.5)
    sfx = 1

def mute_music():
    global msc, music_volume
    music_volume = 0
    pygame.mixer.music.set_volume(music_volume)
    msc = 0

def unmute_music():
    global msc, music_volume
    music_volume = 0.4
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    msc = 1

unmute_sfx()
unmute_music()

class Player(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.size = 30
        self.number = number
        if self.number == 1:
            self.texture = sumo1_texture
            self.pos = vec(WIDTH - 150, HEIGHT - 58)
        elif self.number == 2:
            self.texture = sumo2_texture 
            self.pos = vec(150, HEIGHT - 58)        
        self.rect = self.texture.get_rect()
        self.jumps = 0
        self.jumplimit = 2
        self.attacked = 0
        self.hit = 0

        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0,GRAV)

        pressed_keys = pygame.key.get_pressed()
        acc_x = 0
        if over == 0 and menu == 0:
            if self.number == 1:
                acc_x = pressed_keys[K_RIGHT] - pressed_keys[K_LEFT]
                if self.attacked == 0:
                    if acc_x == 0:
                        self.texture = sumo1_texture
                    if acc_x == -1:
                        self.texture = sumo1_l
                    if acc_x == 1:
                        self.texture = sumo1_r

            if self.number == 2:
                acc_x = pressed_keys[K_d] - pressed_keys[K_a]
                if self.attacked == 0:
                    if acc_x == 0:
                        self.texture = sumo2_texture
                    if acc_x == -1:
                        self.texture = sumo2_l
                    if acc_x == 1:
                        self.texture = sumo2_r
        
        if self.jumps == 0:
            self.acc.x = acc_x * GRND_ACC
        elif self.jumps == 1:
            self.acc.x = acc_x * ACC_1J
        else:
            self.acc.x = acc_x * ACC_2J

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc

        if  P2_HD.rect.colliderect(P1_HU.rect) or P1.rect.colliderect(P2.rect) and not P1_HD.rect.colliderect(P2_HU.rect):
            self.acc.x = 0

        move_xy = self.vel + 0.5 * self.acc

        self.pos += move_xy

        if self.pos.x > WIDTH + self.size / 2:
            self.pos.x = - self.size / 2
        if self.pos.x < -self.size / 2:
            self.pos.x = WIDTH + self.size / 2
        if self.pos.y > HEIGHT - 58:
            self.pos.y = HEIGHT - 58
            if self.attacked == 0:
                self.jumps = 0
            if self.acc.x != acc_x * GRND_ACC:
                self.acc.x = acc_x * GRND_ACC
        if self.pos.y < self.size / 2:
            self.pos.y = self.size / 2

        self.rect.midbottom = self.pos

        P1_HU.pos.x = P1.pos.x
        P1_HU.pos.y = P1.pos.y - self.size + 13
        P1_HD.pos.x = P1.pos.x
        P1_HD.pos.y = P1.pos.y

        P2_HU.pos.x = P2.pos.x
        P2_HU.pos.y = P2.pos.y - self.size + 13
        P2_HD.pos.x = P2.pos.x
        P2_HD.pos.y = P2.pos.y

        P1_HU.rect.midbottom = P1_HU.pos
        P2_HU.rect.midbottom = P2_HU.pos
        P1_HD.rect.midbottom = P1_HD.pos
        P2_HD.rect.midbottom = P2_HD.pos

    def jump(self):
        self.vel.y = -JUMP

    def attack(self):
        self.vel.y = ATCK


class Hitbox_Up(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((P1.size - 4, 14))
        self.surf.fill(red)
        self.rect = self.surf.get_rect()
        self.pos = vec(0,0)


class Hitbox_Down(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((P1.size, 14))
        self.surf.fill(red)
        self.rect = self.surf.get_rect()
        self.pos = vec(0,0)


P1 = Player(1)
P2 = Player(2)

P1_HU = Hitbox_Up()
P2_HU = Hitbox_Up()
P1_HD = Hitbox_Down()
P2_HD = Hitbox_Down()

players = pygame.sprite.Group()
players.add(P1)
players.add(P2)

others = pygame.sprite.Group()
others.add(P1_HU)
others.add(P1_HD)
others.add(P2_HU)
others.add(P2_HD)


def restart():
    global over, music_volume, won

    P1.hit = 0
    P1.pos = vec(WIDTH - 150, HEIGHT - 58)

    P2.hit = 0
    P2.pos = vec(150, HEIGHT - 58) 

    over = 0

    if msc == 1:
        music_volume = 0.4  
    else:
        music_volume = 0  

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_volume)  


background_rect = background_texture.get_rect()
background_rect.bottomright = (WIDTH,HEIGHT)

darken_rect = darken_texture.get_rect()
background_rect.bottomright = (WIDTH,HEIGHT)


while True:
    dt = pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            if menu == 1:
                if event.key == pygame.K_SPACE:
                    menu = 0
                    menu_jump = 0
                if event.key == pygame.K_COMMA:
                    if msc == 1:
                        mute_music()
                    else:
                        unmute_music()
                if event.key == pygame.K_PERIOD:
                    if sfx == 1:
                        mute_sfx()
                    else:
                        unmute_sfx()
            else:
                if over == 0:
                    if event.key == pygame.K_UP and P1.jumps < P1.jumplimit and not P1_HU.rect.colliderect(P2_HD.rect):
                        P1.jumps += 1
                        if P1.jumps == 1:
                            pygame.mixer.Sound.play(sumo1_jump1_sound)
                        if P1.jumps == 2:
                            pygame.mixer.Sound.play(sumo1_jump2_sound)
                        P1.jump()
                    if event.key == pygame.K_DOWN and P1.jumps > 0 and not P2_HU.rect.colliderect(P1_HD.rect) and not P1_HU.rect.colliderect(P2_HD.rect) and P1.attacked == 0:
                        P1.texture = sumo1_d
                        pygame.mixer.Sound.play(sumo1_attack_sound)
                        P1.attack()
                        P1.attacked = 1
                        P1_attack_counter = 0
                    if event.key == pygame.K_w and P2.jumps < P2.jumplimit and not P2_HU.rect.colliderect(P1_HD.rect):
                        P2.jumps += 1
                        if P2.jumps == 1:
                            pygame.mixer.Sound.play(sumo2_jump1_sound)
                        if P2.jumps == 2:
                            pygame.mixer.Sound.play(sumo2_jump2_sound)
                        P2.jump()
                    if event.key == pygame.K_s and P2.jumps > 0 and not P1_HU.rect.colliderect(P2_HD.rect) and not P2_HU.rect.colliderect(P1_HD.rect) and P2.attacked == 0:
                        P2.texture = sumo2_d
                        pygame.mixer.Sound.play(sumo2_attack_sound)
                        P2.attack()
                        P2.attacked = 1
                        P2_attack_counter = 0
                else:
                    if event.key == pygame.K_r:
                        restart()
                    if event.key == pygame.K_m:
                        restart()
                        menu = 1
                    
    P2.move()
    P1.move()

    if P1.attacked == 1 and P1_attack_counter < 750:
        P1_attack_counter += dt
        P1.acc.x *= 0.1
        P1.vel.x *= 0.5
        P1.jumps = 2
    else:
        P1.attacked = 0
    
    if P2.attacked == 1 and P2_attack_counter < 750:
        P2_attack_counter += dt
        P2.acc.x *= 0.1
        P2.vel.x *= 0.5
        P2.jumps = 2
    else:
        P2.attacked = 0

    screen.blit(background_texture, background_rect) 

    
    if (P1_HD.rect.colliderect(P2_HU.rect) or P2_HD.rect.colliderect(P1_HU.rect)) and not P1_HD.rect.colliderect(P2_HD.rect) and not P2_HU.rect.colliderect(P1_HU.rect) and P2.pos.y != P1.pos.y + P1.size and P1.pos.y != P2.pos.y + P2.size:
        if P1.rect.y <= P2.rect.y:
            P1.pos.y = P2.rect.top + 1
            P2.pos.y = P1.rect.bottom + P2.size
            P1.vel.y = 0
            P1.acc.y = 0
            P2.vel.x = 0
            P2.acc.x = 0
            P1.jumps = 2
            P2.jumps = 2
            if P2.hit == 0:
                pygame.mixer.Sound.play(sumo2_death_sound)
                darkened = 10
            P2.hit = 1
            over = 1
            
        else:
            P2.pos.y = P1.rect.top + 1
            P1.pos.y = P2.rect.bottom + P1.size
            P2.vel.y = 0
            P2.acc.y = 0
            P1.vel.x = 0
            P1.acc.x = 0
            P1.jumps = 2
            P2.jumps = 2
            if P1.hit == 0:
                pygame.mixer.Sound.play(sumo1_death_sound)
                darkened = 10
            P1.hit = 1
            over = 1

    if (P1.rect.colliderect(P2.rect) and not (P1_HD.rect.colliderect(P2_HU.rect) or P2_HD.rect.colliderect(P1_HU.rect))):
            if P1.pos.x < P2.pos.x:
                if P1.acc.x > 0 and P2.acc.x < 0:
                    P1.acc.x, P1.vel.x = 0, 0
                    P2.acc.x, P2.vel.x = 0, 0
                    P1.pos.x = P2.pos.x - P1.size
                    P2.pos.x = P1.pos.x + P2.size + 1
                if P1.acc.x > 0:
                    P1.acc.x, P1.vel.x = 0, 0
                    P1.pos.x = P2.pos.x - P1.size
                if P2.acc.x < 0:
                    P2.acc.x, P2.vel.x = 0, 0
                    P2.pos.x = P1.pos.x + P2.size
                if P1.vel.x > 0:
                    P1.acc.x, P1.vel.x = 0, 0
                    P1.pos.x = P2.pos.x - P1.size
                if P2.vel.x < 0:
                    P2.acc.x, P2.vel.x = 0, 0
                    P2.pos.x = P1.pos.x + P1.size
            else:
                if P1.acc.x < 0 and P2.acc.x > 0:
                    P1.acc.x, P1.vel.x = 0, 0
                    P2.acc.x, P2.vel.x = 0, 0
                    P1.pos.x = P2.pos.x + P1.size - 1
                    P2.pos.x = P1.pos.x - P1.size
                if P1.acc.x < 0:
                    P1.acc.x, P1.vel.x = 0, 0
                    P1.pos.x = P2.pos.x + P1.size
                if P2.acc.x > 0:
                    P2.acc.x, P2.vel.x = 0, 0
                    P2.pos.x = P1.pos.x - P2.size
                if P1.vel.x < 0:
                    P1.acc.x, P1.vel.x = 0, 0
                    P1.pos.x = P2.pos.x + P1.size
                if P2.vel.x > 0:
                    P2.acc.x, P2.vel.x = 0, 0
                    P2.pos.x = P1.pos.x - P2.size   

    for entity in players:
        screen.blit(entity.texture, entity.rect)
    
    if menu == 1:
        menu_jump += dt
        if menu_jump >= menu_jump_randomizer:
            coin = random.randint(1, 2)
            if coin == 1:
                P1.jump()
            else:
                P2.jump()
            menu_jump = 0
            menu_jump_randomizer = random.randint(500, 10000)

        text_surf = text_font.render('press SPACE to begin', True, (50, 50, 50))
        text_rect = text_surf.get_rect(center = (WIDTH/2, 250))

        if msc == 1:
            text_surf2 = text_font2.render('press "," to mute music', True, (50, 50, 50))
        else:
            text_surf2 = text_font2.render('press "," to unmute music', True, (50, 50, 50))
        text_rect2 = text_surf2.get_rect(center = (130, 325))

        if sfx == 1:
            text_surf3 = text_font2.render('press "." to mute sfx', True, (50, 50, 50))
        else:
            text_surf3 = text_font2.render('press "." to unmute sfx', True, (50, 50, 50))
        text_rect3 = text_surf3.get_rect(center = (380, 325))

        screen.blit(darken_menu, darken_rect)
        screen.blit(logo, logo.get_rect())
        screen.blit(text_surf, text_rect)
        screen.blit(text_surf2, text_rect2)
        screen.blit(text_surf3, text_rect3)
    
    #for entity in others:
        #screen.blit(entity.surf, entity.rect)

    if over == 1:
        if music_volume != 0:
            music_volume -= 0.05
        pygame.mixer.music.set_volume(music_volume)

        if darkened > 0:
            for i in range(0, 10 - darkened):
                screen.blit(darken_texture, darken_rect)
            darkened -= 2
            if P2.hit == 1:
                screen.blit(redw, redw.get_rect())
            if P1.hit == 1:
                screen.blit(bluew, bluew.get_rect())
        else:
            screen.blit(darken_texture2, darken_rect)
            if P2.hit == 1:
                screen.blit(redw, redw.get_rect())
            if P1.hit == 1:
                screen.blit(bluew, bluew.get_rect())

        text_surf = text_font.render('press "r" to restart', True, (200, 200, 200))
        text_rect = text_surf.get_rect(center = (WIDTH/2, 225))

        text_surf2 = text_font.render('press "m" to return to menu', True, (200, 200, 200))
        text_rect2 = text_surf2.get_rect(center = (WIDTH/2, 250))

        screen.blit(text_surf, text_rect)
        screen.blit(text_surf2, text_rect2)

    pygame.display.update()