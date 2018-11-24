import time

# (15)(14)(13)(12)(11)(10)(9 )(8 )  ((  ))
# (0 )(1 )(2 )(3 )(4 )(5 )(6 )(7 )	Comp
# --------------------------------
# (0 )(1 )(2 )(3 )(4 )(5 )(6 )(7 )  ((  ))
# (15)(14)(13)(12)(11)(10)(9 )(8 )	Player


def UpdateScreen(Comp,Player, Supply_Comp ,Supply_Player):
	print()
	print("(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)  ((%2s))"%(tuple([Comp[i] for i in range(15,7,-1)]+[Supply_Comp]))) # first line comp
	print("(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)  Comp"%(tuple([Comp[i] for i in range(8)])))
	print("--------------------------------")
	print("(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)  ((%2s))"%(tuple([Player[i] for i in range(8)]+ [Supply_Player]))) # first line Player
	print("(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)(%2s)  Player"%(tuple([Player[i] for i in range(15,7,-1)])))
	print()

def possibilites(Comp,Player):
	possibilities_Go  = []
	possibilities_Eat = []
	for i in range(8):
		if Player[i] != 0:
			possibilities_Go.append(i)
			if Comp[i] != 0:
				possibilities_Eat.append(i)
	return [possibilities_Go,possibilities_Eat]

def StartEating(possibilities_Eat):
	print("You have to eat.")
	Choice = ""
	while Choice not in possibilities_Eat:
		Choice = eval(input("Where do you want to start? {} are the possibilities.".format(possibilities_Eat)))
	return Choice

def AfterEating(pos, direction):
	
	if pos in [0,1]:
		start = 0
	elif pos in [6,7]:
		start = 7
	else:
		if direction == 1:
			start = 0
		else:
			start = 7
	if start == 7:
		direction = -1
	else:
		direction = 1
	return [pos,start,direction]

def AfterEatingFirstTime(pos):
	
	time.sleep(1)
	Choice = pos 
	
	if Choice in [0,1]:
		start = 0
	elif Choice in [6,7]:
		start = 7
	else:
		start = ""
		while start not in [0,7]:
			start = eval(input("Where to start? Left: {} right: {}".format(0,7)))
	if start == 7:
		direction = -1
	else:
		direction = 1
	return [Choice,start,direction]

def startWithoutEating(possibilities_Go):
	print("You have to go without eating.")
	Choice = ""
	while Choice not in possibilities_Go:
		Choice = eval(input("Where do you want to start? {} are the possibilities.\n".format(possibilities_Go)))

	if Choice in [0,1]:
		direction = 1
	elif Choice in [6,7]:
		direction = -1
	else:
		direction = ""
		while direction not in [1,-1]:
			direction = eval(input("For right enter {} and for left enter {}.\n".format(1,-1)))
	return [Choice,direction]

def go(Comp,Player, start, direction, tmpHand, Supply_Comp,Supply_Player):
	time.sleep(1)
	for balls in range(tmpHand):
		pos = start + balls * direction
		if pos > 15:
			pos = pos - 16
		elif pos < 0:
			pos = pos + 16

		Player[pos] += 1
		UpdateScreen(Comp,Player,Supply_Comp,Supply_Player)
		print("... You are going with the {}. ball ...".format(balls+1))
		time.sleep(0.8)
	return [Player, pos, 0] # tmpHand = 0

