import pygame as pg
import sys
from src.particle import *


class Simulation():
	def __init__(self, particleLocations = []):
		self.positions = particleLocations
		self.numParticles = 0

		# Pygame information
		self.width = 2000
		self.height = 1000
		self.bgColor = [32, 32, 32]
		self.particleColor = [255, 255, 255]
		self.loadingBgColor = [0, 0, 0]
		self.loadingTextColor = [255, 50, 50]
		self.screen = None
		self.font = None
		self.simComplete = False
		self.paused = False

	def runSim(self):
		pg.init()

		# Pygame information
		self.screen = pg.display.set_mode([self.width, self.height], 0, 0)
		self.font = pg.font.Font('assets/Roboto/Roboto-Regular.ttf', 20)
		pg.display.set_caption("2D Gravity Simulation")
		clock = pg.time.Clock()

		iterations = 0
		# Every list will have the first item be the number of particles. Remove it so the loop can run correctly
		self.numParticles = self.positions.pop(0)

		while not self.simComplete:
			if not self.paused:
				self.screen.fill(self.bgColor)

				for i in range(0, self.numParticles):
					self.screen.set_at((int(self.positions[i + iterations][0] + (self.width/2)), int(self.positions[i + iterations][1] + (self.height/2))), self.particleColor)


				pg.display.update()

				iterations += 1

			for e in pg.event.get():
				if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
					self.simComplete = True
					break
				if e.type == pg.KEYUP and e.key == pg.K_SPACE:
					if self.paused:
						self.paused = False
					else:
						self.paused = True

			iterations += 1

			if (iterations >= (len(self.positions) - self.numParticles)):
				self.simComplete = True

		pg.quit()


	def calculateParticlePos(self, loops, particleList):
		pg.init()

		# Pygame information
		self.screen = pg.display.set_mode([self.width/2, self.height/2])
		self.font = pg.font.Font('assets/Roboto/Roboto-Regular.ttf', 40)
		pg.display.set_caption("2D Gravity Simulation")
		self.screen.fill(self.loadingBgColor)
		positions = []
		self.numParticles = len(particleList)
		self.positions.append(self.numParticles)

		iterations = 0

		while iterations <= loops:
			percent = (iterations/loops) * 100
			percentString = "{:.2f}".format(percent)
			percentString = "Completion: " + percentString + "%"
			text = self.font.render(str(percentString), True, self.loadingTextColor)
			textRect = text.get_rect()
			textRect.center = (self.width/4, self.height/4)
			self.screen.fill(self.loadingBgColor)
			self.screen.blit(text, textRect)
			pg.display.update()

			# Update the particles
			for i in particleList:
				i.updateParticle(particleList, 1, 2)

			for i in particleList:
				self.positions.append([i.position[0], i.position[1]])
				i.move()

			for e in pg.event.get():
				if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
					iterations = loops
					print("Calculation exited. Closing program.")
					sys.exit(0)

			iterations += 1

		pg.quit()
