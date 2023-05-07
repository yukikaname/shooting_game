import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

	def __init__(self, main_game):
		super().__init__()
		self.screen = main_game.screen
		self.speed = main_game.settings.bullet_speed
		self.width = main_game.settings.bullet_width
		self.height = main_game.settings.bullet_height
		self.color = main_game.settings.bullet_color

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.midtop = main_game.player.rect.midtop

		self.y = float(self.rect.y)


	def update(self):
		"""画面上の弾を移動"""
		self.y -= self.speed
		self.rect.y = self.y


	def draw_bullet(self):
		"""画面上に弾を描画"""
		pygame.draw.rect(self.screen, self.color, self.rect)