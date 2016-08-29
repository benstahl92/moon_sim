# the main file that controls the simulation
# Written by the group

# import function and class definitions
import initial
import AraLuc_Trynewthings as check
import plot_c
import numpy as np
import adv
import overlap_check as oc
import pickle
from rock import Rock

# main function definition that runs the simulation
# arguments:
#	N: number of rocks to generate (1000 by default)
#	moon_mass: total mass of the rocks to generate (default to moon mass)
#	moon_dist: mean distance from planet to satellite (default to Earth-Moon distance)
#	M: mass of planet (default to Earth mass)
#	tstep: timestep of the simulation
#	tmax: duration of the simulation
#	plot_int: plot interval (in terms of time steps)
#	save: name of file to save to
def main(N=500,moon_mass=4*7.3459e22,moon_dist=0.5*3.864e8,M=5.972e24, tstep=0, tmax=1.0e7, plot_int = 10., dist_scale = 1.,save='simulation'):

	# generate initial conditions (planet and list of rocks)
	planet, rock_list, P_min = initial.initial(N,moon_mass,moon_dist,M)
	
	# check for (and remove) any overlaps of rocks with the planet from initial conditions
	rock_list = oc.out_check(planet, rock_list)
	
	# check for and handle any collisions in the rocks from initial conditions
	rock_list, collision_count_init, max_rad, max_mass, max_index = check.c_finder(rock_list)
	
	# plot the initial conditions
	plot_c.gen_plot(rock_list,planet,moon_dist, max_mass, max_index, dist_scale, save, n_col=collision_count_init)
	
	# if tstep is not specified by the user, set it to 1000th of the smallest period from
	#	initial conditions and round up
	if tstep == 0:
		tstep = P_min/15000.
		
	print 'Commencing the simulation...'
	print '    Initial Time Step: {}'.format(tstep)

	# create a counter for total collisions and loop through time steps
	tot_col_cnt = 0
	ctr = 0
	metrics = []
	for j in np.arange(0 , tstep + tmax, tstep):

		# advance the rocks by one step
		rock_list = adv.advOdeInt(rock_list, tstep, planet)
		
		# check and handle any overlaps of the rocks and planet
		rock_list = oc.out_check(planet, rock_list)
		
		# check for and handle collisions
		rock_list, collision_count, max_rad, max_mass, max_index = check.c_finder(rock_list)
		
		# increment the total collision counter if a collision(s) occur
		tot_col_cnt += collision_count
		
		metrics.append((j,max_mass,collision_count))
	    
		# if the appropriate time step, then plot the system
		if ctr % plot_int == 0:
			plot_c.gen_plot(rock_list,planet,moon_dist, max_mass,max_index,dist_scale,save,orb_step=j,n_col=tot_col_cnt+collision_count_init,frac_comp=j/(tstep+tmax),count=int(ctr/plot_int))
		
		ctr += 1
		
	rem_mass = 0
	for i in rock_list:
		rem_mass += i.mass
	print 'Remaining Mass in System: {}'.format(rem_mass)
		
	# save the metrics to a pickle file:
	print 'Saving simulation iteration information to {}_metrics.pkl ...'.format(save)
	f = open(save+'_metrics.pkl', 'wb')
	pickle.dump(metrics, f)
	f.close()

	# save simulation information to a txt file
	print 'Saving simulation info to {}_stats.txt ...'.format(save)
	f = open(save+'_stats.txt', 'w')
	f.write('Moon creation simulation information\n')
	f.write('Initial number of rocks: {}\n'.format(N))
	f.write('Initial mean distance: {} m\n'.format(moon_dist))
	f.write('Initial total mass: {} kg\n'.format(moon_mass))
	f.write('Earth mass: {} kg\n'.format(M))
	f.write('Simulation time step: {} s\n'.format(tstep))
	f.write('Plotting interval: {}\n'.format(plot_int))
	f.write('Simulation run time: {} s\n'.format(tmax))
	f.write('Moon mass: {} kg\n'.format(rock_list[max_index].mass))
	f.write('Remaining mass in rocks: {}\n'.format(rem_mass))
	f.write('Remaining number of rocks: {}\n'.format(len(rock_list)))
	f.write('Earth-Moon Distance: {} m\n'.format(np.sqrt(rock_list[max_index].x_pos**2 + rock_list[max_index].y_pos**2)))
	f.close()
	
	
