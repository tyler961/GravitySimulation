import numpy

class Vector:
	def __init__(self, magnitude, direction):
		self.magnitude = magnitude
		self.direction = direction
		self.xComp = 0
		self.yComp = 0
		self.calcVectorComponents()

	def calcVectorComponents(self):
		self.xComp = self.magnitude * numpy.cos(self.direction)
		self.yComp = self.magnitude * numpy.sin(self.direction)

	def calcVectorMagAndDir(self):
		self.magnitude = numpy.sqrt(self.xComp**2 + self.yComp**2)
		self.direction = numpy.arctan(self.yComp / self.xComp)
		self.updateAngle()

	def updateAngle(self):
		self.direction = numpy.absolute(self.direction)
		if (self.xComp < 0 and self.yComp < 0):
			self.direction += 3.14159
		elif (self.xComp < 0 and self.yComp >= 0):
			self.direction = 3.14159 - self.direction
		elif (self.xComp >= 0 and self.yComp < 0):
			self.direction = 6.28319 - self.direction


class Particle:
	def __init__(self, id, mass = 0, position = [0, 0, 0], velocityVector = Vector(0, 0), accelerationVector = Vector(0, 0)):
		self.mass = mass
		self.position = position
		self.velocityVector = velocityVector
		self.finalForceVector = Vector(0, 0)
		self.accelerationVector = accelerationVector
		self.GRAV_CONST = 6.67408 * 10**-11
		self.ID = id

	# Gets a list of the other particles.
	# Loops through each particle and calculates this particle's vector delta based on the attraction.
	# For now, each particle finds it's own attraction. Later change this so I don't have to recalc the same equations over and over.
	# Ex: p1 and p2 have 33 N of attraction. If this loop is taking place in p1, p1 sets that as it's attraction. 
	# 	  This will have to be recalced again when it's p2's turn to loop. Remove this overlap later.
	def updateParticle(self, particleList, seconds, numDimensions):
		forceVectors = []
		dist = 0
		for i in particleList:
			if(i.ID is not self.ID):
				# Find distance between both particles
				dist = numpy.sqrt((i.position[0] - self.position[0])**2 + (i.position[1] - self.position[1])**2)

				# Find force between the two particles
				force = self.GRAV_CONST * ((self.mass * i.mass) / dist**2)

				# First find x diff and y diff
				xDiff = i.position[0] - self.position[0]
				yDiff = i.position[1] - self.position[1]

				# alpha angle
				# a = y diff
				# b = x diff
				if xDiff == 0 and yDiff >= 0:
					angle = 0
				elif xDiff == 0 and yDiff < 0:
					angle = 3.14159
				else:
					angle = numpy.absolute(numpy.arctan(yDiff / xDiff))
					# Correct the angle
					if (xDiff < 0 and yDiff < 0):
						angle += 3.14159
					elif (xDiff < 0 and yDiff >= 0):
						angle = 3.14159 - angle
					elif (xDiff >= 0 and yDiff < 0):
						angle = 6.28319 - angle

				forceVector = Vector(force, numpy.absolute(angle))
				
				# Need to get a list of all the vectors, then combine them and calcuate the final vector that will be applied.
				forceVectors.append(forceVector)

		tempForceVector = Vector(0, 0)
		# Calculate the final vector
		for i in forceVectors:
			# Find vector's components and add them up for the final vector's components
			i.calcVectorComponents()
			tempForceVector.xComp += i.xComp
			tempForceVector.yComp += i.yComp

		# Now that I have the final vector's components I update the mag and direction of the final vector
		self.finalForceVector = tempForceVector
		self.finalForceVector.calcVectorMagAndDir()

		# Update current particle's acceleration
		self.accelerationVector.magnitude = (self.finalForceVector.magnitude / self.mass) 
		self.accelerationVector.magnitude *= seconds
		self.accelerationVector.direction = self.finalForceVector.direction
		self.accelerationVector.calcVectorComponents()

		# update velocity vector by adding the acceleration vector
		tmpVelocityVector = Vector(0, 0)
		tmpVelocityVector.xComp = self.velocityVector.xComp + self.accelerationVector.xComp
		tmpVelocityVector.yComp = self.velocityVector.yComp + self.accelerationVector.yComp
		tmpVelocityVector.calcVectorMagAndDir()
		self.velocityVector = tmpVelocityVector

	def move(self):
		self.position[0] += numpy.cos(self.velocityVector.direction) * self.velocityVector.magnitude
		self.position[1] += numpy.sin(self.velocityVector.direction) * self.velocityVector.magnitude

	def printParticleStats(self):
		print("\n*******************************************************************************************")
		print("ID: ", self.ID)
		print("Final Force Vector: \n\tMagnitude: ", self.finalForceVector.magnitude, "\n\tDirection: ", self.finalForceVector.direction)
		print("Acceleration Vector: \n\tMagnitude: ", self.accelerationVector.magnitude, "\n\tDirection: ", self.accelerationVector.direction)
		print("Velocity Vector: \n\tMagnitude: ", self.velocityVector.magnitude, "\n\tDirection: ", self.velocityVector.direction)
		print("Position:\n\tX: ", self.position[0], "| Y: ", self.position[1])
		print("Mass:", self.mass, " kg")
		print("*******************************************************************************************\n")


# Needed to create final force vector to calculate what direction the acceleration is pointing
# Force vector to every particle. This is the Force (magnitude of the vector) and the angle ()

# Adding vectors:
# First, find the components of each vector in relation to each other. 
# Vector A:
#		Ax = A(mag) cos(thetaA)
#		Ay = A(mag) sin(thetaA)
# Vector B:
#		Bx = B(mag) cos(thetaB)
#		By = B(mag) sin(thetaB)
#
# Find the magnitude of the resulting vector T
# 		Rx = Ax + Bx
#		Ry = Ay + By
#
# Now that I have the components of the new vector, turn it from components back into vector values
#		R(mag) = sqrt(Rx^2 + Ry^2)
#		R(theta) = arctan(Ry / Rx)
#
# This can be used to add any number of vectors.
# Ex:
#		Rx = Ax + Bx + Cx + Dx + ....
#		Ry = Ay + By + Cy + Dy + ....
# I can then use the equations above to find the new vector's magnitude and angle