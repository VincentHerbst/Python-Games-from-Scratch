import pygame
from pygame.locals import*
import random
import time
import datetime
import math
import os

import dicties.functions as dictis
import dicties.rounded_rects as rounded_rects


global pos_matrix, pos_matrix_return
global possible_moves, horizontal_mills, vertical_mills
global field, amount_moves
global WIDTH, HEIGHT

WIDTH, HEIGHT = 800, 730

class setting_in_game:

    def __init__(self, time_to_play):
        
        self.time_to_play = time_to_play
        
setting = setting_in_game(time_to_play = 35)# # sec



pygame.font.init()
pygame.init()
pygame.mixer.quit()

#full_display = (1280,720)
#screen = pygame.display.set_mode((640,480), FULLSCREEN)


WHITE = (255, 255, 255)
WHITE_grey = (230, 230, 255)
BLACK = (0,0,0)
Grey = (160,160,160)
BLUE = (0, 0, 255)
RED = (190, 0, 0)
GREEN = (61, 169, 40) #(0,255,0)
GREEN = (125,187, 41)
#Mint_GREEN = (152,255,81) 0, bb, 7f ##> 12*16 + 12, 7*16 + 15
ORANGE = (255,125,0)
YELLOW = (250,220,0)
BLACK_GREY = (65,65,65)
BLUE_bright = (0,155,255)
dark_BLUE = (0,115,200)
#fresh_green = (50,255,0)
fresh_green = GREEN



game_display = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
#game_display = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)


pygame.display.set_caption('Quiz')


clock = pygame.time.Clock()

font_size = int(WIDTH/30)
font =        pygame.font.SysFont("Arial", int(font_size))
font_source = pygame.font.SysFont("Arial", int(0.5*font_size))

#### DICTIONARY for all questions and answers!!!
dicties = (dictis.read_data("dicties/quests.txt"))





class Rect:
    def __init__(self, color, pos, text, geometry = (WIDTH/2, HEIGHT*2.2/10), chosen_rect = False, space_width= WIDTH/50, space_height = HEIGHT/25, mode="normal"):
        
        self.color = color
        if self.color == WHITE:
            self.text_color = BLACK
        else: self.text_color = WHITE

        #self.space_width, self.space_height = 
        #space_width, space_height = geometry[0]/20, geometry[1]/5
        self.pos = (pos[0] + space_width/2 , pos[1]+ space_height/2)# + 1/10 * WIDTH)
        self.geometry = [geometry[0]- space_width, geometry[1]- space_height]
                        #(geometry[0]- WIDTH/15, geometry[1]- HEIGHT/15)
        self.text = text
        self.chosen_rect = chosen_rect
        self.mode = mode
        self.new_lines = []
        self.splitting = False


    def collidepoint(self, event_pos):
        
        if event_pos[0] > self.pos[0] and event_pos[0] < self.pos[0] + self.geometry[0] and \
           event_pos[1] > self.pos[1] and event_pos[1] < self.pos[1] + self.geometry[1]:
            
            #print(event_pos[0], ">", self.pos[0], "and" ,event_pos[0] ,"<", self.pos[0] + self.geometry[0])
            #print(event_pos[1], ">", self.pos[1] ,"and", event_pos[1] ,"<", self.pos[1] + self.geometry[1])
            #print(event_pos)

            if self.chosen_rect:
                self.chosen_rect = False
            else:
                self.chosen_rect = True

    def collision_only(self, event_pos):
        
        if event_pos[0] > self.pos[0] and event_pos[0] < self.pos[0] + self.geometry[0] and \
           event_pos[1] > self.pos[1] and event_pos[1] < self.pos[1] + self.geometry[1]:
            collision = True
        else: 
            collision = False

        return collision
     
    def write_text(self):
        
        if self.splitting:
            add = 0
            for text_frag in self.new_lines:
                text_on_screen = font.render(text_frag, False, self.text_color)
                
                if self.mode == "source":
                    game_display.blit(text_on_screen, (self.pos[0], self.pos[1] + add*text_on_screen.get_height() )) 
                else:
                    centering = (self.geometry[0] - text_on_screen.get_width())/2
                    centering_height = (self.geometry[1] - (len(self.new_lines))*text_on_screen.get_height())/2
                    game_display.blit(text_on_screen, (self.pos[0]+centering, self.pos[1]+centering_height + add*text_on_screen.get_height() ))
                add += 1
        else:
            if self.mode == "source":
                text_on_screen = font_source.render(self.text, False, self.text_color)
            else:
                text_on_screen = font.render(self.text, False, self.text_color)
            
            if self.mode == "source":
                game_display.blit(text_on_screen, (self.pos[0], self.pos[1]))
            else:
                centering = (self.geometry[0] - text_on_screen.get_width())/2
                centering_height = (self.geometry[1] - text_on_screen.get_height())/2 ##### 0.8 =!=!=
                game_display.blit(text_on_screen, (self.pos[0]+centering, self.pos[1]+centering_height))

        


    def init_text(self):
        if self.mode == "source":
            text_on_screen = font_source.render(self.text, False, BLACK)#
        else: 
            text_on_screen = font.render(self.text, False, BLACK)
            
            
        if text_on_screen.get_width() > ( self.geometry[0] - (1* font_size)):
            self.splitting = True
        else: 
            self.splitting = False
          
                
        if self.splitting:
            
            new_text = self.text.split(" ")
            new_lines = []
            line = ""
            tmp_1 = ""
            tmp_0 = ""
            
            for word in new_text:
                if len(tmp_1) > 1:
                    tmp_1 += " " + word
                else: tmp_1 += word

                text_on_screen_tmp = font.render(tmp_1, False, BLACK)
                if (text_on_screen_tmp.get_width())> self.geometry[0] - font_size:
                    new_lines.append(tmp_0) # hopefully line will be not none
                    tmp_1 = word
                    tmp_0 = word
               
                else:
                    if len(tmp_0) > 1:
                        tmp_0 += " " + word
                    else: tmp_0 += word
            
            new_lines.append(tmp_0)
            self.new_lines = new_lines
                    

        


