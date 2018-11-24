import random
import pygame
import time

import constants as c

pygame.mixer.quit()

class Game(object):

    def __init__(self, WHIDTH=250, HEIGHT=750):
        self.WHIDTH = WHIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WHIDTH, HEIGHT))
        pygame.display.set_caption("PathwithMath")

        self.clock = pygame.time.Clock()

        self.List_of_levels = []
        self.rect_list = []
        self.bomb_list = []
        self.player_pos = None

        self.player_active = False
        
    
    def make_levels(self):
        for diffi in range(0,10):
            self.List_of_levels.append(Level(amount_bombs=(diffi+1)*2, difficulty = diffi))

    def create_rects(self,level):
        tile_size = self.WHIDTH / (level.tiles_hor + 1)  ### everytime the same???!!!
        distance = tile_size/(level.tiles_hor + 1)       ### everytime the same???!!!
        
        self.rect_list = [pygame.Rect(distance,distance,tile_size, tile_size) for x in range(level.tiles_hor*level.tiles_vert)]

        for x in range(level.tiles_hor):
            for y in range(level.tiles_vert):
                i = x + y * 6
                self.rect_list[i].move_ip(x*(tile_size + distance), y*(tile_size + distance))
                

    def create_bombs(self,level):
        self.bomb_list = []

        if len(level.possible_bombs) < level.amount_bombs:
            rest_bombs = level.amount_bombs - len(level.possible_bombs)
            self.bomb_list = list( set(level.possible_bombs) - set(level.path) )
            free_rectangles = [x for x in range(level.tiles_hor*level.tiles_vert) if x not in level.path]
            free_rectangles = list(set(free_rectangles)- set(self.bomb_list))
            for i in range(rest_bombs):
                new_bomb = random.choice(free_rectangles)
                self.bomb_list.append(new_bomb)
                if len(free_rectangles) > 1:
                    free_rectangles.remove(new_bomb)
                else: continue
        else:
            try:
                self.bomb_list = list(set(level.possible_bombs) - set(level.path))[:level.amount_bombs]
            except:
                print("NOOOO BOOOOMBS")

    def show_bombs(self, level):
        self.screen.fill(c.WHITE)

        for rectangles in self.rect_list:
            self.screen.fill((c.GREY), rectangles)

        for i in self.bomb_list:
            self.screen.fill((c.RED), (self.rect_list[i])) 
        self.screen.fill((c.GREEN), (self.rect_list[level.aim_pos]))
        self.screen.fill((c.BLUE), (self.rect_list[level.start_pos]))
        
        pygame.display.flip()

    #def ignore_input(self, event):
     #   if event.type == pygame.QUIT: 
      #      sys.exit()
       # elif event.type == pygame.KEYDOWN:
        #    print(event)

    def user_input(self, event,level):
        
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN: # and self.player_active:
            if event.key == pygame.K_RIGHT:
                if self.player_pos % level.tiles_hor != level.tiles_hor-1:
                    self.player_pos += 1
                
            if event.key == pygame.K_LEFT:
                if self.player_pos % level.tiles_hor != 0:
                    self.player_pos -= 1
            
            if event.key == pygame.K_UP:
                if self.player_pos >= level.tiles_hor:
                    self.player_pos -= level.tiles_hor
                
            if event.key == pygame.K_DOWN:
                if self.player_pos < level.tiles_hor * level.tiles_vert - level.tiles_hor:
                    self.player_pos += level.tiles_hor

    def player_moves(self, level):
        self.player_active = True
        event = pygame.event.wait()#:# -  set(self.pre_events )) :
            #print(self.player_active, event)
        self.user_input(event, level)
    
    def clear(self):
        """Clear the event queue from keyboard events."""
        print("before",pygame.event.get())
        pygame.event.clear(pygame.KEYDOWN)
        print("after",pygame.event.get())

        #pygame.event.clear(pygame.KEYUP)

    def update_screen(self,level):
        self.screen.fill(c.WHITE)

        for rectangles in self.rect_list:
            self.screen.fill((c.GREY), rectangles)

        #### Start and Aim Position --> Highlighting
        self.screen.fill((c.GREEN), (self.rect_list[level.aim_pos]))
        #self.screen.fill((c.DARK_GREEN), (self.rect_list[level.start_pos]))
        self.screen.fill((c.BLUE), (self.rect_list[self.player_pos]))

        
        pygame.display.flip()


    def show_solution(self, level):
        for i in level.path[0:-1]:
            self.screen.fill((c.YELLOW), (self.rect_list[i]))
        #for bom in self.bomb_list:
        #    self.screen.fill(c.RED, self.rect_list[bom])
        self.screen.fill(c.DARK_GREEN, self.rect_list[level.start_pos])
        pygame.display.flip()

    def start(self):

        self.make_levels()

        for level in self.List_of_levels:
            #pygame.event.set_blocked(pygame.KEYDOWN)
            level.path_difficulty() ## gets start and aim position and also creates one solution

            self.create_rects(level)
            self.create_bombs(level)

            self.player_pos = level.start_pos
            self.update_screen(level)
            #self.show_solution(level)
            
            #time.sleep(2)

            self.show_bombs(level)
            self.player_active = False
            pygame.event.clear()
            

            while self.player_active == False:
                self.player_moves(level)
                self.clock.tick(30)
            
            #pygame.event.clear()
            
            #pygame.event.set_allowed(pygame.KEYDOWN)
            
            while self.player_pos != level.aim_pos:
                pygame.event.clear()
                self.clock.tick(60)
                #if self.player_active:
                self.player_moves(level)
                #self.player_active = True
                #self.player_active = True
                #pygame.event.pump()

                self.update_screen(level)

                if self.player_pos in self.bomb_list:
                    #pygame.event.set_allowed(None)
                    self.show_bombs(level)
                    self.show_solution(level)
                    self.screen.fill(c.BLACK, self.rect_list[self.player_pos])
                    pygame.display.flip()
                    self.player_active = False
                    while pygame.event.get(pygame.KEYDOWN) == []:
                        self.clock.tick(60)
                    #pygame.event.clear()

                    self.start()
                    break

            self.show_bombs(level)
            pygame.event.clear()
            #self.player_active = False
            
            while pygame.event.get(pygame.KEYDOWN) == []:
                self.clock.tick(60)
            

