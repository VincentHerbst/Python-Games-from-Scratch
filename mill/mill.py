import pygame
import pygame.locals as loc
import random
import time
import math
import dictionaries.possib as dictis



global pos_matrix, pos_matrix_return
global possible_moves, horizontal_mills, vertical_mills
global field, amount_moves



pygame.font.init()
font_size = 20
myfont = pygame.font.SysFont("Times New Roman",font_size)
big_font_size = font_size*5
my_big_font = pygame.font.SysFont("Times New Roman",big_font_size)


WIDTH = 700
HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0,0,0)
Grey = (160,160,160)



game_display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Mill')
clock = pygame.time.Clock()




#   x - - x - - x
#   - x - x - x -
#   - - x x x - -
#   x x x   x x x
#   - - x x x - -
#   - x - x - x -  
#   x - - x - - x


class Player:

    def __init__(self, color, strength, start=None, aim=None):
        
        self.color = color
        self.strength = strength
        self.start = start
        self.aim = aim



class mill_stars:
    
    def __init__(self, color,pos, size=10):
        
        self.color = color
        self.pos = pos

        self.size = size

                        
   

    #def display_life(self, font_size):
    #    if self.RANDOM == False:
    #        text = myfont.render("%i"%(self.life), True, BLACK)
    #        game_display.blit(text, (self.x-int(font_size/2), self.y-int(font_size/2)))
            

### --- constant things
   
Player_WHITE = Player(color="WHITE", strength=0)
Player_BLACK = Player(color="BLACK", strength=0)

pos_mill = [0,3,6,8,10,12,16,17,18,21,22,23,25,26,27,30,31,32,36,38,40,42,45,48]
    
