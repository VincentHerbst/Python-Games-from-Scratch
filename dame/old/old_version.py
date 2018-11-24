import random
import numpy as np
import pygame
import pygame.locals as loc
import time

import constants as c

pygame.mixer.quit()


class Game(object):

    def __init__(self, WIDTH=720, HEIGHT=720):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dame")
        self.clock = pygame.time.Clock()
        
        self.tile_size = self.WIDTH/8 # 8 tiles next to each other
        #self.distance = 0 # no space between field and outerlayer 
        # self.distance_factor = 1 # space between tiles?!

        self.clicked_down = (888,888)
        self.clicked_up = (888,888)

        self.field_black = {}
        self.stones_black = c.stones_black
        self.stones_black_pos = []
        self.stones_white = c.stones_white
        self.stones_white_pos = []

        ### COMPUTER --> DATA
        self.possibilities = []
        self.computer_beatings = []

    def draw_field(self):
        self.screen.fill(c.GREEN)
        
        # dictionary for the positions of allsquares
        

        # dark_field
        for pos in c.pos_black:
            pos_x = (pos % 8 * self.tile_size)
            pos_y = (pos // 8 * self.tile_size)
            self.field_black[pos] = (pos_x,pos_y)

            pygame.draw.rect(self.screen, c.dark_field,\
                            (pos_x,pos_y,self.tile_size,self.tile_size))
        
        # white_field
        for pos in c.pos_white:
            pos_x = (pos % 8 * self.tile_size)
            pos_y = (pos // 8 * self.tile_size)
            pygame.draw.rect(self.screen, c.white_field,\
                            (pos_x,pos_y,self.tile_size,self.tile_size))

        pygame.display.flip()

   
    def stone_setup(self):

        self.stones_black_pos = \
                    [(int(self.WIDTH/16 + self.tile_size * (x%8)), \
                    int(self.HEIGHT/16 + self.tile_size *(x//8)))\
                    for x in self.stones_black]

        self.stones_white_pos = \
                    [(int(self.WIDTH/16 + self.tile_size * (x%8)), \
                    int(self.HEIGHT/16 + self.tile_size *(x//8)))\
                    for x in self.stones_white]

    def draw_stones(self):

        diameter = int(self.tile_size/24*9)
                
        for pos in (self.stones_black_pos):
            pygame.draw.circle(self.screen, c.black_Grey, pos, diameter)

        for pos in (self.stones_white_pos):
            pygame.draw.circle(self.screen, c.WHITE , pos, diameter)

        pygame.display.flip()

    def convert_pos_to_int(self, position, down):
        column = int(position[0] / self.tile_size)
        row = int(position[1] / self.tile_size)
        if down:
            self.clicked_down = column + 8*row
        else:
            self.clicked_up = column + 8*row
        
    def move(self):
        self.stones_black.remove(self.clicked_down)
        self.stones_black.append(self.clicked_up)

        self.update() ## redraws the field and the stones
        self.computer_acts()
        self.update() 
        print(self.clicked_down, self.clicked_up,)
        # self.clicked_up = None
        # self.clicked_down = None
        
    def update(self):
        self.stone_setup()
        self.draw_field()
        self.draw_stones()    

    def start_game(self):
        self.draw_field()
        self.stone_setup() ### if no argument -> initial conditions
        self.draw_stones()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                

                if (event.type == loc.MOUSEBUTTONDOWN):
                    self.convert_pos_to_int(event.pos, down = True)
                    ### --> saves the position in self.clicked_down
                                     
                if (event.type == loc.MOUSEBUTTONUP)\
                    and self.clicked_down in self.stones_black:
                    self.convert_pos_to_int(event.pos, down = False)
                    # print("NO", self.clicked_down, self.clicked_up)
                       
                    if self.clicked_down != self.clicked_up\
                        and self.clicked_up not in self.stones_black\
                        + self.stones_white \
                        and self.clicked_up in self.field_black:
                            ### --> saves the position in self.clicked_down
                         
                        ##### must to beat some one, before normally moving 
                        self.check_for_beating("black")
                        print(self.beatings)
                        if len(self.beatings) > 0:
                            if [self.clicked_down, self.clicked_up]\
                            not in self.beatings:
                                continue
                            else:
                                self.stones_white.remove(int(self.clicked_down +\
                                                            self.clicked_up)/2)
                                self.move()
                        ##### #####  ##### #####   ##### #####  ##### ##### 
                        else:
                            self.check_for_moves("black")
                            print(self.possibilities, [self.clicked_down, self.clicked_up])
                            if len(self.possibilities) > 0 \
                            and [self.clicked_down, self.clicked_up]\
                            in self.possibilities:
                                self.move()
                            else: "Game is over!"




                        # if self.clicked_up == self.clicked_down + 7 or\
                        #     self.clicked_up == self.clicked_down + 9:
                        #     # only going forward
                            # self.move() ## chosen stone moves to desired place

                        # elif self.clicked_up == self.clicked_down + 14 and\
                        #     self.clicked_down + 7 in self.stones_white and\
                        #     self.clicked_down + 14 not in \
                        #     self.stones_white + self.stones_black:
                            
                        #     self.move()
                        #     self.stones_white.remove(self.clicked_down + 7)

                        # elif self.clicked_up == self.clicked_down + 18 and\
                        #     self.clicked_down + 9 in self.stones_white and\
                        #     self.clicked_down + 18 not in \
                        #     self.stones_white + self.stones_black:
                            
                        #     self.move()
                        #     self.stones_white.remove(self.clicked_down + 9)
                        
                    

                
                #if (event.type == loc.MOUSEBUTTONUP):
                #elif pygame.mouse.get_pressed()[0]
                #else:
                
            self.clock.tick(60)

##############################################################
##################### Computer ##########################
##############################################################

    def check_for_moves(self, color):
        self.possibilities = []
        if color == "black":
            attacker = self.stones_black
            defender = self.stones_white
            direction = 1
        elif color == "white": 
            attacker = self.stones_white
            defender = self.stones_black
            direction = -1
        else: print("problem with the color in check_for_moves")

        for stone in attacker:
            right = stone + 7*direction
            left = stone + 9*direction
            if right not in attacker + defender\
                and right in self.field_black:
                self.possibilities.append([stone, right])
                
            if left not in attacker + defender\
                and left in self.field_black:
                self.possibilities.append([stone, left])
       
    def check_for_beating(self, color):
        self.beatings = []
        if color == "black":
            attacker = self.stones_black
            defender = self.stones_white
            direction = 1
        else: 
            attacker = self.stones_white
            defender = self.stones_black
            direction = -1

        for stone in attacker:
            right = stone + 7*direction
            left = stone + 9*direction
            if right in defender and \
                right + 7*direction not in defender + attacker\
                and (right + 7*direction) in self.field_black:
                self.beatings.append([stone, right + 7*direction])   

            if left in defender and \
                left + 9*direction not in defender + attacker\
                and left + 9*direction in self.field_black:
                self.beatings.append([stone, left + 9*direction])   
        
    def computer_moves(self, vector):
        self.stones_white.remove(vector[0])
        self.stones_white.append(vector[1])
        self.possibilities = []

    def computer_acts(self):
        time.sleep(0.5)

        self.check_for_beating("white")
        if len(self.beatings) > 0:
            chosen_move = random.choice(self.beatings)
            self.stones_black.remove(int((chosen_move[0]+chosen_move[1])/2))
            self.computer_moves(chosen_move)
            # self.check_for_beating()
            # for i in self.computer_beatings:
            #     if i[0] == chosen_move[0]:
            #         self.computer_moves(chosen_move)

        else:
            self.check_for_moves("white")
            chosen_move = random.choice(self.possibilities)
            self.computer_moves(chosen_move)




mill1 = Game()
mill1.start_game()