

WHITE = (255, 255, 255)
BLACK = (0,0,0)
black_Grey= (50,50,50)
Grey = (160,160,160)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
ORANGE = (255,255,0)

dark_field = (100,120,50)
white_field = (200,200,255)

#        # + # + # + # + # + #
#        + # + # + # + # + # +
#        # + # + # + # + # + #
#        + # + # + # + # + # +
#        # + # + # + # + # + #
#        + # + # + # + # + # +
#        # + # + # + # + # + #
#        + # + # + # + # + # +
# --> creates position of white and black fields
pos_even = [x for x in range(64) if x % 2 == 1]
pos_odd = [x for x in range(64) if x % 2 == 0]

pos_black = []
pos_white = []
for i in range(len(pos_even)):
    if i % 8 < 4:
        pos_black.append(pos_even[i])
        pos_white.append(pos_odd[i])
    else:
        pos_black.append(pos_odd[i])
        pos_white.append(pos_even[i])

########################################################################
# initial stone positions
stones_black = pos_black[:12]
print(stones_black)
stones_white = pos_black[-12:]

# convert position of integers in computer interpreted positions
# -> in the window



########################################################################
########################################################################