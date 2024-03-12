import pygame as pg
import sys
import random
from pygame import mixer
from settings import *
from sprites import *


# lager lister
platform_list = [Platform(0, HEIGHT-40, WIDTH, 40)]
money_list =[Money(random.randint(0,460),random.randint(40,560),WIDTH,HEIGHT)]

# lager et slott
castle = Castle(395, 100, 60, 60)

castle_img = pg.image.load('slott.png')

castle_img = pg.transform.scale(castle_img, (60, 60))

# legger inn tegning av spiller tima
player_img = pg.image.load('spiller.png')
player_img = pg.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

#lager penger
money=Money(250,150,150,100)

money_img=pg.image.load('penger.png')

money_img=pg.transform.scale(money_img, (60,60))

#henter bilde til bakgrunn
background_img= pg.image.load('bakgrunnsbilde.JPG')

#tilpasser bakgrunnsbildet vår skjemstørrelse
background_img=pg.transform.scale(background_img, SIZE)


#initialiserer mixer
mixer.init()

#legger inn lyd
jump_sfx= pg.mixer.Sound('jump.mp3')
intro_sfx=pg.mixer.Sound('intro.mp3')
slott_sfx =pg.mixer.Sound('slott.mp3')
money_sfx=pg.mixer.Sound('money.mp3')

# indikerer level
poeng = 0


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

        # legger inn en font
        self.font = pg.font.SysFont('Poppins-Regular', 32)

        # intro bakgrunn
        self.intro_background = pg.image.load('intro_background.JPG')

    # Funksjon som viser level
    def display_poeng(self):
        text_img = self.font.render(f"Poeng: {poeng}", True, BLACK)
        self.screen.blit(text_img, (20,20))

    # Metode for å starte et nytt spill
    def new(self):
        # Lager spiller-objekt
        self.player = Player()

        # lager platformer
        i = 0
        while len(platform_list) < 5:
            # lager en ny platform
            new_platform = Platform(
                PLATFORM_X[i],
                PLATFORM_Y[i],
                100,
                20

            )
            i += 1

            safe = True

            # sjekker om den nye platformen kolliderer med de gamle
            for p in platform_list:
                if pg.Rect.colliderect(new_platform.rect, p.rect):
                    safe = False
                    break
            if safe:
                # legger i lista
                platform_list.append(new_platform)
            else:
                print("platformen kolliderte, prøver på nytt")

        #lager nye penger
        while len(money_list) < 10:
            # lager en ny penge
            new_money = Money(random.randint(0,460),random.randint(40,560),WIDTH,HEIGHT)
            i += 1
            
            money_list.append(new_money)

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
                self.running = False  # Spillet skal avsluttes

            if event.type == pg.KEYDOWN:
                # Spilleren skal hoppe hvis vi trykker på mellomromstasten
                if event.key == pg.K_SPACE and self.jump_count<=1:
                    self.player.jump()
                    jump_sfx.play()
                    self.jump_count+=1

                
    
    # Metode som oppdaterer
    def update(self):
        global collide_castle
        global collide_platform
        global poeng
        self.player.update()

        
        for p in platform_list:
            if pg.Rect.colliderect(p.rect, castle.rect):
                p.image.fill(RED)
        
        #sjekker om vi faller
        if self.player.vel[1] >0:
            collide_platform = False
            
            #sjekker om spilleren kolliderer med en platform
            for p in platform_list:
                if pg.Rect.colliderect(self.player.rect, p.rect):
                    collide_platform = True
                    self.jump_count=0
                    break

             if collide_platform:
                self.player.pos[1] = p.rect.y-PLAYER_HEIGHT
                self.player.vel[1]=0

        
        #sjekker om vi står stille
        if self.player.vel[1]<=0: 

            #sjekker om spiller kolliderer med slottet
            if pg.Rect.colliderect(self.player.rect, castle.rect) and not collide_castle:
                collide_castle = True
                slott_sfx.play()
                #print("kolliderte med slott")
                poeng+=1
                self.player.pos[1] += HEIGHT - castle.rect.y - 100

                
                i = 0
                while i < len(platform_list):
                    platform_list[0].image.fill(RED)
                    platform_list[i].rect.y += HEIGHT - castle.rect.y - 100
                    if platform_list[i].rect.top >= HEIGHT:
                        del platform_list[i]
                        
                    else:
                        i += 1
                
    
                
                castle.rect.x = random.randint(20, 380)
                castle.rect.y = 70
                
                platform_castle = Platform(castle.rect.x - 20 ,castle.rect.y + 60,100,20)
                platform_list.append(platform_castle)
                platform_castle.image.fill(RED)
                collide_castle = False
                
                #legge til nye platformer
                while len(platform_list) < 7: #5 platformer å hoppe på til slottet
                    new = Platform(random.randint(0,WIDTH-100),random.randint(castle.rect.y +60, 470),100,20)
                    
                    safe=True
            
                    #sjekker om den nye platformen kolliderer med de gamle
                    for p in platform_list:
                        if pg.Rect.colliderect(new.rect, p.rect):
                            safe=False
                            break
                    if safe:
                    #legger i lista
                        platform_list.append(new)
                    else:
                        print("platformen kolliderte, prøver på nytt")
                    
                      
        #sjekker kollisjon med bunn
        if self.player.pos[1] + PLAYER_HEIGHT >= HEIGHT:
            #print("game over")
            pg.quit()
            sys.exit()
            print("game over")
               
                
    # Metode som tegner ting på skjermen
    def draw(self):
        #bruker bakgrundsbildet
        self.screen.blit(background_img, (0,0))
        
        #tegner platformene
        for p in platform_list:
            self.screen.blit(p.image, (p.rect.x, p.rect.y))

        #tegner slott
        self.screen.blit(castle_img, (castle.rect.x, castle.rect.y))
        
        # Tegner spilleren
        self.screen.blit(player_img, self.player.pos)

        #tegner penger
        for money in money_list:
            self.screen.blit(money_img, (money.rect.x, money.rect.y))
        
        
        #viser poeng
        self.display_poeng()
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    
    # Metode som viser start-skjerm
    def show_start_screen(self):
        intro=True
        intro_sfx.play()
        
        title=self.font.render('Super TIMA', True, BLACK)
        title_rect=title.get_rect(x=180, y=100)
        
        text_img = self.font.render(f"Få Tima til slottet. Bruk biltastene til å bevege deg fra høyre til venstre, og bruk space for å hoppe.",True, BLACK)
        text_rect=text_img.get_rect(x=10,y=300)
        
        
        play_button = Button(180,350,100,50, WHITE, BLACK, 'Play', 32)
        
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
collide_platform = False

# Lager et spill-objekt
game_object = Game()

# Spill-løkken
while game_object.running:
    game_object.show_start_screen()
    # Starter et nytt spill
    game_object.new()

pg.quit()
sys.exit()



