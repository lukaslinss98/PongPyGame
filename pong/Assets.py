import pygame

class Paddle:
	COLOR = (255,255,255)
	VEL = 4

	def __init__(self, x, y, width, height, win):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.width = width
		self.height = height
		self.h = win.get_height()

	def draw(self, win):
		pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

	def move(self, up=True):
		if up and self.y > 0:
			self.y -= self.VEL
		elif self.y < self.h - self.height:
			self.y += self.VEL

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y

class Ball:
	MAX_VEL = 5
	COLOR = (255,255,255)

	def __init__(self, x, y, radius, win):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.radius = radius
		self.x_vel = self.MAX_VEL
		self.y_vel = 0
		self.w = win.get_width()
		self.h = win.get_height()


	def draw(self, win):
		pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

	def move(self):
		if((self.y - self.radius) <= 0 or (self.y + self.radius) >= self.h):
			self.y_vel *= -1

		self.x += self.x_vel
		self.y += self.y_vel

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y
		self.y_vel = 0
		self.x_vel *= -1
