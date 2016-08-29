# Class definition and global variables
# Written by the group.

# import necessary function definitions
import numpy as np

# define 'global variables'
dens=2.650e3 # density of rock in kg/m**3

# define class called Rock
# arguments:
#	x,y: x and y position of a rock
#	vs,vy: velocity in x and y components of a rock
#	m: mass of a rock
# attributes:
#	x_pos,y_pos: x and y position
#	x_vel,y_vel: velocity in x and y components
#	mass: mass
#	radius: radius calculated using the defintion of density with global variable (dens)
class Rock:
	def __init__(self, x, y, vx, vy, m):
		self.x_pos = x
		self.y_pos = y
		self.x_vel = vx
		self.y_vel = vy
		self.mass = m
		self.radius = ((3.*m)/(4. * np.pi * dens))**(1./3.)