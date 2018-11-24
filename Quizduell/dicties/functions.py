import matplotlib.pyplot as plt
import os


def read_data(name):
    dictie = []
    fungua = open(name).readlines()
    
    for line in fungua:
        current_inp = line.strip("\n").split(";;")
        
        dictie.append(current_inp)

    return dictie

def make_txt_doc(name):
    with open(name, "a") as out_file:
        out_file.write("")


def write_data(name, dictie):
    with open(name, "a") as out_file:
        for i in range(len(dictie)):
            p = "\n"
            p = str(dictie[i])
            p += ";;"
            out_file.write(p)
        out_file.write("\n")


def append_data(name,dictie):
    with open(name, "a") as out_file:
        for i in range(len(dictie)):
            p = ""
            p += str(dictie[i])
            
            out_file.write(p)
        out_file.write("\n")


def get_information_for_chart():
    questions = {}
    data = (read_data("statistics/data/everything"))
    raw_questions = (read_data("dicties/quests.txt"))

    for quests in data:
        
        if quests[0] not in questions:
            questions[quests[0]] = [[],[]]
        
        if quests[-1] == "1":
            questions[quests[0]][0].append(quests[-2])
        else:
            questions[quests[0]][1].append(quests[-2])

    ##### questions is a dictionary in which all right answers are saved in the first list and all wrong answers in the second list

    
    quest_dictionary = {}

    for quest_answers in raw_questions:

        if quest_answers[0] in questions:
            
            #answer_possib = [quest_answers[i] for i in range(1,5)] + ["None"] + [" "]
            for i in range(1,5) :

                if i == 1:
                    right_answers = questions[quest_answers[0]][0].count(quest_answers[i])
                    quest_dictionary[quest_answers[0]] = {quest_answers[i] : right_answers}
                    
                else:
                    wrong_answers = questions[quest_answers[0]][1].count(quest_answers[i])  
                    quest_dictionary[quest_answers[0]].update({quest_answers[i] : wrong_answers})

            None_answers = questions[quest_answers[0]][1].count("Unbeantwortet") + questions[quest_answers[0]][1].count(" ")

            if None_answers > 0:
                quest_dictionary[quest_answers[0]].update({"Unbeantwortet" : None_answers})
        else:
            
            quest_dictionary[quest_answers[0]] = {quest_answers[1] : 0}
            for i in range(2,5) :
                quest_dictionary[quest_answers[0]].update({quest_answers[i] : 0})
            quest_dictionary[quest_answers[0]].update({"Unbeantwortet" : 0})



    return quest_dictionary


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:1.1f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def draw_chart(current_question, right_answer, quest_dictionary):

    
    labels = [x for x in quest_dictionary[current_question] if quest_dictionary[current_question][x] != 0]
    try:
        labels.remove(right_answer)
        labels = [right_answer] + labels
        colors = ['green', 'red','orange','purple', 'yellow']

    except:
        print("Is the right answer green?")
        colors = ['red','orange','purple', 'yellow']




    sizes = [quest_dictionary[current_question][y] for y in labels if quest_dictionary[current_question][y] != 0]
    
    explode = [0.2]
    explode += (len(labels)-1) * [0]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors[0:len(labels)+1], autopct= make_autopct(sizes),
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    title_chart =  current_question
    length_title = 60
    


    if len(title_chart) > length_title:
        middle_position = int(length_title*5/6)
        for cutting_point in range(middle_position,middle_position + 11):
            if title_chart[cutting_point] == " ":
                plt.title(title_chart[:cutting_point] + "\n" + title_chart[cutting_point:])
                break
    else: plt.title(title_chart)


    folder_name = "statistics/charts/everything/"
    if os.path.exists(folder_name):
        pass
    else:
        os.mkdir( folder_name )

    
    if "/" in current_question:
        changed_question = ""
        for i in current_question:
            if i != "/":
                changed_question += i
    else: changed_question = current_question

    plt.savefig(folder_name + changed_question)


