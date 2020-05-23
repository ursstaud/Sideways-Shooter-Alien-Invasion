import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	"""class representing all aliens"""
	
	def __init__(self, ai_game):
		"""initialize the alien and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen #the screen that the aliens are on is the same as the game screen
		self.screen_rect = ai_game.screen.get_rect()
		#load the alien image 
		self.image = pygame.image.load('ayylmao.bmp')
		self.rect = self.image.get_rect(topright = self.screen_rect.topright)
		self.settings = ai_game.settings
		#store the y value of the alien
		self.y = float(self.rect.y)

	def update(self):
		"""move the alien to up/down"""
		self.y += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.y = self.y

	def check_edges(self):
		"""return true if alien is at the edge of the screen"""
		bottom_screen_limit = 2 * self.rect.height
		screen_rect = self.screen.get_rect()
		if (self.rect.top <= 100) or (self.rect.bottom >= self.screen_rect.bottom):
		#self.rect.bottom >= self.screen_rect.bottom:
			return True