pos_matrix = {}
pos_matrix_return = {}
for pos in pos_mill:
    pos_matrix.update({ (50 + (pos % 7) * 100 , 50 + (pos // 7) * 100) : pos})
    pos_matrix_return.update({ pos : (50 + (pos % 7) * 100 , 50 + (pos // 7) * 100)})
    print(pos_matrix)

field = []
for pos in pos_matrix:
    field.append(mill_stars(BLACK, pos))

next_colour=(WHITE,BLACK)


possible_moves, horizontal_mills, vertical_mills = dictis.possibilities_for_stone()  
# returns a dictionary for all possible moves of on position



# ------------- Functions -------------------------------------
def draw_environment(mill_field):

    game_display.fill(Grey)

    pygame.draw.rect(game_display, BLACK,(47.5,47.5,605,605))
    pygame.draw.rect(game_display, Grey,(52.5,52.5,595,595))

    pygame.draw.rect(game_display, BLACK,(WIDTH/2 - 2.5,WIDTH/2 - 2.5 ,300 + 5,300 + 5))
    pygame.draw.rect(game_display, Grey,(WIDTH/2 + 2.5,WIDTH/2 + 2.5, 300 - 5,300 - 5))
    pygame.draw.rect(game_display, BLACK,(47.5 ,47.5 ,300 + 5,300 + 5))
    pygame.draw.rect(game_display, Grey,(52.5 ,52.5, 300 - 5,300 - 5))

    pygame.draw.rect(game_display, BLACK,(100 + 47.5,100 + 47.5,405,405))
    pygame.draw.rect(game_display, Grey,(100 + 52.5,100 + 52.5,395,395))

    pygame.draw.rect(game_display, BLACK,(WIDTH/2 - 2.5,WIDTH/2 - 2.5 ,205,205))
    pygame.draw.rect(game_display, Grey,(WIDTH/2 + 2.5,WIDTH/2 + 2.5, 195,195))
    pygame.draw.rect(game_display, BLACK,(100 +47.5 ,100 + 47.5 ,205,205))
    pygame.draw.rect(game_display, Grey,(100 +52.5 ,100 +52.5, 195,195))
    pygame.draw.rect(game_display, BLACK,(200 + 47.5,200 + 47.5,205,205))
    pygame.draw.rect(game_display, Grey,(200 + 52.5,200 + 52.5,195,195))



    for stone in mill_field:
        pygame.draw.circle(game_display, stone.color, stone.pos, stone.size)
 
    pygame.display.update()

def collision(pos_one, pos_second, size=20):

    if ((pos_one[0]-pos_second[0])**2 + (pos_one[1]-pos_second[1])**2 < (size)**2):
        return True
    else:
        return False



def distributing(field,amount_moves, next_colour=(WHITE,BLACK)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if (event.type == loc.MOUSEBUTTONDOWN):

            for stone in field:
                if collision(stone.pos, event.pos):
                    
                    if stone.size == 10:# and amount_moves < 18:
                        stone.color = next_colour[amount_moves % 2]
                        stone.size = 20



                        check_mill(stone.pos, stone.color)
                            


                        if amount_moves % 2 == 0:
                            Player_WHITE.strength += 1
                        else:
                            Player_BLACK.strength += 1

                        amount_moves += 1

    return amount_moves

def moving(pos_matrix,field,amount_moves, next_colour=(WHITE,BLACK) ):

    MOVING_STONE = None
    z = 0
    player_turn = next_colour[amount_moves%2]

    if player_turn == WHITE:
        life = Player_WHITE.strength
    else:
        life = Player_BLACK.strength
        
    conti = True
    while conti:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if (event.type == loc.MOUSEBUTTONDOWN):
                for stone in field:
                    if collision(event.pos, stone.pos, 30) and stone.color \
                    == player_turn and stone.size == 20:
                        MOVING_STONE = stone
                        break
                    


            if (event.type == loc.MOUSEBUTTONUP) and MOVING_STONE \
            != event.pos and MOVING_STONE:

                if MOVING_STONE.color == player_turn:
                    for stone in field:
                        if collision(event.pos, stone.pos) and \
                        stone.size == 10: ## and adjacent
                            
                            if life > 3 and pos_matrix[stone.pos] in \
                            possible_moves[pos_matrix[MOVING_STONE.pos]] or \
                                life == 3:

                                #print(MOVING_STONE.color, player_turn)
                                MOVING_STONE.color = BLACK
                                MOVING_STONE.size = 10

                                print(player_turn,":",pos_matrix[MOVING_STONE.pos], \
                                    "-->", pos_matrix[stone.pos])

                                stone.color = player_turn
                                stone.size = 20
                                
                                conti = False
                                amount_moves += 1
                                #draw_environment(field)
                                check_mill(stone.pos, stone.color)
                                
                                break 
                    
                       


            
    return amount_moves
                        
def jump(pos_matrix,field,amount_moves, next_colour=(WHITE,BLACK) ):
    
    for event in pygame.event.get():
        player_turn = next_colour[amount_moves%2]
        
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if (event.type == loc.MOUSEBUTTONDOWN):
            for stone in field:
                if collision(event.pos, stone.pos, 30) and stone.color == player_turn:
                    
                    stone.color = BLACK
                    stone.size = 10
                       

                    if (event.type == loc.MOUSEBUTTONUP):

                        for stone in field:
                            if collision(event.pos, stone.pos) and stone.size == 10:
                                

                                stone.color = player_turn
                                stone.size = 20
                                amount_moves += 1


                                draw_environment(field)
                                print(Player_WHITE.strength, Player_BLACK.strength)
    return amount_moves

def take_a_stone(color_to_take):
    conti = True
    print("color to take", color_to_take)
    while conti:
    
        for event in pygame.event.get():
                            
            if (event.type == loc.MOUSEBUTTONDOWN):

                for stone in field:
                    if collision(stone.pos, event.pos) and stone.color == \
                    color_to_take and stone.size == 20 \
                    and not check_stone_in_mill(stone.pos,stone.color):
                        
                        stone.size = 10
                        stone.color = BLACK
                      
                        if color_to_take == WHITE:
                            Player_WHITE.strength -= 1
                        else:
                            Player_BLACK.strength -= 1

                        conti = False
                        break
                    # elif all are safe -- then continue without taking a stone 

def check_stone_in_mill(position, color):
    stone_is_save = False

    columns = pos_matrix[position] // 7
    line = pos_matrix[position] % 7
    
    if line == 3 and columns > 3:
        z = 1
    else: z = 0
    
    tmp = True
    for pos in vertical_mills[line][z]:

        for stone in field:
            if pos_matrix_return[pos] == stone.pos:
                
                if stone.size == 20 and tmp and stone.color == color:
                    tmp = True
                else: 
                    tmp = False
                    break

    if tmp:
        stone_is_save = True
        #color takes a stone of the enemy


    if columns == 3 and line > 3:
        z = 1
    else: z = 0
    
    tmp = True
    for pos in horizontal_mills[columns][z]:
        for stone in field:
            if pos_matrix_return[pos] == stone.pos:
                print((pos_matrix[stone.pos]), "vertical")
                if stone.size == 20 and tmp and stone.color == color:
                    tmp = True
                else: 
                    tmp = False
                    break

    if tmp:
        stone_is_save = True

    return stone_is_save


def check_mill(position, color):

    draw_environment(field)

    if color == BLACK:
        opposite_color = WHITE
    else: opposite_color = BLACK

    columns = pos_matrix[position] // 7
    line = pos_matrix[position] % 7
    
    if line == 3 and columns > 3:
        z = 1
    else: z = 0
    
    tmp = True
    for pos in vertical_mills[line][z]:

        for stone in field:
            if pos_matrix_return[pos] == stone.pos:
                
                if stone.size == 20 and tmp and stone.color == color:
                    tmp = True
                else: 
                    tmp = False
                    break

    if tmp:
        print(color, "can take a stone, vertically milled")
        take_a_stone(opposite_color)
        #color takes a stone of the enemy


    if columns == 3 and line > 3:
        z = 1
    else: z = 0
    
    tmp = True
    for pos in horizontal_mills[columns][z]:
        for stone in field:
            if pos_matrix_return[pos] == stone.pos:
                print((pos_matrix[stone.pos]), "vertical")
                if stone.size == 20 and tmp and stone.color == color:
                    tmp = True
                else: 
                    tmp = False
                    break


    if tmp:
        print(color, "can take a stone, horizontally milled")
        take_a_stone(opposite_color)
        #color takes a stone of the enemy


      

def main():

    
    t = 0
    

    
    
    
     
    amount_moves = 0

    while True:
        
        draw_environment(field)

        if amount_moves < 18:
            amount_moves = distributing(field, amount_moves)
        elif Player_BLACK.strength >= 3 and Player_WHITE.strength >= 3: # 3 3     
            amount_moves = moving(pos_matrix, field,amount_moves)
        else:
            if Player_BLACK.strength < 3:
                print("Player_WHITE has won!")
            else:
                print("Player_BLACK has won!")

            break


        



        


                
            
            


        clock.tick(90)
        t += 1
        
        
if __name__ == '__main__':
    main()


