class Settings:

	def __init__(self):
		# 画面に関する設定
		self.screen_width = 1200
		self.screen_height = 650
		self.bg_color = (10, 10, 10)

		# 操作キャラの設定
		self.player_speed = 1.5
		self.player_width = 50
		self.player_height = 50
		self.player_color = (255, 255, 255)
		self.player_limit = 3
		self.invincible_time = 650

		# 敵の設定
		self.enemy_speed = 0.3
		self.enemy_width = 50
		self.enemy_height = 50
		self.enemy_color = (255, 255, 255)
		self.enemy_hp = 3
		self.next_enemy = 500

		# 弾の設定
		self.bullet_speed = 1.0
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (255, 255, 255)

		self.enemy_bullet_speed = 0.7
		self.enemy_bullet_width = 5
		self.enemy_bullet_height = 5
		self.enemy_bullet_color = (255, 255, 255)
		self.bullet_count_limit = 650

		# 点数
		self.point_nomal = 10
		self.point_crash = 50
