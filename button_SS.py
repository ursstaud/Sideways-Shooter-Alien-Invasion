import pygame.font

class Button:
	"""class holding all button related things"""

	def __init__(self, ai_game, msg):
		"""initialize button attributes"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#set dimensions and properties
		self.width, self.height = 300, 50
		self.button_color = (231, 84, 128)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 35)

		#build rect and center
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		#prep button message 
		self._prep_msg(msg)


	def _prep_msg(self, msg):
		"""turn the message into a rendered image and center"""
		self.msg_image = self.font.render(msg, True, self.text_color,
			self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center


	def draw_button(self):
		"""draw blank button and draw message"""
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
