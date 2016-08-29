# Advance the pos. and vel. of each object
# Cesar Gonzalez Renteria and Monique Windju

# FUNCTIONS CONTAINED:
##  derivs       ## adv0deInt

# When called in main.py: 
    # Uses the Rock class and constants defined in rock.py
    # Requires the output of initial.py 

import numpy as np
import scipy.constants as sc
import scipy.integrate as integ
from rock import Rock

# --DERIVS--        Args:
# Rock_array: The objects that interact with the central body (eg: planet)
# t: A necessary variable
# planet_mass: mass of planet
# planet_radius: radius of planet

def derivs(Rock_array, t, planet_mass, planet_radius):
    
    # Distance between the center of the planet and the moving objects   
    r = np.sqrt((Rock_array[0])**2 + (Rock_array[1])**2)
    rsoft = 1.E-3 * planet_radius
    # Defines derivatives to be used in advOdeInt.    
    dxdt = Rock_array[2]
    dydt = Rock_array[3]
    dvxdt = (sc.G*planet_mass*(-Rock_array[0]/r))/(r**2 + rsoft**2)
    dvydt = (sc.G*planet_mass*(-Rock_array[1]/r))/(r**2 + rsoft**2)
    
    return np.array([dxdt, dydt, dvxdt, dvydt])
    

# --ADV0DEINT--     Args:
# rock_list: passed from initial(), list of objects 
# tstep: upper limit on timestep for each instance 
# Planet: Object called and stored in an array for use in derivs
    
def advOdeInt(rock_list, tstep, Planet):
    # Makes a set of times to pass to odeint function, containing 0 and tstep.
    t_set = np.array([0,tstep])
    planet_mass = Planet.mass
    planet_radius = Planet.radius
    # LOOP over objects to advance their positions and velocities
    # Storing NEW OBJECT in new_Rock and re-assigning value to object
    for i in rock_list:
    
        # Saves the attributes necessary for odeint as an array of initial conditions.
        Rock_array = np.array([i.x_pos, i.y_pos, i.x_vel, i.y_vel])
        
        # Returns the most recent array of updated values.
        new_Rock = integ.odeint(derivs, Rock_array, t_set, args = (planet_mass , planet_radius), rtol = 1.0E-6, atol = 1.0E-6)[1]
    
        # Takes the new values and updates the objects attributes.
        i.x_pos = new_Rock[0]
        i.y_pos = new_Rock[1]
        i.x_vel = new_Rock[2]
        i.y_vel = new_Rock[3]
        
    return rock_list

# woot