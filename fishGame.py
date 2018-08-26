import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *
from pygame.sprite import Sprite

def calc_velocity(direction, vel=1.0):
    velocity = Point(0,0)
    if direction == 0: #north
        velocity.y = -vel
    elif direction == 1: #east
        velocity.x = vel
    elif direction == 2: #south
        velocity.y = vel
    elif direction == 3: #west
        velocity.x = -vel
    return velocity

def reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 6:
        sprite.direction = 2

def reverse_angle(angle):
    angle+=90
    if angle>=360:
        angle-=360
    return angle

def load_image(num):
    image=MySprite()
    image.num=num
    if num==0:
        image.load("data/E.png", 32, 32, 1)
    elif num==1:
        image.load("data/A.png", 32, 32, 1)
    elif num==2:
        image.load("data/S.png", 32, 32, 1)
    return image
#create setting
class Setting():
    def __init__(self):
        self.screen_width=800
        self.screen_height=600
        self.E=100
        self.A=100
        self.S=100
        self.boss_coming=False
        self.boss_head_coming=False
        self.boss_time=False
        self.bosspart_1=False;self.bosspart_2=False;self.bosspart_3=False
        self.bubble_speed=10;
        self.bosspart_2_attack=False
        self.bubble_del=False
        self.boss_health=self.boss_health_now=500
        self.boss_attack_time=3
        self.boss_attack_strong=3
        self.boss_attack_old_strong=3
        self.next_attack=False
        self.next=True
        self.first_start=True
        self.first_init=True

#main program begins
pygame.init()
setting=Setting()
screen = pygame.display.set_mode((setting.screen_width,setting.screen_height))
pygame.display.set_caption("Find Kun")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()
current_time=0

#create sprite groups
player_group = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
ability_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
boss_head_group=pygame.sprite.Group()
bubble_group=pygame.sprite.Group()

#create button sprite
class Button():
    """docstring for Button"""
    def __init__(self, setting,screen,msg):
        self.msg=msg
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.setting = setting
        self.width=200
        self.height=50
        self.rect=pygame.Rect(0,0,200,50)
        self.button_color=(100,100,250)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)
        self.rect.center=self.screen_rect.center
        self.prep_msg(self.msg)
    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

#create bullet sprite
class Bullet(Sprite):
    def __init__(self, player):
        super(Bullet, self).__init__()
        self.image=pygame.image.load('data/bullet.png')
        self.rect=self.image.get_rect()
        self.player = player
        self.direction=0
        self.rect.centerx=self.player.rect.centerx
        self.rect.centery=self.player.rect.centery

#create bubble sprite
class Bubble(Sprite):
    def __init__(self):
        super(Bubble, self).__init__()
        self.image=pygame.image.load('data/bubble.png')
        self.rect=self.image.get_rect()
        self.rect.centery=setting.screen_height/2
        self.rect.centerx=50