def main():
	# initial conditions
	Comp = 	 [0,0,0,0,4,3,3,0]+[0 for x in range(8)]
	Player = [0,3,3,4,0,0,0,0]+[0 for x in range(8)]
	################################################
	Supply_Player = 22
	Supply_Comp   = 22
	
	UpdateScreen(Comp,Player, Supply_Comp,Supply_Player )	
	

	##### Real Code
	################################################
	#while (sum(Comp[:8]) != 0  and sum(Player[:8]) != 0):
	#	UpdateScreen(Comp,Player)
	#''' ############################# how to make a class!!! otherwise I have to make two
	possibilities_Eat = []
	possibilities_Go  = []
	while (sum(Comp[:8]) != 0  and sum(Player[:8]) != 0):

		if Supply_Player != 0:
			tmpHand = 1
			Supply_Player -= 1

			possibilities_Go, possibilities_Eat = possibilites(Comp,Player)
						
			if len(possibilities_Eat) != 0:
				Beginning = StartEating(possibilities_Eat)
				choice, start, direction = AfterEatingFirstTime(Beginning)
				Player[choice] += 1
				tmpHand -= 1
				tmpHand += Comp[choice]
				Comp[choice] = 0
				mode = "eat" 

			elif len(possibilities_Go) != 0:
				choice,direction = startWithoutEating(possibilities_Go) #### malus = 1 --> cannot eat!!!
				start = choice + direction
				tmpHand += Player[choice]
				Player[choice] = 0
				mode = "justGo"
			
			### go ###
			Player, pos, tmpHand = go(Comp,Player, start, direction, tmpHand, Supply_Comp,Supply_Player)
			#tmpHand = 0

			### continue - eating or going ###
			while Player[pos] > 1:
				if (pos in range(8)) and (Comp[pos] > 0) and (mode == "eat"): ## if not have eat in the first round mode "justGo"
					pos, start, direction = AfterEating(pos,direction)
					tmpHand += Comp[pos]
					Comp[pos] = 0
					print(start)
					Player, pos, tmpHand = go(Comp,Player, start, direction, tmpHand, Supply_Comp,Supply_Player)

				else:
					start = pos + direction
					tmpHand += Player[pos]
					Player[pos] = 0


					Player, pos, tmpHand = go(Comp,Player, start, direction, tmpHand,Supply_Comp,Supply_Player)

					#continueGoing(,mode) ##

				

				



			##########	
			#else: ### supply == 0
				### go with one (more than 1 containing .. and has to eat)
				#tmpHand = 0

				#for i in range(16):
				#	if Player[i] != 0:
				#		possibilities_Go.append(i)				
						####### more complicated --- possibilities_Eat append 


	#'''
	################################################


	### while 1. line of each player is not empty ...
		### Update
		
		### two ways : 
			### 1. with Supply 
			### 2. Supply == 0

		### Check Possibilities --- this is the possible insert or the random movement of comp
		### choice of Move + ...
		### calculation  (go + eat(if last move ...))  delayed --to show the player-- ... 
			### decision where to go, if there is on ? RIGHT or LEFT

		### next player



if __name__ == '__main__':
	main()















































##### Real Code
	################################################
	#while (sum(Comp[:8]) != 0  and sum(Player[:8]) != 0):
	#	UpdateScreen(Comp,Player)
	''' ############################# how to make a class!!! otherwise I have to make two
		possibilities_Eat = []
		possibilities_Go  = []

		if supply != 0:
			tmpHand = 1
			supply -= 1

			for i in range(8):
				if Player[i] != 0:
					possibilities_Go.append(i)
					if Comp[i] != 0:
						possibilities_Eat.append(i)
			
			if len(possibilities_Eat) != 0:
				print("You have to eat.")
				mode = "eat"

				Choice = ""
				while Choice not in possibilities_Eat:
					Choice = input("Where do you want to start? {} are the possibilities.".format(possibilities_Eat))
				
				if mode == "eat":
					if Choice in [0,1]:
						start = 0
					elif Choice in [6,7]:
						start = 7
					else:
						start = ""
						while start not in [0,7]:
							start = input("Where do you want to start? For left enter {} and for right enter {}".format(0,7))
				#else: # mode = "go"
					# start = last position ... 

			else: ### nothing to eat
				####  -->>>>>>>>  do i need to copy that or can I just make the list variable



		else: ### supply == 0
			### go with one (more than 1 containing .. and has to eat)
			tmpHand = 0

			for i in range(16):
				if Player[i] != 0:
					possibilities_Go.append(i)				
					####### more complicated --- possibilities_Eat append
					'''
