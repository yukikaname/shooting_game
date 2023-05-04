import pygame

class Player:

	def __init__(self, main_game):
		self.screen = main_game.screen
		self.screen_rect = self.screen.get_rect()
		self.player_width = main_game.settings.player_width
		self.player_height = main_game.settings.player_height
		self.player_color = main_game.settings.player_color
		self.player_speed = main_game.settings.player_speed

		self.player_points = [(0, 0), 
				(self.player_width, 0), 
				(self.player_width / 2, -self.player_height)
				]
		self.player_points = [(point[0] + self.screen_rect.centerx, point[1] + self.screen_rect.bottom) for point in self.player_points]

		# 移動フラグ
		self.moving_right = False
		self.moving_left = False


	def update(self):
		"""移動フラグによってキャラの位置を更新"""
		if self.moving_right and self.player_points[1][0] < self.screen_rect.right:
			self.player_points = [(point[0] + self.player_speed, point[1]) for point in self.player_points]
		if self.moving_left and self.player_points[0][0] > 0:
			self.player_points = [(point[0] - self.player_speed, point[1]) for point in self.player_points]


	def draw_player(self):
		"""キャラを現在位置に描画する"""
		pygame.draw.polygon(self.screen, self.player_color, self.player_points, 3)