background=pygame.image.load('data/background.png')
background_rect=background.get_rect()
#Init
game_over = True
game_win = False
player_moving = False
player_health = 100
last_z = bullet_last = boss_last= pygame.time.get_ticks()
#repeating loop
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_x, mouse_y):
                game_over = False
                last_time= pygame.time.get_ticks()
    #clear the screen
    screen.blit(background,background_rect)

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: sys.exit()
        elif keys[K_UP] or keys[K_w]:
            player.direction = 0;
            player_moving = True
        elif keys[K_RIGHT] or keys[K_d]:
            player.direction = 1
            player_moving = True
        elif keys[K_DOWN] or keys[K_s]:
            player.direction = 2
            player_moving = True
        elif keys[K_LEFT] or keys[K_a]:
            player.direction = 3
            player_moving = True
        elif keys[K_SPACE]:
            bullet_current = pygame.time.get_ticks()
            if len(bullet_group)<=6 and ticks2sec(bullet_current - bullet_last) >= -0.00014*(setting.A-100)+0.15:
                new_bullet=Bullet(player)
                new_bullet.direction=player.last_direction
                bullet_last=bullet_current
                bullet_group.add(new_bullet)
        else:
            player_moving = False
        if setting.first_init:
            setting.first_init=False
            #create the player sprite
            player = MySprite()
            player.load("data/fish_all.png", 120, 71, 4)
            player.position = setting.screen_width-player.frame_width, (setting.screen_height-player.frame_height)/2
            player.direction = 0
            player.last_direction=3
            player_group.add(player)

            #create the fish sprite
            for n in range(0, 3):
                color=random.randint(1,3)
                fish = Fish(setting)
                if fish.color==1:
                    fish.load("data/green_fish_all.png", 120, 80,2)
                elif fish.color==2:
                    fish.load("data/blue_fish_all.png", 120, 76.5, 2)
                elif fish.color==3:
                    fish.load("data/red_fish_all.png", 120, 54.5, 2)
                fish.random_position()
                fish_group.add(fish)
        #set animation frames based on player's direction
        if player.direction==1:
            player.last_direction=player.direction
            player.first_frame = 0 * player.columns
            player.last_frame = player.first_frame + player.columns-1
        elif player.direction==3:
            player.last_direction=player.direction
            player.first_frame = 1 * player.columns
            player.last_frame = player.first_frame + player.columns-1
        else:
            if player.last_direction==1:
                player.first_frame=0;player.last_frame=3
            elif player.last_direction==3:
                player.first_frame=player.columns;player.last_frame=player.columns+3

        

        if player.frame < player.first_frame:
            player.frame = player.first_frame

        if not player_moving:
            #stop animating when player is not pressing a key
            player.frame = player.first_frame = player.last_frame
        else:
            #move player in direction 
            player.velocity = calc_velocity(player.direction, 1.5)
            player.velocity.x *= 2.5+setting.A/1000
            player.velocity.y *= 2.5+setting.A/1000

        #update player sprite
        player_group.update(ticks, 50)

        #manually move the player
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0: player.X = 0
            elif player.X > setting.screen_width-player.frame_width: player.X = setting.screen_width-player.frame_width
            if player.Y < 0: player.Y = 0
            elif player.Y > setting.screen_height-player.frame_height: player.Y = setting.screen_height-player.frame_height
        
        #add new fish every 10 seconds
        current = pygame.time.get_ticks()
        if ticks2sec(current - last_z) >= .50:
            if len(fish_group)<12:
                for i in range(0,3):
                    fish = Fish(setting)
                    if fish.color==1:
                        fish.load("data/green_fish_all.png", 120, 80,2)
                    elif fish.color==2:
                        fish.load("data/blue_fish_all.png", 120, 76.5, 2)
                    elif fish.color==3:
                        fish.load("data/red_fish_all.png", 120, 54.5, 2)
                    fish.random_position()
                    fish_group.add(fish)
            last_z = current


        #manually iterate through all the fishes
        for z in fish_group:
            if 0<=z.angle<90 or 360>z.angle>270:
                z.first_frame = 1 * z.columns
                z.last_frame = z.first_frame + z.columns-1
            elif 90<=z.angle<=270:
                z.first_frame = 0 * z.columns
                z.last_frame = z.first_frame + z.columns-1
 
            if z.frame < z.first_frame:
                z.frame = z.first_frame 
            
            if z.X < -z.frame_width or z.X > setting.screen_width:
                z.angle=180-z.angle
            elif z.Y < -z.frame_height or z.Y > setting.screen_height:
                z.angle=360-z.angle

            if z.angle>=360:
                z.angle-=360
            elif z.angle<0:
                z.angle+=360
            #keep the fish on the screen        
            z.X += z.fish_speed *math.cos(math.radians(z.angle))
            z.Y += z.fish_speed *math.sin(math.radians(z.angle))*-1
        #update fish sprites
        fish_group.update(ticks, 200)         
        #update bullet_group
        if bullet_group:
            for bullet in bullet_group.copy():
                if bullet.direction==1:
                    bullet.rect.centerx+=setting.S/10
                    if bullet.rect.centerx>setting.screen_width:
                        bullet_group.remove(bullet)
                elif bullet.direction==3:
                    bullet.rect.centerx-=setting.S/10
                    if bullet.rect.centerx<0:
                        bullet_group.remove(bullet)

        #check for player collision with fish
        attacker = None
        attacker = pygame.sprite.spritecollideany(player, fish_group)
        if attacker != None:
            #we got a hit, now do a more precise check
            if pygame.sprite.collide_rect_ratio(0.5)(player,attacker):
                player_health -= 10
                if attacker.rect.centerx <= player.rect.centerx:   player.rect.centerx += 20
                elif attacker.rect.centerx > player.rect.centerx: player.rect.centerx -= 20
                if attacker.rect.centery <= player.rect.centery:   player.rect.centery += 20
                elif attacker.rect.centery > player.rect.centery: player.rect.centery -= 20
            else:
                attacker = None

        #check bullet collision with fish
        for bullet in bullet_group:
            kill=pygame.sprite.spritecollideany(bullet,fish_group)
            if kill!=None:
                if pygame.sprite.collide_rect_ratio(0.5)(bullet,kill):
                    if kill.color==1:
                        ability=load_image(0)
                    elif kill.color==2:
                        ability=load_image(1)
                    elif kill.color==3:
                        ability=load_image(2)
                    fish_group.remove(kill)
                    bullet_group.remove(bullet)
                    ability.num=kill.color-1
                    ability.X = kill.rect.centerx
                    ability.Y = kill.rect.centery
                    ability_group.add(ability)

        #check bubble collision with boss_head
        if setting.bosspart_2:
            shoted=None
            shoted=pygame.sprite.spritecollideany(boss_head,bullet_group)
            if shoted !=None:
                if pygame.sprite.collide_rect_ratio(0.5)(boss_head,shoted):
                    bullet_group.remove(shoted)
                    boss_head.health -= setting.S/10
                    setting.boss_health_now = boss_head.health

        #check bubble collision with player
        shoted=None
        shoted=pygame.sprite.spritecollideany(player,bubble_group)
        if shoted !=None:
            if pygame.sprite.collide_rect_ratio(0.5)(player,shoted):
                bubble_group.remove(shoted)
                if shoted.rect.centerx <= player.rect.centerx:   player.rect.centerx += 10
                elif shoted.rect.centerx > player.rect.centerx: player.rect.centerx -= 10
                if shoted.rect.centery <= player.rect.centery:   player.rect.centery += 10
                elif shoted.rect.centery > player.rect.centery: player.rect.centery -= 10
                player_health -= 10
        #check for collision with ability
        for ability in ability_group.copy():
            change = None
            change = pygame.sprite.spritecollideany(player, ability_group)
            if change != None:
                if pygame.sprite.collide_rect_ratio(0.5)(player, ability):
                    if ability.num==0:
                        player_health += 10
                        setting.E += 5
                        if player_health > setting.E: player_health = setting.E
                        ability_group.remove(ability)
                    elif ability.num==1:
                        if setting.A<1000: setting.A += 40;
                        else: setting.A=1000
                        ability_group.remove(ability)
                    elif ability.num==2:
                        setting.S += 10
                        ability_group.remove(ability)
                else:
                    change = None
        #update the health drop
        ability_group.update(ticks, 50)
        #boss coming
        boss_current = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        second=(current_time-last_time)/1000
        if second>=60 and not setting.boss_time:
            fish_group.empty()
            bullet_group.empty()
            ability_group.empty()
            setting.boss_coming=True
            setting.boss_time=True

            #create boss sprite
            boss=MySprite()
            boss.load("data/boss_left.png", 553, 400, 4)
            boss.position=setting.screen_width-100,setting.screen_height/2-200
            boss.direction=0
            boss_group.add(boss)
        #boss swimming
        if setting.boss_coming:  
            if boss.direction==0:
                boss.X-=20;
                if boss.X<-100:
                    #create boss head sprite
                    boss_head=MySprite()
                    boss_head.load("data/boss_head.png", 120, 295, 8)
                    boss_head.position=-100,setting.screen_height/2-150
                    boss_head.direction=0
                    boss_head.health=setting.boss_health_now
                    boss_head_group.add(boss_head)
                    boss_group.empty()
                    boss=None
                    setting.next=True
                    setting.boss_head_coming=True
                    setting.boss_coming=False;setting.bosspart_1=True
            elif boss.direction==2:
                boss.X+=20;
                if boss.X>setting.screen_width+100:
                    #create boss head sprite
                    boss_head=MySprite()
                    boss_head.load("data/boss_head_right.png", 120, 295, 8)
                    boss_head.position=setting.screen_width,setting.screen_height/2-150
                    boss_head.direction=2
                    boss_head.health=setting.boss_health_now
                    boss_head_group.add(boss_head)
                    boss_group.empty()
                    boss=None
                    setting.next=True
                    setting.boss_head_coming=True
                    setting.boss_coming=False;setting.bosspart_1=True
            
        #boss attack
        if setting.boss_head_coming:
            if setting.bosspart_1:
                bosspart_1_cureent = pygame.time.get_ticks()
                if boss_head.direction==0:
                    boss_head.X+=5;
                    if boss_head.X>=0:
                        boss_head.position=0,setting.screen_height/2-150
                        setting.bosspart_1=False
                        setting.bosspart_2=True
                elif boss_head.direction==2:
                    boss_head.X-=5;
                    if boss_head.X<=setting.screen_width-100:
                        boss_head.position=setting.screen_width-100,setting.screen_height/2-150
                        setting.bosspart_1=False
                        setting.bosspart_2=True
            elif setting.bosspart_2:
                bosspart_2_cureent = pygame.time.get_ticks()
                if setting.boss_attack_time>=0 and setting.next:
                    if ticks2sec(bosspart_2_cureent - bosspart_1_cureent)>0.2:
                        bosspart_1_cureent=bosspart_2_cureent
                        bosspart_2_last=bosspart_2_cureent
                        setting.boss_attack_time-=1
                        setting.next_attack=True
                        setting.next=False
                elif setting.boss_attack_time<0:
                    boss=MySprite()
                    if boss_head.direction==0:
                        boss.load("data/boss_right.png", 553, 400, 4)
                        boss.position=-553,setting.screen_height/2-200
                        boss.direction=2
                        boss_group.add(boss)
                    elif boss_head.direction==2:
                        boss.load("data/boss_left.png", 553, 400, 4)
                        boss.position=setting.screen_width-100,setting.screen_height/2-200
                        boss.direction=0
                    boss_group.add(boss)
                    setting.boss_coming=True
                    setting.boss_head_coming=False
                    setting.bosspart_2=setting.bosspart_1=False
                    setting.next_attack=False
                    setting.boss_attack_time=3  
                    if setting.boss_attack_old_strong<10:
                        setting.boss_attack_strong=setting.boss_attack_old_strong+1
                    setting.boss_attack_old_strong=setting.boss_attack_strong
                    boss_head_group.empty()
                    boss_head=None
                if setting.next_attack and ticks2sec(bosspart_2_cureent - bosspart_2_last)>0.02:
                    bosspart_2_last=bosspart_2_cureent
                    if setting.boss_attack_strong>0:
                        setting.boss_attack_strong-=1
                        bubble_num=10
                        for b in range(0,bubble_num+1):
                            bubble=Bubble()
                            bubble.angle=b*(180/bubble_num)-90
                            if boss_head.direction==0:
                                bubble.direction=0
                                bubble.rect.centerx=50
                            elif boss_head.direction==2:
                                bubble.direction=2;
                                bubble.rect.centerx=setting.screen_width-50   
                            bubble_group.add(bubble)
                    else:
                        setting.boss_attack_strong=setting.boss_attack_old_strong 
                        setting.next=True
                        setting.next_attack=False
        if setting.boss_time:
            boss_group.update(ticks, 500)
            boss_head_group.update(ticks, 100)
            for bub in bubble_group.copy():
                if bub.direction==0:
                    bub.rect.x+=(setting.bubble_speed*math.cos(math.radians(bub.angle)))
                    bub.rect.y+=(setting.bubble_speed*math.sin(math.radians(bub.angle)))
                    if bub.rect.x>setting.screen_width or bub.rect.y>setting.screen_height or bub.rect.y<0:
                        bubble_group.remove(bub)
                elif bub.direction==2:
                    bub.rect.x-=(setting.bubble_speed*math.cos(math.radians(bub.angle)))
                    bub.rect.y+=(setting.bubble_speed*math.sin(math.radians(bub.angle)))
                    if bub.rect.x<0 or bub.rect.y>setting.screen_height or bub.rect.y<0:
                        bubble_group.remove(bub)
            #is player dead?
        if player_health <= 0 :
            game_over = True
        if setting.boss_head_coming:
            if boss_head!=None and boss_head.health<=0:
                game_over = True    
        #draw sprites
        ability_group.draw(screen)
        fish_group.draw(screen)
        player_group.draw(screen)
        boss_group.draw(screen)
        bullet_group.draw(screen)
        boss_head_group.draw(screen)
        bubble_group.draw(screen)
        if 0<=second<=60:
            print_text(font, setting.screen_width-100,20, str(int(60-second)))

        #draw E bar
        pygame.draw.rect(screen, (50,150,50), Rect(20,510,player_health,25))
        pygame.draw.rect(screen, (100,200,100), Rect(20,510,setting.E,25), 2)
        #draw A bar
        pygame.draw.rect(screen, (50,50,250), Rect(20,540,setting.A/5+80,25))
        #draw S bar
        pygame.draw.rect(screen, (250,50,50), Rect(20,570,setting.S/5+80,25))
        #draw boss bar
        if setting.boss_head_coming:
            pygame.draw.rect(screen, (250,50,50), Rect(100,20,setting.boss_health_now,25))
            pygame.draw.rect(screen, (250,100,100), Rect(100,20,setting.boss_health,25), 2)
        if game_over:
            print_text(font, 300, 100, "G A M E   O V E R")
            game_over=True
            setting.first_start=True
            setting.first_init=True
        if game_win:
            print_text(font, 300, 100, "G A M E   W I N")
            setting.first_start=True
            setting.first_init=True
            game_over=True
    elif game_over:
        if setting.first_start:
            button=Button(setting,screen,'play')
        print_text(font, 160, 100, "You want save your polluted hometown")
        print_text(font, 40, 140, "An old man told you to find a solution by looking for 'KUN'")
        print_text(font, 60, 180, "So you embarked on a dangerous road to find the 'KUN'")
        button.draw_button()
        ability_group.empty()
        fish_group.empty()
        player_group.empty()
        boss_group.empty()
        bullet_group.empty()
        boss_head_group.empty()
        bubble_group.empty()
        setting=None
        setting=Setting()
        setting.first_start=False
        player_health=100
        last_time=current_time
    '''
    elif game_win:
        print_text(font, 40, 200, "Squid tells you that he is not the ‘KUN’ you are looking for")    
        ability_group.empty()
        fish_group.empty()
        player_group.empty()
        boss_group.empty()
        bullet_group.empty()
        boss_head_group.empty()
        bubble_group.empty()
    '''
    pygame.display.update()
