# MyLibrary.py

import sys, time, random, math, pygame
from pygame.locals import *


# prints text using the supplied font
def print_text(font, x, y, text, color=(0,0,0)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface() #req'd when function moved into MyLibrary
    screen.blit(imgText, (x,y))

# MySprite class extends pygame.sprite.Sprite
class MySprite(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0,0.0) 

    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)
        

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename)
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)


#Point class
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"


#Convert ticks to seconds: 1 tick == 0.001 sec
def ticks2sec(ticks):
    return ticks * 0.0001


#Convert seconds to ticks: 1 sec == 100 ticks 
def sec2ticks(seconds):
    return seconds * 1000

#angle to direction
def angle2direction(angle):
    direction=None
    if angle<45 and angle>=315:
        direction = 0
    elif angle>=45 and angle<135:
        direction=1
    elif angle>=135 and angle<225:
        direction=2
    elif angle>=225 and angle<315:
        direction=3
    return direction
#create fish sprite
class Fish(MySprite):
    def __init__(self,setting):
        super(Fish, self).__init__()
        self.setting=setting
        color=random.randint(1,3)
        self.color=color
    def random_position(self):
        angle=random.randint(0,360)
        self.angle=angle
        self.direction = angle2direction(angle)
        speed=random.randint(2,6)
        self.fish_speed=speed
        if self.direction==0:
            positionx=random.randint(self.setting.screen_width/4,3*self.setting.screen_width/4)
            self.position = positionx, self.setting.screen_height
        elif self.direction==1:
            positiony=random.randint(self.setting.screen_height/4,3*self.setting.screen_height/4)
            self.position = -self.frame_width,positiony
        elif self.direction==2:
            positionx=random.randint(self.setting.screen_width/4,3*self.setting.screen_width/4)
            self.position = positionx,-self.frame_height
        elif self.direction==3:
            positiony=random.randint(self.setting.screen_height/4,3*self.setting.screen_height/4)
            self.position = self.setting.screen_width, positiony

        
