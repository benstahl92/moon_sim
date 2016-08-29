# This file contains the functions that generate the initial conditions of simulation
# The primary function that should be called in the main function is initial
# Written by Benjamin Stahl and Jarred Gillette

# import necessary function definitions
import numpy as np
import numpy.random as rnd
import scipy.constants as sc
from rock import Rock # the Rock class that is contained in rock.py

# function to generate a random gaussian distribution
# assumes a variance using Poisson statistics
# arguments:
#	mu: mean of the distribution
#	N: number of elements in the distribution
# returns the random distribution
def grandom(mu,N):
    # Mean ("center") of the distribution, Std, Output shape
    noise = np.random.normal(loc=mu, scale=np.sqrt(mu), size=N)
    return noise

# function to generate the initial conditions
# arguments:
#	N: number of rocks to generate initially
#	moon_mass: total mass of the generated rocks
#	moon_dist: average current distance from the moon to Earth
#	M: Earth mass
# returns a rock instance for the Earth and a list of rock instances (one for each rock)
def initial(N,moon_mass,moon_dist,M):

	# average mass of an object
	mu = moon_mass/N 
	
	# generate random parameters
	rand_mass = grandom(mu,N)
	rand_a = grandom(moon_dist,N)
	rand_e = rnd.rand(N)

	# convert input arrays to float64 type
	a = np.float64(rand_a)
	e = np.float64(rand_e)
	m = np.float64(rand_mass)
	
	# calculations are done using formulas from class 11
    # mass ratio 'q', total mass, initial distance, initial velocity
	q = np.float64(m/M)
	m_tot = np.float64(m + M)
	r_init = ((1. - e)/(1. + q)) * a
	v_init = (1./(1. + q)) * np.sqrt((1. + e)/(1. - e)) * np.sqrt(sc.G * m_tot/a)
	
	# generate N equally likely random angles between 0 and 2pi 
	ang = rnd.rand(len(a)) * 0.5 * np.pi
	
	# randomize the sign of the velocities
	vx = []
	vy = []
	for i in range(len(a)):
		vel_sign = rnd.rand(1)
		if vel_sign <= 0.8:
			vx.append(-v_init[i] * np.sin(ang[i]))
			vy.append(v_init[i] * np.cos(ang[i]))
		elif vel_sign <= 0.9:
			vx.append(v_init[i] * np.sin(ang[i]))
			vy.append(-v_init[i] * np.cos(ang[i]))
		else:
			vx.append(v_init[i] * np.sin(ang[i]))
			vy.append(v_init[i] * np.cos(ang[i]))
	
	# convention: x for particle 1 and X for Earth
	# calculate the locations and velocities of rocks and Earth
	# nb: it is not redundant that the Earth is included in each calculation because
	# 	the effect of each rock on it must be considered, these contributions will
	#	be summed later
	x = r_init * np.cos(ang)
	y = r_init * np.sin(ang)
	X = 0#-q * r_init * np.cos(ang)
	Y = 0#-q * r_init * np.sin(ang)
	vX = 0#-q * v_init * np.sin(ang)
	vY = 0#-q * v_init * np.cos(ang)
	
	# create a Rock instance for the Earth by taking the sum of all the Earth positions
	# and velocities
	Earth = Rock(np.sum(X),np.sum(Y),np.sum(vX),np.sum(vY),M)
	
	# create a Rock instance for each of the objects generated
	rocks = [] # create list to hold the rocks
	for i in range(len(a)):
		rocks.append(Rock(x[i],y[i],vx[i],vy[i],m[i]))
	
	# determine the minimum period of the cleaned initial condition rocks
	P = []
	for i in rocks:
		P.append(np.sqrt((4 * np.pi**2 * a**3)/(sc.G*(i.mass + M))) )# seconds
	P_min = np.min(np.array(P))
	
	# return
	return Earth, rocks, P_min


	
