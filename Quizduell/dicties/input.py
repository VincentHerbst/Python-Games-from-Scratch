import functions as fun


file_name = "quests.txt"

while True:
	quest_group = []

	print("Next question to add is:")
	quest_group.append(input())
	print("The right answer is:")
	quest_group.append(input())
	print("Another answers are:")
	for i in range(3):
		quest_group.append(input())
	
	print("From which source do you have this information?")
	quest_group.append(input())

	print(quest_group)

	#print("\nDo want to take this question in your set? If no, write N or n\n")
	#ans = input()
	#if ans == "n" or ans == "N" or ans == "no":
	#	pass
	#else:
	
	fun.write_data(file_name, quest_group)
	