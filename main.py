import sys
import pygame

from settings import Settings
from player import Player

class ShootingGame:

	def __init__(self):
		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("shooting_game")

		self.player = Player(self)


	def run_game(self):
		while True:
			self._check_events()
			self.player.update()
			self._update_screen()


	def _check_events(self):
		"""キーボードとマウスのイベントに対応"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)


	def _check_keydown_events(self, event):
		"""キーを押すイベントに対応"""
		if event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_RIGHT:
			# キャラを右に移動
			self.player.moving_right = True
		elif event.key == pygame.K_LEFT:
			# キャラを左に移動
			self.player.moving_left = True


	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.player.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.player.moving_left = False


	def _update_screen(self):
		"""画面上の画像を更新し、新しい画面に切り替える"""
		self.screen.fill(self.settings.bg_color)
		self.player.draw_player()

		pygame.display.flip()


if __name__ == "__main__":
	"""ゲームのインスタンスを作成し、実行する"""
	sg = ShootingGame()
	sg.run_game()