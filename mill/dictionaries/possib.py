def possibilities_for_stone():
	# returns list of possible targets for one stone

	pos_mill = [0,3,6,8,10,12,16,17,18,21,22,23,25,26,27,30,31,32,36,38,40,42,45,48]

	vertical_mills = [[[]] for x in range(7)]
	horizontal_mills = [[[]] for x in range(7)]

	### Ausnahme
	vertical_first = []
	vertical_second = []

	horizontal_first = []
	horizontal_second = []
	###

	for i in pos_mill:
		for z in range(7):
			if i % 7 == z:
				if z == 3:
					if i // 7 < 3:
						vertical_first.append(i)
					else:
						vertical_second.append(i)

				else:
					vertical_mills[z][0].append(i)

			if i // 7 == z:
				if z == 3:
					if i % 7 < 3:
						horizontal_first.append(i)
					else:
						horizontal_second.append(i)
				else:
					horizontal_mills[z][0].append(i)

	vertical_mills[3] = [vertical_first, vertical_second]
	horizontal_mills[3] = [horizontal_first, horizontal_second]
		
	dictionary_moves = {}
	for num in pos_mill:

		possible_moves = []

		if (num % 7 == 3):
			if num // 7 > 3:
				V = 1
			else:
				V = 0
		else: V = 0

		if (num // 7 == 3):
			if num % 7 > 3:
				H = 1
			else:
				H = 0
		else: H = 0


		if horizontal_mills[num//7][H].index(num) == 1:
			possible_moves.append(horizontal_mills[num//7][H][0])
			possible_moves.append(horizontal_mills[num//7][H][2])
		else:
			possible_moves.append(horizontal_mills[num//7][H][1])

		if vertical_mills[num%7][V].index(num) == 1:
			possible_moves.append(vertical_mills[num%7][V][0])
			possible_moves.append(vertical_mills[num%7][V][2])
		else:
			possible_moves.append(vertical_mills[num%7][V][1])

		dictionary_moves.update({num: possible_moves})
	

	return (dictionary_moves, horizontal_mills, vertical_mills)



'''
0 [3, 21]
3 [0, 6, 10]
6 [3, 27]
8 [10, 22]
10 [8, 12, 3, 17]
12 [10, 26]
16 [17, 23]
17 [16, 18, 10]
18 [17, 25]
21 [22, 0, 42]
22 [21, 23, 8, 36]
23 [22, 16, 30]
25 [26, 18, 32]
26 [25, 27, 12, 40]
27 [26, 6, 48]
30 [31, 23]
31 [30, 32, 38]
32 [31, 25]
36 [38, 22]
38 [36, 40, 31, 45]
40 [38, 26]
42 [45, 21]
45 [42, 48, 38]
48 [45, 27]

'''