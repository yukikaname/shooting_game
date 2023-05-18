import math
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""プレイヤーの弾"""

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



class EnemyBullet(Sprite):
	"""敵の弾"""

	def __init__(self, main_game, enemy):
		super().__init__()
		self.screen = main_game.screen
		self.player = main_game.player

		self.speed = main_game.settings.enemy_bullet_speed
		self.width = main_game.settings.enemy_bullet_width
		self.height = main_game.settings.enemy_bullet_height
		self.color = main_game.settings.enemy_bullet_color

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = enemy.rect.center

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		self.direction_save_flag = True
		self.target_save_flag = True

		self.direction = 0
		self.target = {}


	def update(self):
		"""画面上の弾を移動"""

		if self.direction_save_flag:
			self._direction_save()

		if self.target_save_flag:
			self._target_save()

		if self.target['y_flag']:
			self.y += self.speed * self.direction
		elif self.target['x_flag'] and not self.target['a']:
			self.x += self.speed * self.direction
		elif self.target['x_flag'] and self.target['a']:
			self.x += (1 / math.sqrt(1 + self.target['a'] ** 2)) * self.direction
			self.y = self.target['a'] * self.x + self.target['b']

		self.rect.x = self.x
		self.rect.y = self.y


	def _direction_save(self):
		"""弾の方向を決定する"""
		if self.player.rect.x < self.rect.x:
			self.direction = -1
		elif self.player.rect.x > self.rect.x:
			self.direction = 1
		elif self.player.rect.y > self.rect.y:
			self.direction = 1
		elif self.player.rect.y < self.rect.y:
			self.direction = -1

		# 方向は最初だけ決める
		self.direction_save_flag = False


	def _target_save(self):
		"""弾の軌道を決定する"""
		if self.player.rect.x == self.rect.x:
			self.target = {'x_flag': False, 'y_flag': True, 'a': False, 'b': False}
		elif self.player.rect.y == self.rect.y:
			self.target = {'x_flag': True, 'y_flag': False, 'a': False, 'b': False}
		else:
			a = (self.player.rect.y - self.rect.y) / (self.player.rect.x - self.rect.x)
			b = self.player.rect.y - a * self.player.rect.x
			self.target = {'x_flag': True, 'y_flag': False, 'a': a, 'b': b}

		# 軌道は最初だけ決める
		self.target_save_flag = False


	def draw_bullet(self):
		"""画面上に弾を描画"""
		pygame.draw.ellipse(self.screen, self.color, self.rect, 3)