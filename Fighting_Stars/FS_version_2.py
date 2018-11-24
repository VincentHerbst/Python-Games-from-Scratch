import pygame
import pygame.locals as loc
import random
import time
import math

pygame.font.init()
font_size = 20
myfont = pygame.font.SysFont("Times New Roman",font_size)
big_font_size = font_size*5
my_big_font = pygame.font.SysFont("Times New Roman",big_font_size)
pygame.mixer.quit()

WIDTH = 1300
HEIGHT = 750

WHITE = (255, 255, 255)
BLACK = (0,0,0)
Grey = (85,85,85)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
ORANGE = (255,255,0)


game_display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('StarGame')
clock = pygame.time.Clock()

pos_green = [WIDTH-80, HEIGHT-80]
pos_red = [80, 80]
pos_blue = [80,HEIGHT-80]
pos_orange = [WIDTH- 80,80]



class star:
    
    def __init__(self, color,pos=[80,80], size=20, RANDOM=False, life=50, Star_start=None, Star_aim=None, mode="defence", base=False, points=None):
        
        self.RANDOM = RANDOM

        if RANDOM:
            self.x = pos[0] + random.randrange(-15, 15)
            self.y = pos[1] + random.randrange(-15, 15)
        else:
            self.x = pos[0]
            self.y = pos[1]
        
        self.color = color
        self.life = life
        self.pos = pos

        self.tmp_x = 0
        self.tmp_y = 0
        self.stop = False

        
        self.Star_start = Star_start
        self.Star_aim = Star_aim

        self.size = size


        if mode == "defence":
            self.character = (1,2,3)
        elif mode == "normal":
            self.character = (3,5,7)
        elif mode == "aggressive":
            self.character = (7,8,9)

        self.minimum_soldiers = 0
        self.BASE = base

                        
    def move(self):   
           
            slowdown = math.sqrt((self.pos[0]-self.Star_aim.pos[0])**2 + (self.pos[1]-self.Star_aim.pos[1])**2)/3
            
            if slowdown == 0:
                slowdown = 500/3

            self.move_x = int((self.Star_aim.pos[0]- self.pos[0])/((slowdown)) )
            self.tmp_x += ((self.Star_aim.pos[0]- self.pos[0])/(slowdown) ) - self.move_x
            
            if abs(self.tmp_x) >= 1:
                self.move_x += int(self.tmp_x // 1 )
                self.tmp_x -= int(self.tmp_x // 1)

            self.move_y = int((self.Star_aim.pos[1]- self.pos[1])/(slowdown) )
            self.tmp_y += ((self.Star_aim.pos[1]- self.pos[1])/(slowdown) ) - self.move_y
        
            if abs(self.tmp_y) >= 1:
                self.move_y += int(self.tmp_y // 1)
                self.tmp_y -= int(self.tmp_y // 1)
            
            if abs(self.y-self.Star_aim.pos[1]) < self.Star_aim.size and abs(self.x-self.Star_aim.pos[0]) < self.Star_aim.size: ## self.Star_aim.size
                self.stop = True
            #if math.sqrt((abs(self.y-self.Star_aim.pos[1])**2 + abs(self.x-self.Star_aim.pos[0]))**2) < 10*self.Star_aim.size: ## self.Star_aim.size
            #    self.stop = True
            
            else:
                self.x += self.move_x
                self.y += self.move_y

    def loselife(self, CHANGE_COLOR, points=1):
        
        if points == 1:
            self.life -= 1
        else:
            self.life -= points

        if self.life == 0:
            self.color == Grey

        if self.life <= -1:
            self.color = CHANGE_COLOR
            self.life =  -self.life

        self.change_size()

            
    def gainlife(self, points=1):

        if points == 1:
            self.life += 1
        else:
            self.life += points

        self.change_size()

        if self.life == 0:
            self.color == Grey

    def display_life(self, font_size):
        if self.RANDOM == False:
            text = myfont.render("%i"%(self.life), True, BLACK)
            game_display.blit(text, (self.x-int(font_size/2), self.y-int(font_size/2)))
            
    def sendArmy(self, big_stars,small_stars, Star_aim, how_many=0):
        
        #self.size = how_many
        if how_many == 0:
            how_many = int(self.life/2)

        if how_many > self.life:
            how_many = int(self.life/3)
        
        self.life -= how_many

        small_stars.append(star(self.color,self.pos, RANDOM=True, Star_start=self, Star_aim=Star_aim,life=how_many))

        return big_stars, small_stars

    def reaction_defence(self, big_stars, small_stars):
        for sta in big_stars:
            if sta != self:

                if sta.size > 10 and sta.color != RED and sta.color == self.color and sta.color != Grey and sta.life > 100:
                    if sta.life > 1000 or (sta.life > 100 and sta.life < 150) or (sta.life > 200 and sta.life < 350)  :
                        army = sta.life/2
                        big_stars, small_stars = sta.sendArmy(big_stars, small_stars, Star_aim=self, how_many= army)
        
        return big_stars, small_stars 

    def reaction_offence(self, big_stars, small_stars):
        for sta in big_stars:
            if sta.size > 10 and sta.color != Grey and sta.color != RED and sta.life >= 20:
                big_stars, small_stars = sta.sendArmy(big_stars, small_stars, Star_aim=self, how_many=int(sta.life/2))
        
        return big_stars, small_stars 

    def change_size(self,how_many=None):
        #if self.RANDOM:
        #    pass
            #self.size = how_many
        if self.life < 100:
            self.size = 30
        elif self.life < 200:
            self.size = 40
        elif self.life < 500:
            self.size = 50
        else: 
            self.size = 60

    def conquer_star(self, big_stars, small_stars, Star_aim, conquer_mode=True): ### conquering easiest_enemy or saving --> base!
                    #(self, stars, Star_aim, how_many=0):
        for sta in big_stars:
            

            if sta.color == self.color and Star_aim != self:
                sta.character = self.character 

                if sta.BASE and conquer_mode and Star_aim != self:
                    how_many = self.life - self.minimum_soldiers
                
                if sta.life > 1000:
                    how_many = int(sta.life/2)

                # elif sta.life > 100 and conquer_mode:
                #     how_many = int(sta.life/2)

                elif sta.life > 25 and conquer_mode:
                    how_many = int(sta.life/2)
                else:
                    how_many = 0
                
                if sta.life > self.life:
                    sta.BASE = True 
                    self.base = False
                

                #sta.life -= how_many

                big_stars, small_stars = self.sendArmy(big_stars,small_stars, Star_aim, how_many)
                #for i in [star(sta.color,sta.pos, size=2, RANDOM=True, Star_start=sta, Star_aim=Star_aim,life=0) for x in range(how_many)]:
                #    small_stars.append(i)

        return big_stars, small_stars

    def saving_complete(self, stage):
        if stage == 0:
            self.minimum_soldiers = 30
        elif stage == 1:
            self.minimum_soldiers = 100
        elif stage == 2:
            self.minimum_soldiers = 200
        else:
            self.minimum_soldiers = 500

        if self.life >= self.minimum_soldiers:
            return True
        else:
            return False    

    def saving_or_fighting(self, big_stars, small_stars, amount_stars, Star_aim):
        #### only called one time --- through base --- NEEDS to be a list of the biggest stars -> amount stars
        z = 0
        try:

            for i in self.character:
                
                if amount_stars >= i:
                    z =+ 1
                    
                else:
                    break

            if self.saving_complete(stage=z): # check_if_saving_complete
                big_stars, small_stars = self.conquer_star(big_stars, small_stars, Star_aim) ## the easiest one -- if you have enough spare soldiers
            
            # else:
            #     if Star_aim.BASE and Star_aim.life <  :
            #         Star_aim = self
            #         big_stars, small_stars = self.conquer_star(big_stars, small_stars, Star_aim, conquer_mode=False)
            
        except:
            pass

        return big_stars, small_stars
    
       
def draw_environment(big_stars, small_stars):
    
    stars = big_stars + small_stars

    for sta in stars:
        if sta.stop:
            if sta.color == sta.Star_aim.color:
                sta.Star_aim.life += sta.life
            else:
                sta.Star_aim.life -= sta.life
                if sta.Star_aim.life < 0:
                    sta.Star_aim.color = sta.color
                    sta.Star_aim.life *= -1
                    
                
            small_stars.remove(sta)

        pygame.draw.circle(game_display, sta.color, [sta.x, sta.y], sta.size)
        
        sta.display_life(font_size)
    
    pygame.display.update()
    


def main():
    
    t = 0
    small_stars = []
    big_stars = []
    stars = []
    small_stars = []

    ########### Player included 

    players = {RED:[pos_red,1,0, None], \
                BLUE:[pos_blue,1,0,"aggressive"], \
                ORANGE:[pos_orange,1,0,"defence"],\
                GREEN:[pos_green,1,0,"normal"]}

    for color in players:
        big_stars.append(star(color,players[color][0], base=True, mode=players[color][3]))
    
    ########### neutral stars

    pos_grey_stars = [[int(2*WIDTH/4), int(5*HEIGHT/16)],
                      [int(3*WIDTH/4), int(2*HEIGHT/4)],
                      [int(WIDTH/4),   int(2*HEIGHT/4)],
                      [int(2*WIDTH/4), int(2*HEIGHT/4)],
                      [int(2*WIDTH/4), int(11*HEIGHT/16)],
                      [int(1*WIDTH/8), int(2*HEIGHT/4)],
                      [int(7*WIDTH/8), int(2*HEIGHT/4)],
                      [int(4*WIDTH/8), int(1*HEIGHT/8)],

                      [int(3*WIDTH/16), int(3*HEIGHT/16)],#
                      [int(3*WIDTH/16), int(13*HEIGHT/16)],#
                      [int(13*WIDTH/16), int(3*HEIGHT/16)],#
                      [int(13*WIDTH/16), int(13*HEIGHT/16)],#
                      [int(4*WIDTH/8), int(7*HEIGHT/8)]]

    for pos_grey in pos_grey_stars:
        big_stars.append(star(Grey, pos_grey, life=5, size = 30))
    ######################################################################
    
    game_display.fill(WHITE)
    
    while True:

        game_display.fill(WHITE)
        draw_environment(big_stars, small_stars)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if (event.type == loc.MOUSEBUTTONDOWN): 
                Star_start = None    

                for sta in big_stars:
                    if sta.size >= 10: # unnoetig
                        if abs((event.pos[0]-sta.pos[0])**2 + (event.pos[1]-sta.pos[1])**2) <= 60**2 and sta.color == RED:
                            Star_start = [sta]
            try:
                if pygame.mouse.get_pressed()[0]:
                    for sta in big_stars:
                        
                        if sta.size >= 10:
                            if sta != Star_start[0]:
                                try:
                                    if abs((event.pos[0]-sta.pos[0])**2 + (event.pos[1]-sta.pos[1])**2) <= 60**2:
                                        
                                        if sta not in Star_start and sta.color == Star_start[0].color:
                                            try:
                                                Star_start.append(sta)
                                                print(pygame.mouse.get_pressed())
                                            except AttributeError:
                                                pass
                                except:
                                    pass
            except:
                pass
            
            if (event.type == loc.MOUSEBUTTONUP):
                Star_aim = None

                for sta in big_stars:
                    if sta.size >= 10:
                        if abs((event.pos[0]-sta.pos[0])**2 + (event.pos[1]-sta.pos[1])**2) <= 60**2:
                            Star_aim = sta
                        
                if Star_start and Star_aim:
                    
                    for Star_indiv in Star_start:
                        big_stars, small_stars = (Star_indiv.sendArmy(big_stars, small_stars, Star_aim))

                    if Star_start[0] != Star_aim:
                        big_stars, small_stars = Star_aim.reaction_defence(big_stars, small_stars)
                    #    
                        #big_stars, small_stars = Star_start[0].reaction_offence(big_stars, small_stars)



        bases = [sta for sta in big_stars if sta.BASE]                   
        #for sta in big_stars:
        #    if sta.base:
        #        bases.append(sta)
        
            
        

        if t % 25 == 0:
            Reihenfolge = []     
            numerator = 0
            for sta in big_stars:
                num = int(sta.life)
                Reihenfolge.append((num,numerator))
                numerator +=1
                
            indice = [i for i in Reihenfolge]
            indice.sort()
            
            easiest_enemy = big_stars[indice[0][1]]

            if t % 7 == 0:
                Tried = {GREEN:False, BLUE:False, ORANGE:False}
                
                for i in range(len(bases)):
                    if bases[i].color != RED:
                        if Tried[bases[i].color]:
                            continue
                        else:
                            big_stars, small_stars = bases[i].saving_or_fighting(big_stars, small_stars, players[bases[i].color][1], big_stars[indice[i][1]])
                            Tried[bases[i].color] = True


            players[RED][2] = 0
            players[BLUE][2] = 0
            players[GREEN][2] = 0
            players[ORANGE][2] = 0

            for colors in players:
                for i in [0,1]:
                    players[colors][i] = 0

            stars = big_stars + small_stars
            for sta in stars:
                
                for colors in players:
                     

                    if sta.color == colors and sta.size >= 10:
                        players[colors][2] += sta.life
                        players[colors][1] += 1
                    elif sta.color == colors and sta.size < 10:
                        players[colors][2] += 1


                
                if sta.color != Grey and sta.RANDOM == False:
                    if sta.life > 100:
                        sta.gainlife(points=2)
                        
                    if sta.life > 200:
                        sta.gainlife(points=3)
                        
                    
                    if sta.life > 500:
                        sta.gainlife(points=4)
                        
                        
                    else:
                        sta.gainlife(points=1)
                        
            
            for colors in players:
                print(" {} hat {} Sterne und {} Einheiten.".format( colors, players[colors][1],players[colors][2]))
            

            #### Diagramm --- wie punkteverteilung is ;)

            #print("Du:", RED_gesamt, "Blue:", comp_players[BLUE][2])
            #print("Differenz", RED_gesamt-Blue_gesamt)


        WIN = True
        for colors in players:
            if colors != RED and players[colors][2] != 0:
                WIN = False

        if WIN :
            text = my_big_font.render("GEWONNEN!!!!", True, BLACK)
            game_display.blit(text, (int(WIDTH/2-2.5*big_font_size), int(HEIGHT/2-big_font_size)))
            pygame.display.update()
            time.sleep(3)
            break
        

        if players[RED] == 0:
            text = my_big_font.render("VERLOREN!!!!", True, BLACK)
            game_display.blit(text, (int(WIDTH/2-3*big_font_size), int(HEIGHT/2-big_font_size)))
            pygame.display.update()
            time.sleep(3)
            break


        for smallies in small_stars:
            if smallies.Star_aim:
                smallies.move()
        
        clock.tick(90)
        t += 1


if __name__ == '__main__':
    main()