def draw_rects(Rect_lis):
    for rect in Rect_lis:
        rounded_rects.round_rect(game_display, (rect.pos[0],rect.pos[1],rect.geometry[0],rect.geometry[1]), rect.color, rad = 7)
        #pygame.draw.rect(game_display, rect.color,(rect.pos[0],rect.pos[1],rect.geometry[0],rect.geometry[1]))
        if len(rect.text) > 0:
            rect.write_text()
    



def draw_environment(Rect_lis):
    
    game_display.fill(WHITE)
    draw_rects(Rect_lis) # delete Rect_lis_const
    
    pygame.display.update()



def einblenden(Rect_lis, current_question, which_question, WIDTH, time_start):
    conti = True
    chosen = None
    while conti:
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            
            elif (event.type == pygame.locals.MOUSEBUTTONDOWN):

                for rect in Rect_lis[:4]:
                    rect.collidepoint(event.pos)
                    
                    if rect.chosen_rect:
                        if chosen:
                            chosen.chosen_rect = False
                            chosen.color = BLACK_GREY
                        rect.color = YELLOW
                        chosen = rect

                draw_rects([Rect_1, Rect_2, Rect_3, Rect_4])
                pygame.display.update()


                    
                if rect_continue.collision_only(event.pos) and chosen:
                    conti = False
                    right_rect, which_question = check_answer(Rect_lis, current_question, chosen, which_question)
                    
                    #draw_environment(Rect_lis)
                    #draw_rects(Rect_lis) 

            elif event.type is pygame.KEYDOWN and event.key == pygame.K_w:# and WIDTH == 1350:
                WIDTH = 800
                WIDTH = init_game(WIDTH)
                pygame.display.set_mode((WIDTH,HEIGHT))
                draw_environment(Rect_lis)#,Rect_lis_const)

            elif event.type is pygame.KEYDOWN and event.key == pygame.K_f:
                WIDTH = 800
                WIDTH = init_game(WIDTH)
                pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)

                draw_environment(Rect_lis) #Rect_lis_const)

        draw_rects([Time_line_outer_layer, Time_line])
        pygame.display.update()
            

         
        time_start[0] = setting.time_to_play- (time.time() - time_start[1])
        Time_line.geometry[0] = const_geometry * (time_start[0]/setting.time_to_play)
        if Time_line.geometry[0] < 12:
            Time_line.geometry[0] = 0

        if time_start[0] + 0.1 <= 0:
            right_rect, which_question = check_answer(Rect_lis, current_question, chosen, which_question)
            chosen = right_rect 
            for rect in Rect_lis:
                rect.chosen_rect = False
            break



    return chosen, right_rect, which_question

