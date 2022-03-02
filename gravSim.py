# 2D Fast Version 
# Using pygame. First the simulation runs and gets all of the particles' x and y.
# Once that has been calculated, the windoow shows the particles' movement graphically

# TODO: Have all input from the program instead of the console

import time
from src.particle import *
from src.fileFuncs import *
from src.runSim import *
import sys

#######################################################################################################
def main():

	numArguments = len(sys.argv)
	useRandom = False
	save = False
	savePath = ''
	calculate = False
	loadSetup = False
	loadedCalc = False
	setupPath = ''
	positions = []
	particleList = []
	loops = 0

	if numArguments == 1:
		print("\nOptions must be chosen. Use '-h' to know what options are available.")
		sys.exit(0)

	if numArguments > 1:
		options = str(sys.argv[1])
		if options == "-h":
			print("\nUsage: gravSim.py [-c] [-l] [-r] [-s]")
			print("\nTo combine options, use -clrs in any order with any number of options")
			print("\nOptions:\n")
			print("\n\t-a\t\tLoad a file with particle information (not supported)")
			print("\n\t-c\t\tCalculates the particles positioning.")
			print("\n\t-l\t\tLoads from a file containing particle movements")			
			print("\n\t-s\t\tCalculates the particles positioning and saves the calculation to a specified file\n")
			sys.exit(0)


		if '-' in options:
			if 'a' in options:
				loadSetup = True
				print("\nChoose a file to load a setup from:")
				setupPath = input()
				print("\nHow many seconds do you want to simulate:")
				loops = int(input())
			if 'c' in options:
				calculate = True
				print("\nHow many seconds do you want to simulate:")
				loops = int(input())
			if 'l' in options:
				print("\nPlease enter a filename to load calculations:")
				positions = loadPositions(input())
				loadedCalc = True
			if 's' in options:
				print("\nPlease enter a filename to save calculations:")
				savePath = input()
				save = True

		if loadSetup and loadedCalc:
			print("\nERROR: Cannot load a setup and load calculations. Please only choose one option. Use -h for help.")
			sys.exti(0)
		elif loadedCalc and calculate:
			print("\nERROR: Cannot load a calculation and calculate. Please only choose one option. Use -h for help.")
			sys.exit(0)


	if not useRandom and not loadSetup:
		particleList.append((Particle(id=0, mass=10**10, position = [-70, 5, 0], velocityVector=Vector(.05, 1.5708))))
		particleList.append((Particle(id=1, mass=10**10, position = [70, 5, 0], velocityVector=Vector(.05, 4.71239))))
		particleList.append((Particle(id=2, mass=10**10, position = [-950, 5, 0], velocityVector=Vector(.025, 0.0001))))
	elif loadSetup:
		particleList = loadParticles(setupPath)
	else:
		randomParticles()

	if calculate or loadSetup:
		sim = Simulation()
		sim.calculateParticlePos(loops, particleList)
		sim.runSim()
	else:
		sim = Simulation(positions)
		sim.runSim()

	if save:
		saveParticlePos(savePath, sim.numParticles, sim.positions)

#######################################################################################################

main()