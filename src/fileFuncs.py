import os
import sys
from src.particle import *
# TODO: Change all file operations to binary files to save on space

# Saves the provided particle positions to a file
def saveParticlePos(path, numParticles, positions):
	f = open(path, 'w')
	finalString = str(numParticles) + "\n"

	for i in positions:
		finalString += str(i[0]) + " " + str(i[1]) + "\n"

	f.write(finalString)
	print("File saved successfully")
	f.close()



# Loads from a text file getting all of the saved number 
# of particles in the sim and the x, y positions of them all
def loadPositions(path):
	f = None

	if os.path.exists(path):
		f = open(path, 'r')
	else:
		print("ERROR: Simulation file does not exist. Exiting program.")
		sys.exit(1)

	positions = []

	numParticles = 0
	foundNumParticles = False
	foundX = False
	x = ''
	y = ''
	numParts = ''

	
	lines = f.readlines()

	for line in lines:
		x = ''
		y = ''
		foundX = False
		for i in line:
			if i == ' ':
				foundX = True
			elif foundX == False and i != '\n':
				if foundNumParticles == False:
					numParts += i
				else:
					x += i
			elif foundX == True and i != '\n':
				y += i

		if foundNumParticles == True:
			positions.append([float(x), float(y)])
		else:
			# This should always be the first value
			positions.append(int(numParts))
			foundNumParticles = True


	return positions


# Loads from a text file getting set particles
def loadParticles(path):
	foundID = False
	foundMass = False
	foundPos = False
	foundVel = False
	foundAccel = False
	ID = 0
	mass = ''
	pos = []
	vel = []
	accl = []
	currentString = ''

	f = None

	# Particles are loaded as id mass position velocityvector accelerationvector
	if os.path.exists(path):
		f = open(path, 'r')
	else:
		print("ERROR: Setup file does not exist. Exiting program.")

	particleList = []

	lines = f.readlines()

	for line in lines:
		for i in range(0, (len(line))):
			# ID
			if not foundID:
				if line[i] == ' ':
					foundID = True
					ID = int(currentString)
					currentString = ''
				else:
					currentString += line[i]
			
			# Mass
			elif not foundMass:
				if line[i] == ' ':
					foundMass = True
					mass = currentString
					currentString = ''
				else:
					currentString += line[i]
			
			# Position
			elif not foundPos:
				if line[i] == ' ':
					foundPos = True
					pos.append(float(currentString))
					currentString = ''
				elif line[i] == ',':
					pos.append(float(currentString))
					currentString = ''
				elif line[i] != ')' and line[i] != '(':
					currentString += line[i]

			# Velocity
			elif not foundVel:
				if line[i] == ' ':
					foundVel = True
					vel.append(float(currentString))
					currentString = ''
				elif line[i] == ',':
					vel.append(float(currentString))
					currentString = ''
				elif line[i] != ')' and line[i] != '(':
					currentString += line[i]

			# Acceleration
			elif not foundAccel:
				if line[i] == line[len(line)-1]:
					foundAccel = True
					accl.append(float(currentString))
					currentString = ''
				elif line[i] == ',':
					accl.append(float(currentString))
					currentString = ''
				elif line[i] != ')' and line[i] != '(':
					currentString += line[i]
		
		# Convert mass into an actual value from something like 10^10
		index = mass.index("^", 0)
		num1 = mass[0:index]
		num2 = mass[index+1:len(mass)]

		totalMass = float(num1)**float(num2)

		# Everything found. Record the particle and reset everything
		particleList.append(Particle(ID, totalMass, pos, Vector(vel[0], vel[1]), Vector(accl[0], accl[1])))

		# Reset values
		foundID = False
		foundMass = False
		foundPos = False
		foundVel = False
		foundAccel = False
		ID = 0
		mass = ''
		pos = []
		vel = []
		accl = []
		currentString = ''

	return particleList
