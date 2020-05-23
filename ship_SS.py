import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""a class to manage the ship"""
	def __init__(self, ai_game):
		"""initialize the ship and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()#turns screen into rectangle

		self.image = pygame.image.load('meme.bmp')
		self.rect = self.image.get_rect()
		
		self.rect.midleft = self.screen_rect.midleft 

		self.y = float(self.rect.y)

		#movement flags
		self.moving_top = False
		self.moving_bottom = False

	def update(self):
		"""update the ship's position based on the movement flag"""
		if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom: #checks the position of the ship before changing the value of self.x
			self.y += self.settings.ship_speed
		if self.moving_top and self.rect.top > 100:
			self.y -= self.settings.ship_speed

		self.rect.y = self.y

	def blitme(self):
		"""draw the ship at its current location"""
		self.screen.blit(self.image, self.rect) 

	def center_ship(self):
		"""center the ship on screen"""
		self.rect.midleft = self.screen_rect.midleft
		self.y = float(self.rect.y)