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
        self.stones_white = c.stones_white
        # self.stones_black_pos = []
        # self.stones_white_pos = []

        self.checkers = []

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

   
    def stone_setup(self, x):
        return (int(self.WIDTH/16 + self.tile_size * (x%8)), \
                int(self.HEIGHT/16 + self.tile_size *(x//8)))
                
    def draw_stones(self):

        diameter = int(self.tile_size/24*9)
                
        for pos_int in (self.stones_black):
            pos = self.stone_setup(pos_int)
            pygame.draw.circle(self.screen, c.black_Grey, pos, diameter)

        for pos_int in (self.stones_white):
            pos = self.stone_setup(pos_int)
            pygame.draw.circle(self.screen, c.WHITE , pos, diameter)

            ##### marks checkers
        for pos_int in (self.checkers):
            pos = self.stone_setup(pos_int)
            pygame.draw.circle(self.screen, c.RED , pos, int(diameter/3))


        pygame.display.flip()

    def convert_pos_to_int(self, position, down):
        column = int(position[0] / self.tile_size)
        row = int(position[1] / self.tile_size)
        if down:
            self.clicked_down = column + 8*row
        else:
            self.clicked_up = column + 8*row
        
    def update(self):
        self.draw_field()
        self.draw_stones()    

    def beat(self):
        for beat in self.beatings:
            if beat[0] == self.clicked_down \
            and beat[-1] == self.clicked_up:
                for i in range(len(beat)-1):
                    self.stones_white.remove\
                    (int((beat[i]+beat[i+1])/2))
                    self.move(beat[i:i+2], "black")
                    time.sleep(0.25)
                self.computer_acts()

    def start_game(self):
        self.draw_field()
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
                         
                        ##### must to beat someone, before normally moving 
                        self.check_for_beating("black")
                        tmp_beatings = [[x[0],x[-1]] for x in self.beatings]
                        vector = [self.clicked_down, self.clicked_up]
                        if len(self.beatings) > 0:
                            if vector not in tmp_beatings:
                                continue
                            else:
                                self.beat()
                                
                                ##### #####  ##### #####   ##### #####  
                        else:   # -> no Beatings -> just moving
                            self.check_for_moves("black")
                            if len(self.possibilities) > 0 \
                            and vector in self.possibilities:
                                self.move(vector,"black")
                                self.computer_acts()
                            else: "Game is over!"

            
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
            right = 7*direction
            left  = 9*direction
            move = [right, left]
            
            tmp = []
            for dir in move:
                enemy = stone + dir 
                free_space1 = enemy + dir
                if enemy in defender and \
                free_space1 not in defender + attacker\
                and free_space1 in self.field_black:
                    tmp.append([stone,free_space1])

                    for dir in move:
                        enemy = free_space1 + dir
                        free_space2 = enemy + dir
                        if enemy in defender and \
                        free_space2 not in defender + attacker\
                        and free_space2 in self.field_black:
                            tmp.append([stone,free_space1,free_space2])
                        
                            for dir in move:
                                enemy = free_space2 + dir
                                free_space3 = enemy + dir
                                if enemy in defender and \
                                free_space3 not in defender + attacker\
                                and free_space3 in self.field_black:
                                    tmp.append([stone,free_space1, \
                                        free_space2,free_space3])
            
            if len(tmp) > 0:
                print(tmp, len(max(tmp)))
                self.beatings += [x for x in tmp if len(x) == len(max(tmp))]
            
    def move(self, vector, color):
        if color == "white":
            self.stones_white.remove(vector[0])
            self.stones_white.append(vector[1])
            if vector[1] in range(8):
                self.checkers.append(vector[1])
        else:
            self.stones_black.remove(vector[0])
            self.stones_black.append(vector[1])            
            if vector[1] in range(56, 64):
                self.checkers.append(vector[1])

        self.update() ## redraws the field and the stones

    def computer_acts(self):
        time.sleep(0.25)

        self.check_for_beating("white")
        if len(self.beatings) > 0:
            chosen_move = max(self.beatings) #random.choice(self.beatings)
            for i in range(len(chosen_move)-1):
                self.stones_black.remove(\
                    int((chosen_move[i]+chosen_move[i+1])/2))
                
                self.move(chosen_move[i:i+2], "white")
                time.sleep(0.25)
        else:
            self.check_for_moves("white")
            if len(self.possibilities) > 0:
                chosen_move = random.choice(self.possibilities)
                self.move(chosen_move, "white")
            else: 
                print("You win!")
                time.sleep(2)
                quit()
            


mill_1 = Game()
mill_1.start_game()