def check_answer(Rect_lis, current_question, chosen, which_question):
    if chosen:

        if chosen.text == current_question[1]:
            chosen.color = GREEN
            right_rect = chosen
            Rect_lis[-3+which_question].color = GREEN
            text_to_write = (current_question[0] + ";;" + chosen.text + ";;" + "1")
        else:
            chosen.color = RED
            Rect_lis[-3+which_question].color = RED
            text_to_write = (current_question[0] + ";;" + chosen.text+ ";;" + "0")
            
    else:
        text_to_write = (current_question[0] + ";;" + "Unbeantwortet"+ ";;" + "0")

        Rect_lis[-3+which_question].color = RED


    for rect in Rect_lis:
        if rect.text == current_question[1]:
            rect.color = GREEN
            right_rect = rect
       


    which_question += 1
    if which_question == 1: 
        for rect in Rect_lis[-2:]:
            rect.color = WHITE_grey
    draw_environment(Rect_lis)

    ################### print Statistics for each question ######################################################
    file_name = str(datetime.date.today().strftime("%d")) + "." +str(datetime.date.today().strftime("%B")) 
    # print(file_name)
    dictis.append_data("statistics/data/" + file_name, text_to_write )
    ###################
    # not only for the day !!! #
    dictis.append_data("statistics/data/" + "everything" , text_to_write )   #### important to delete if junk is in !!!!
    ###################

    which_question %= 3

    return right_rect, which_question

def init_game(WIDTH):
    global Rect_lis, Rect_lis_const, space_width, space_height, height_quest, position_rect, Rect_lis, rect_continue
    global first_game, second_game, third_game, space_width, space_height
    global Rect_Quest, Rect_1, Rect_2,Rect_3,Rect_4
    ### Position of the rectangles

    
    

    ### Question fields:
    height_quest = HEIGHT*4/10
    position_rect = [(0,HEIGHT/10-space_height/5),(0,HEIGHT*(1/2-1/45)), (WIDTH/2,HEIGHT*(1/2-1/45)), \
                    (0,HEIGHT*(7/10-1/45)), ( WIDTH/2,HEIGHT*(7/10-1/45)), (space_width,HEIGHT*0.4) ]

    Rect_Quest = Rect( BLACK_GREY, position_rect[0], text="Question", geometry = (WIDTH, height_quest)) ### pos and geometry has to be put together

    ### Answer fields : 
    Rect_1 = Rect( BLACK_GREY, position_rect[1], text="Answer", geometry = (WIDTH/2, HEIGHT*2.2/10)) ### pos and geometry has to be put together
    Rect_2 = Rect( BLACK_GREY, position_rect[2], text="Answer", geometry = (WIDTH/2, HEIGHT*2.2/10)) ### pos and geometry has to be put together
    Rect_3 = Rect( BLACK_GREY, position_rect[3], text="Answer", geometry = (WIDTH/2, HEIGHT*2.2/10)) ### pos and geometry has to be put together
    Rect_4 = Rect( BLACK_GREY, position_rect[4], text="Answer", geometry = (WIDTH/2, HEIGHT*2.2/10)) ### pos and geometry has to be put together

    ### space for source
    Rect_source = Rect( BLACK_GREY, position_rect[5], text="", geometry = (WIDTH, height_quest * 0.1), mode="source") ### pos and geometry has to be put together

    rect_continue = Rect (BLUE, (WIDTH-WIDTH*2/8 ,HEIGHT*8.8/10), text="Weiter", geometry =(WIDTH*2/8,HEIGHT/12) )
    ### continue_pos = (WIDTH/2-WIDTH/8 ,3/4*HEIGHT-HEIGHT/35)

    
    Rect_lis = [Rect_1, Rect_2, Rect_3, Rect_4, Rect_Quest, Rect_source,rect_continue, Time_line_outer_layer, Time_line, first_game, second_game, third_game]
    return WIDTH

###    
space_width, space_height = WIDTH/50, HEIGHT/25
### small rectangles above the questionmaker
first_game = Rect (WHITE_grey, (0 ,HEIGHT*1/50), text="", geometry =(WIDTH*1/9,HEIGHT*1/12) )
second_game = Rect (WHITE_grey, (WIDTH*1/9-space_width*0.5  ,HEIGHT*1/50), text="", geometry =(WIDTH*1/9,HEIGHT*1/12) )
third_game = Rect (WHITE_grey, ( 2*(WIDTH*1/9-space_width*0.5 ) ,HEIGHT*1/50), text="", geometry =(WIDTH*1/9,HEIGHT*1/12) )

### time rectangle
diff = WIDTH/100 ## difference inner and outer layer
Time_line_outer_layer = Rect (dark_BLUE, (WIDTH*0/8 ,HEIGHT*8.8/10), text="", geometry =(WIDTH*6/8,HEIGHT/12 ) )
Time_line             = Rect (fresh_green, (WIDTH*0/8+diff/2 ,HEIGHT*8.8/10+diff/2), text="", geometry =[WIDTH*6/8-diff,HEIGHT/12-diff] )
const_geometry = Time_line.geometry[0]

