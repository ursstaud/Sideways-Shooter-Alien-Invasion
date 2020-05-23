import sys
from time import sleep
import pygame
from settings_SS import Settings
from ship_SS import Ship
from bullet_SS import Bullet
from alien_SS import Alien
from game_stats_SS import GameStats
from button_SS import Button
from scoreboard_SS import Scoreboard 

class AlienInvasion:
	"""Overall class to mamage game assets and behaviors"""

	def __init__(self):
		"""initialize the game and create game resources"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height
		self.settings.screen = self.screen.get_rect()
		pygame.display.set_caption("Alien Invasion")

		self.ship=Ship(self)
		self.bullets = pygame.sprite.Group() 
		self.aliens = pygame.sprite.Group()
		self.stats = GameStats(self)
		self._create_fleet()
		self.play_button = Button(self, "Play Sideways Shooter")
		self.sb = Scoreboard(self)


	def run_game(self):
		"""start the main loop for the game"""
		while True:
			self._check_events() 
			if self.stats.game_active:
				self.ship.update() 
				self._update_bullets() 
				self._update_aliens()
				
			self._update_screen() 


#ship stuff
	def _fire_bullet(self):
		"""create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet) 

	def _update_bullets(self):
		"""update position of bullets and get rid of old bullets"""
		self.bullets.update() 
		#Get rid of bullets that have disappeared
		for bullet in self.bullets.copy():
			if bullet.rect.left >= self.settings.screen.width:
				self.bullets.remove(bullet)

		#check for any bullets that have hit aliens
		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""checking for collisions"""
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score() 
			self.sb.check_high_score()

		if not self.aliens: 
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#increase level
			self.stats.level += 1
			self.sb.prep_level()

	def _ship_hit(self):
		"""respond to the ship being hit by an alien"""
		#remove 1 from ships left
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center ship
			self._create_fleet()
			self.ship.center_ship()

			#pause for a moment
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)


#alien stuff
	def _create_fleet(self):
		"""create a fleet of aliens"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size

		#determine the number of aliens per row
		available_space_y = self.settings.screen.height - (3 * alien_height)
		number_aliens_y = available_space_y // (2 * alien_height)

		#determine the number of alien rows
		ship_width = self.ship.rect.width
		available_space_x = (self.settings.screen.width - (3 * alien_width) - ship_width)
		number_rows = available_space_x // (2 * alien_width)

		#create the full fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_y):
				self._create_alien(alien_number,row_number)

	def _create_alien(self, alien_number, row_number):
		#make a single alien
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.y =  2 * alien_height + 2 * alien_height * alien_number
		alien.rect.y = alien.y
		
		alien.x =  self.settings.screen.width -  (2 * alien.rect.width 
			* row_number) - alien.rect.width
		alien.rect.x = alien.x
		self.aliens.add(alien)

	def _update_aliens(self):
		"""update aliens"""
		self._check_fleet_edges()
		self.aliens.update()

		#look for alien-ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#look for aliens hitting the bottom
		self._check_aliens_bottom()

	def _check_fleet_edges(self):
		"""respond if aliens reach an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""change the direction of the fleet if an edge is hit"""
		for alien in self.aliens.sprites():
			alien.rect.x -= self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _check_aliens_bottom(self):
		"""check if any aliens have reached the left side of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.left <= screen_rect.left:
				self._ship_hit()
				break


#check events stuff
	def _check_events(self): 
		"""respond to keyboard/mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN: 
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP: 
				self._check_keyup_events(event)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""start a new game when the button is clicked"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#reset game statistics
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#empty alien and bullet groups
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#hide cursor
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event): 
		"""respond to keypresses"""
		if event.key == pygame.K_DOWN: 
			self.ship.moving_bottom = True 
		elif event.key == pygame.K_UP:
			self.ship.moving_top = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self,event): 
		"""respond to key releases"""
		if event.key == pygame.K_DOWN: 
			self.ship.moving_bottom = False 
		elif event.key == pygame.K_UP:
			self.ship.moving_top = False


#update screen
	def _update_screen(self): 
		"""update images on screen, flip to new screen"""
		self.screen.fill(self.settings.bg_color)#
		self.ship.blitme() 
		for bullet in self.bullets.sprites():
			bullet.draw_bullet() 
		self.aliens.draw(self.screen)
		self.sb.show_score()
		
		#draw the play button if game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()


if __name__ == '__main__': 
	#make the game instance and run the game
	ai = AlienInvasion()
	ai.run_game()