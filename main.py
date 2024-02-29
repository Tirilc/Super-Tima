import pygame as pg
import sys
from settings import *
from sprites import *

#lager en plattform for bakken 
platform_list=[Platform(0,HEIGHT-40, WIDTH, 40)]

#lager et slott
castle = Castle(395,100,60,60)

castle_img=pg.image.load('slott.png')

castle_img=pg.transform.scale(castle_img, (60,60))

#legger inn tegning av spiller tima
player_img = pg.image.load('spiller.png')
player_img = pg.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

#indikerer level
level = 1

# Funksjon som viser level
def display_level():
    text_img = self.font.render(f"Level: {level}", True, BLACK)
    surface.blit(text_img, (20,20))


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
        
        #legger inn en font
        self.font = pg.font.SysFont('Poppins-Regular', 32)
        
        #intro bakgrunn
        self.intro_background =pg.image.load('intro_background.JPG')
        
        
    # Metode for å starte et nytt spill
    def new(self):
        # Lager spiller-objekt
        self.player = Player()
        
        
        #lager platformer
        i=0 
        while len(platform_list)<5:
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
        global collide_castle
        self.player.update()
        
        #sjekker om vi faller
        if self.player.vel[1] >0:
            collide_platform = False
            
            #sjekker om spilleren kolliderer med en platform
            for p in platform_list:
                if pg.Rect.colliderect(self.player.rect, p.rect):
                    collide_platform = True
                    break
            
            if pg.Rect.colliderect(self.player.rect, castle.rect) and not collide_castle:
                collide_castle = True
                #print("kolliderte med slott")
                self.player.pos[1] += HEIGHT - castle.rect.y - 100
                
                i = 0
                while i < len(platform_list):
                    platform_list[i].rect.y += HEIGHT - castle.rect.y - 100
                    if platform_list[i].rect.top >= HEIGHT:
                        del platform_list[i]
                    else:
                        i += 1
                   
                castle.rect.x = 220
                castle.rect.y = 70
                
            
                
            if collide_platform:
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
        self.screen.blit(castle_img, (castle.rect.x, castle.rect.y))
        
        # Tegner spilleren
        self.screen.blit(player_img, self.player.pos)
        
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    
    # Metode som viser start-skjerm
    def show_start_screen(self):
        intro=True
        
        title=self.font.render('Super TIMA', True, BLACK)
        title_rect=title.get_rect(x=10, y=10)
        
        text_img = self.font.render(f"Hei",True, BLACK)
        text_rect=text_img.get_rect(x=150,y=150)
        #self.screen.blit(text_img, (10,10))
        
        
        play_button = Button(10,50,100,50, WHITE, BLACK, 'Play', 32)
        
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    intro=False
                    self.running=False
                    
            mouse_pos=pg.mouse.get_pos()
            mouse_pressed=pg.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro=False
                
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(text_img, text_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pg.display.update()
        
        
collide_castle = False

# Lager et spill-objekt
game_object = Game()

# Spill-løkken
while game_object.running:
    game_object.show_start_screen()
    # Starter et nytt spill
    game_object.new()

pg.quit()
sys.exit()