##################################################################
######################  LEVEL  ##################################
##################################################################

class Level(object):
    """docstring for Level"""
    def __init__(self, amount_bombs,difficulty=1, start_pos=None, aim_pos=None, path=None, tiles_hor=6):
        #super(Level, self).__init__()
        self.difficulty = difficulty
        self.path = path
        self.start_pos = start_pos
        self.aim_pos = aim_pos

        self.amount_bombs =  10 + amount_bombs
        self.possible_bombs = []


        ## geometry ##
        self.tiles_hor = tiles_hor
        # vertical length depends on diffi 
        ###### difficulty ########
        if difficulty <= 10:
            self.tiles_vert = 6 + difficulty
        else: 
            print("difficulty is set too high!, has to be under 10")
            self.tiles_vert = 16
        ##########################


    def get_start_aim_pos(self):
        bottom_row = range(self.tiles_vert*self.tiles_hor - self.tiles_hor, self.tiles_vert*self.tiles_hor)
        top_row = range(0, self.tiles_hor)
        
        self.start_pos = random.choice(bottom_row)
        self.aim_pos   = random.choice(top_row)

    def path_difficulty(self):  ### it never goes down 
        # done:        ## neues Feld, darf keine zwei eigenen Felder berühren (prio 1)
        # not yet:    ## --> je schwieriger umso weniger oft darf es in die gleiche Richtung mehrmals gehen
        
        self.get_start_aim_pos()
        #print(self.start_pos, self.aim_pos)
        self.path = [self.start_pos]
        
        self.possible_bombs = []

        while self.path[-1] != self.aim_pos: #### until the top rectangle
            
            possible_moves = []
            if self.path[-1] % self.tiles_hor != self.tiles_hor-1:
                if (self.path[-1] + self.tiles_hor + 1) not in self.path:
                    possible_moves.append(1)
                elif  self.path[-1] + 1 not in self.path:
                    self.possible_bombs.append(self.path[-1] + 1)
            
            if self.path[-1] % self.tiles_hor != 0:
                if (self.path[-1] + self.tiles_hor - 1) not in self.path:
                    possible_moves.append(-1)
                elif  self.path[-1] - 1 not in self.path:
                    self.possible_bombs.append(self.path[-1] - 1)

            if self.path[-1] >= self.tiles_hor: ### one addition if "down" is added  
                possible_moves.append(-self.tiles_hor)
            else:
               if self.aim_pos > self.path[-1]:
                   possible_moves = [1]
               else: 
                   possible_moves = [-1]

            if len(possible_moves) > 1:
                try:
                    possible_moves.remove(-(self.path[-1] - self.path[-2]) ) #### forbid to go left and right 
                    #if self.path[-1] in [1,-1]:
                    #possible_moves.remove(self.path[-3] - self.path[-4] )
                except:
                    pass
            if len(possible_moves) > 1:
                try:
                    exponent = self.path[-5:].count(self.path[-1])
                    if random.choice(range(1,self.difficulty*10+1))/100 <= (1 - (self.difficulty-1)/2) ** exponent: 
                        # 100 - 5 * diff 
                        possible_moves = [self.path[-1] - self.path[-2]]
                    
                    #    possible_moves.remove((self.path[-1] - self.path[-2]) ) #### forbid to go left and right 
                    #else:
                except:
                    pass

            new_field = self.path[-1] + random.choice(possible_moves)
            
            self.path.append( new_field )

        ################# explanation ################################################
        # up means -6
        # right means +1
        # left means -1
        ## restrictions:
            ## numbers may not be mins 
            ## if the number % 6 == 5 cannot go right
            ## if the number % 6 == 0 cannot go left
            ## and only one neighbour may only be in the list potential_path
        ##############################################################################
     
     # to dooo ??!!
     ########################
    ### outputs ##################
    ##############
        # path difficulty

        # show bombs ??! time, which order

        #--> modi ==

        # geometry -- how many rows ?!  