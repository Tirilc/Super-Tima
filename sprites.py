import pygame as pg
from settings import *

class Player:
    def __init__(self):
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (
            20,
            HEIGHT - 40
        )
        
        self.pos = list(self.rect.center)
        self.vel = [0, 0]
        self.acc = [0, 0.8]
        
        #print(self.rect)
    
    def jump(self):
        self.vel[1] = -15
    
    def update(self):
        self.acc=[0,GRAVITY]
        keys=pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.acc[0]=-PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc[0]=PLAYER_ACC
            
            
        #friksjon
        self.acc[0] += self.vel[0]*PLAYER_FRICTION
            
        #bevegelseslikning i x-retning
        self.vel[0] += self.acc[0]
        self.pos[0] += self.vel[0] + 0.5*self.acc[0]
        
        # Bevegelseslikning i y-retning
        self.vel[1] += self.acc[1]
        self.pos[1] += self.vel[1] + 0.5*self.acc[1]
            
        #oppdaterer rektangelets posisjon
        self.rect.x = self.pos[0]
        self.rect.y= self.pos[1]

        # Sjekker kollisjon med sidene
        if self.pos[0] >= WIDTH - PLAYER_WIDTH:
              self.pos[0] = WIDTH - PLAYER_WIDTH
        if self.pos[0] <= 0:
             self.pos[0] = 0
        
class Platform:
    def __init__(self, x,y,w,h):
        self.image=pg.Surface((w,h))
        self.image.fill(BLACK)
    
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class Castle:
    def __init__(self, x,y,w,h):
        self.image = pg.Surface((w,h))
        self.image.fill(LIGHTBLUE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#player = Player()