WIDTH = init_game(WIDTH)



def main():

    which_question = 0
    
    file_path_everything = "statistics/data/everything"

    if os.path.exists(file_path_everything):
        pass
    else: 
        dictis.make_txt_doc(file_path_everything)

    quest_dictionary = dictis.get_information_for_chart()

    visits_today = 0


    while True:
        visits_today += 1

        clock.tick(35)

        ### Start_page (Question_rectangle --> Introduction)
        Rect_lis[5].text = "" # source
        Rect_lis[4].text = "Hallo, viel Erfolg mit den {} Fragen über Religion und Politik. Sie sind die {}. Person heute, die an dem Quiz teilnimmt.".format(len(dicties), visits_today)
        Rect_lis[4].init_text()

        for rect in Rect_lis[:4]:
            rect.text = ""
            rect.color = WHITE
        
        rect_continue.text = "Start"
        draw_environment(Rect_lis)
        not_clicked = True
        while not_clicked:
            clock.tick(35)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
        
                elif (event.type == pygame.locals.MOUSEBUTTONDOWN):
                    if rect_continue.collision_only(event.pos):
                        not_clicked = False
                ### elif enter??
        #############################################################################

        ### All questions will be asked in the same order ### 
        for text_input in dicties: ## dicties = Quiz_Questions ### +1 für die Quelle
            draw_environment(Rect_lis)
            not_clicked = True

            ### source = text_input[5]
            if text_input[5] == "":
                Rect_lis[5].text = "" # source
            else: 
                Rect_lis[5].text = "Quelle: " + text_input[5]   # source

            current_question = text_input[0]
            right_answer = text_input[1]

            Rect_lis[4].text = current_question

            tmp_list = text_input[1:5]
            for rect in Rect_lis[:4]:
                tmp = random.choice(tmp_list)
                rect.text = tmp
                tmp_list.remove(tmp)
                rect.color = BLACK_GREY
                
            rect_continue.text = "Weiter"
            
            for rect in Rect_lis: 
                rect.init_text()    ##### check if lines need to be split up
            
            draw_rects([Rect_Quest, Rect_1, Rect_2, Rect_3, Rect_4])
            

            chosen, right_rect, which_question = einblenden(Rect_lis, text_input, which_question, WIDTH, time_start = [setting.time_to_play, time.time()])
            
            
            if chosen.text in quest_dictionary[current_question]:
                quest_dictionary[current_question][chosen.text] = quest_dictionary[current_question][chosen.text] + 1 
                               
            else: print("{} not in quest_dictionary".format(chosen.text))

            ### update chart_diagram
            #
            dictis.draw_chart(current_question, right_answer, quest_dictionary)

            
            while not_clicked:
                clock.tick(35)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            
            
                    elif (event.type == pygame.locals.MOUSEBUTTONDOWN):
                        if rect_continue.collision_only(event.pos) and chosen:
                            not_clicked = False
            
            ### if diagram exists, open it.
            #
            ### deletes "/" in question, which would raise an error with the file_path
            #
            if "/" in current_question:
                changed_question = ""
                for i in current_question:
                    if i != "/":
                        changed_question += i
            else: changed_question = current_question
            ########################################################################
            chart_path = "statistics/charts/everything/" + changed_question + ".png"
            ########################################################################
            

            if os.path.exists(chart_path):
                img_chart = pygame.image.load(chart_path)
                
                game_display.blit(img_chart, ((WIDTH-img_chart.get_width())/2,(HEIGHT-img_chart.get_height())/2))
                pygame.display.update()
            
                not_clicked = True
                while not_clicked:
                    clock.tick(35)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                
                
                        elif (event.type == pygame.locals.MOUSEBUTTONDOWN):
                            if rect_continue.collision_only(event.pos) and chosen:
                                not_clicked = False
                
        #######################################################################

        ### Final Page         
        Rect_lis[5].text = "" # source
        Rect_lis[4].text = "Vielen Dank für die Teilnahme an unserem Quiz.".format(len(dicties))
        Rect_lis[4].init_text()
        
        for rect in Rect_lis[:4]:
            rect.color = WHITE
            rect.text = ""


        rect_continue.text = "Zum Anfang!"
        
        draw_environment(Rect_lis)
        not_clicked = True

        

        while not_clicked:
            clock.tick(35)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
        
                elif (event.type == pygame.locals.MOUSEBUTTONDOWN):
                    if rect_continue.collision_only(event.pos):
                        not_clicked = False

        
        
if __name__ == '__main__':
    main()


