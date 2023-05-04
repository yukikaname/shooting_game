import sys
import pygame

from settings import Settings
from player import Player
from bullet import Bullet

class ShootingGame:

	def __init__(self):
		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("shooting_game")

		self.player = Player(self)
		self.bullets = pygame.sprite.Group()


	def run_game(self):
		while True:
			self._check_events()
			self.player.update()
			self._update_bullet()
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
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()


	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.player.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.player.moving_left = False


	def _fire_bullet(self):
		"""新しい弾を生成、bulletsグループに追加"""
		new_bullet = Bullet(self)
		self.bullets.add(new_bullet)


	def _update_bullet(self):
		"""弾の位置を更新、古い弾を廃棄"""
		# 弾の位置を更新
		self.bullets.update()

		# 見えなくなった弾を廃棄
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)


	def _update_screen(self):
		"""画面上の画像を更新し、新しい画面に切り替える"""
		self.screen.fill(self.settings.bg_color)
		self.player.draw_player()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		pygame.display.flip()


if __name__ == "__main__":
	"""ゲームのインスタンスを作成し、実行する"""
	sg = ShootingGame()
	sg.run_game()