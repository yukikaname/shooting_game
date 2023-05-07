class GameStats:
	"""ゲームの統計情報を記録"""
	def __init__(self, main_game):
		self.settings = main_game.settings
		self.reset_stats()


	def reset_stats(self):
		"""ゲーム中に変更される統計情報を初期化する"""
		self.player_limit = self.settings.player_limit