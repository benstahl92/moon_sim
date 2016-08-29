import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

def mplot(pfile):

	# open and load the data from the pickle file
	f = open(pfile, 'rb')
	data = pkl.load(f)
	f.close()

	# create arrays to be filled with time steps and masses
	time = np.zeros(len(data))
	mass = np.zeros(len(data))
	
	# loop through the data to retrieve metrics
	for i in range(len(data)):
		time[i] = data[i][0]
		mass[i] = data[i][1]
	
	# convert time to months
	time = time*3.805e-7
	
	# plot the mass and collision counts as a function of time steps
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax1.plot(time,mass,'b')
	ax1.set_xlabel('Elapsed Time (months)')
	ax1.set_ylabel('Mass (kg)')
	ax1.set_title('Mass of Largest Rock vs. Time')	
	plt.savefig(pfile[:-4] + 'mass_plot.png') 
	plt.close(fig)
	