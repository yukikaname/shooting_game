import pygame.font

class Scoreboard:
	"""得点の情報をレポートする"""

	def __init__(self, main_game):
		self.screen = main_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = main_game.settings
		self.stats = main_game.stats

		# 得点表示用のフォントを設定
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# 得点とハイスコアの初期画像を準備
		self.prep_score()
		self.prep_high_score()


	def prep_score(self):
		"""得点を描画用の画像に変換"""
		score_str = "{:,}".format(self.stats.score)
		self.score_image = self.font.render(score_str, True, 
				self.text_color, self.settings.bg_color)

		# 画面の右上に得点を表示する
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20


	def prep_high_score(self):
		"""ハイスコアを描画用の画像に変換"""
		high_score_str = "{:,}".format(self.stats.high_score)
		self.high_score_image = self.font.render(high_score_str, True, 
				self.text_color, self.settings.bg_color)

		# 得点の下にハイスコアを表示
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.screen_rect.right - 20
		self.high_score_rect.top = self.score_rect.bottom + 10


	def show_score(self):
		"""画面に得点を描画する"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)


	def check_high_score(self):
		"""ハイスコアをチェックし、必要なら表示を更新"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()