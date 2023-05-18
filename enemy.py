import pygame
from pygame.sprite import Sprite
from random import randint

class Enemy(Sprite):

	def __init__(self, main_game):
		super().__init__()
		self.screen = main_game.screen
		self.screen_rect = self.screen.get_rect()
		self.speed = main_game.settings.enemy_speed
		self.width = main_game.settings.enemy_width
		self.height = main_game.settings.enemy_height
		self.color = main_game.settings.enemy_color
		self.hp = main_game.settings.enemy_hp

		self.bullet_count = main_game.settings.bullet_count_limit

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.left = randint(self.width, self.screen_rect.right - self.width * 2 + 1)

		self.y = float(self.rect.y)


	def update(self):
		"""画面上の敵を移動"""
		self.y += self.speed
		self.rect.y = self.y


	def draw_enemy(self):
		"""画面上に敵を描画"""
		pygame.draw.ellipse(self.screen, self.color, self.rect, 3)