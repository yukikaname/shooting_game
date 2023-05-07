import pygame

class Player:

	def __init__(self, main_game):
		self.screen = main_game.screen
		self.screen_rect = self.screen.get_rect()
		self.player_width = main_game.settings.player_width
		self.player_height = main_game.settings.player_height
		self.player_color = main_game.settings.player_color
		self.player_speed = main_game.settings.player_speed

		self.rect = pygame.Rect(0, 0, self.player_width, self.player_height)
		self.rect.midbottom = self.screen_rect.midbottom

		self.player_points = [self.rect.bottomleft, self.rect.bottomright, self.rect.midtop]

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		# 移動フラグ
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False


	def update(self):
		"""移動フラグによってキャラの位置を更新"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.player_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.player_speed
		if self.moving_up and self.rect.top > 0:
			self.y -= self.player_speed
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.player_speed

		self.rect.x = self.x
		self.rect.y = self.y
		self.player_points = [self.rect.bottomleft, self.rect.bottomright, self.rect.midtop]


	def draw_player(self):
		"""キャラを現在位置に描画する"""
		pygame.draw.polygon(self.screen, self.player_color, self.player_points, 3)


	def reset_player(self):
		"""キャラを最初の位置に配置する"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.player_points = [self.rect.bottomleft, self.rect.bottomright, self.rect.midtop]
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
