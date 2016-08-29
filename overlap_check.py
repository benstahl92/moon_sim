# checks to see if any rocks are overlapping (within) the Earth and removes them
# Written by Benjamin Stahl

# import necessary function definitions
import numpy as np
from rock import Rock # import Rock class

# function that checks for overlaps and removes if necessary
# arguments:
#	planet: rock instance for the Earth (or other planet)
#	rock_list: list of rock instances
# returns an updated rock_list with overlaps removed
def out_check(planet, rock_list):

	# convert rock_list to a numpy array
	rock_list = np.array(rock_list)
	
	# create a boolean array of the same length as rock_list containing False for every element
	t_arr = np.zeros(len(rock_list),dtype=bool)
	
	# create a counter and loop through the rock_list
	ctr = 0
	for i in rock_list:
		# calculate the distance between a rock and the planet
		d = np.sqrt((i.x_pos - planet.x_pos)**2 + (i.y_pos - planet.y_pos)**2)
		
		# if the distance is greater than the radius of the planet make the element
		#	with index corresponding to the index of the rock in rock_list True in t_arr
		if d > planet.radius:
			t_arr[ctr] = True
		
		# increment the counter
		ctr += 1
		
	# return an updated rock_list with overlaps removed by selecting only the indices of
	#	rock_list that correspond to the indices containing True in t_arr
	return list(rock_list[t_arr])
		