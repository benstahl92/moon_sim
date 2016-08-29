# Plotting functions for the orbital system
# Written by Cesar Gonzalez Renteria and Benjamin Stahl

# import necessary functions and class definitions
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rock import Rock # rock class definition


# define plotting function: gen_plot
# will plot the positions of the rocks and planet
# Mandatory arguments
#	rock_list: the list of rocks
#	Earth: The instance for Earth
#       density: The density of the rocks
# Optional arguments:
#	window: specifies figure window (def: 1)
#	orb_step: orbital time step that the simulation is on
#	unit_scale: multiplier to convert from meters to another unit (def: 1)
#	unit_name: unit scaled to (def: 'm')
def gen_plot(rock_list, Earth, moon_dist, max_mass, max_index, dist_scale, save, window = 1, orb_step = 0, unit_conv = (1.,'m'),p_scale = 1.,r_scale = 1.,n_col=0.0,frac_comp = 0.0,count=False):
	
	# open/move to specified figure window
	fig = plt.figure(window,figsize=(8,8))
	
	# clear the figure in case there is anything left from before
	fig.clf()
	
	# create two subplots 
	ax = fig.add_subplot(111,adjustable='box', aspect=1.0)
 
	# set x and y limits of the subplot to a multiple of moon_dist
	ax.set_xlim([-dist_scale*unit_conv[0]*moon_dist,dist_scale*unit_conv[0]*moon_dist])
	ax.set_ylim([-dist_scale*unit_conv[0]*moon_dist,dist_scale*unit_conv[0]*moon_dist])
	
	# label axes
	ax.set_xlabel(r'$x$ Position ({})'.format(unit_conv[1]))
	ax.set_ylabel(r'$y$ Position  ({})'.format(unit_conv[1]))
	
	# plot Earth
	earthCircle = plt.Circle((Earth.x_pos, Earth.y_pos), radius = Earth.radius *p_scale, color = 'g', label='Earth')
	fig.gca().add_artist(earthCircle)
	
	# plot each rock
	i = rock_list[0]
	rockCircle_s = plt.Circle((i.x_pos, i.y_pos), radius = i.radius*r_scale, color = 'k', label='Rocks')
	fig.gca().add_artist(rockCircle_s)
	i = rock_list[max_index]
	rockCircle_l = plt.Circle((i.x_pos, i.y_pos), radius = i.radius*r_scale, color = 'r', label='Largest Rock')
	fig.gca().add_artist(rockCircle_l)
	for i in rock_list:
		if i != rock_list[0]:
			if i != rock_list[max_index]:
				rockCircle = plt.Circle((i.x_pos, i.y_pos), radius = i.radius*r_scale, color = 'k')
				fig.gca().add_artist(rockCircle)
	    		
	# add a title to the plot
	ax.set_title('Moon Formation Simulation')

	l = 0.02
	h = 0.16
	
	# add text
	ax.text(l, h, 'Elapsed Time: {:6.4f} months'.format(orb_step*3.805e-7), 
			verticalalignment='center',
			transform=ax.transAxes)
			
	# add text
	ax.text(l, h-0.03, 'Simulation Progress: {:6.3f}%'.format(100.*frac_comp), 
			verticalalignment='center',
			transform=ax.transAxes)
			
	# add text
	ax.text(l, h-0.06, 'Number of Rocks: {}'.format(len(rock_list)), 
			verticalalignment='center',
			transform=ax.transAxes)
			
	# add text
	ax.text(l, h-0.09, 'Largest Rock: {:6.2e} kg'.format(max_mass), 
			verticalalignment='center',
			transform=ax.transAxes)
			
	# add text
	ax.text(l, h-0.12, 'Collisions: {}'.format(n_col), 
			verticalalignment='center',
			transform=ax.transAxes)
			
	plt.legend([rockCircle_s,rockCircle_l,earthCircle], ['Rocks','Largest Rock','Earth'],loc='lower right')
		
	if save == False:
		plt.draw()
	else:
		plt.savefig(save+ '_{:08}.png'.format(count))
		plt.close(fig)
	
	# return nothing
	return None