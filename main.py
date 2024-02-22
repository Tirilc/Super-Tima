import pygame as pg
import sys
from settings import *
from sprites import *

#lager en plattform for bakken 
platform_list=[Platform(0,HEIGHT-40, WIDTH, 40)]

#lager et slott
castle = Castle(450,500,40,40)

class Game:
    def __init__(self):
        # Initiere pygame
        pg.init()

        # Lager hovedvinduet
        self.screen = pg.display.set_mode(SIZE)

        # Lager en klokke
        self.clock = pg.time.Clock()
        
        # Attributt som styrer om spillet skal kjøres
        self.running = True
        
        
    # Metode for å starte et nytt spill
    def new(self):
        # Lager spiller-objekt
        self.player = Player()
        
        #lager platformer
        i=0 
        while len(platform_list)<4:
            #lager en ny platform
            new_platform=Platform(
                PLATFORM_X[i],
                PLATFORM_Y[i],
                100,
                20
                
            )
            i+= 1
            
            safe=True
            
            #sjekker om den nye platformen kolliderer med de gamle
            for p in platform_list:
                if pg.Rect.colliderect(new_platform.rect, p.rect):
                    safe=False
                    break
            if safe:
                #legger i lista
                platform_list.append(new_platform)
            else:
                print("platformen kolliderte, prøver på nytt")
        
        self.run()
        
    
    # Metode som kjører spillet
    def run(self):
        # Game loop
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
        
    # Metode som håndterer hendelser
    def events(self):
        # Går gjennom hendelser (events)
        for event in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False # Spillet skal avsluttes
                
            if event.type == pg.KEYDOWN:
                # Spilleren skal hoppe hvis vi trykker på mellomromstasten
                if event.key == pg.K_SPACE:
                    self.player.jump()
    
    # Metode som oppdaterer
    def update(self):
        self.player.update()
        
        #sjekker om vi faller
        if self.player.vel[1] >0:
            collide=False
            
            #sjekker om spilleren kolliderer med en platform
            for p in platform_list:
                if pg.Rect.colliderect(self.player.rect, p.rect):
                    collide=True
                    break
                
            if collide:
                self.player.pos[1] = p.rect.y-PLAYER_HEIGHT
                self.player.vel[1]=0
            
    
    # Metode som tegner ting på skjermen
    def draw(self):
        # Fyller skjermen med en farge
        self.screen.fill(WHITE)
        
        #tegner platofrmene
        for p in platform_list:
            self.screen.blit(p.image, (p.rect.x, p.rect.y))

        #tegner slott
        self.screen.blit(castle.image, (400, 100))
        
        # Tegner spilleren
        self.screen.blit(self.player.image, self.player.pos)
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    
    # Metode som viser start-skjerm
    def show_start_screen(self):
        pass
        
        
# Lager et spill-objekt
game_object = Game()

# Spill-løkken
while game_object.running:
    # Starter et nytt spill
    game_object.new()

pg.quit()
