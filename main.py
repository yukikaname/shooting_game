import sys
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from player import Player
from bullet import Bullet
from enemy import Enemy

class ShootingGame:

	def __init__(self):
		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("shooting_game")

		self.count = 0

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.player = Player(self)
		self.bullets = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()

		# Playボタンを作成
		self.play_button = Button(self, "Play")


	def run_game(self):
		while True:
			self._check_events()

			if self.stats.game_active:
				self.player.update()
				self._update_bullet()
				self._update_enemy()
				self.count += 1

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
		elif event.key == pygame.K_UP:
			# キャラを上に移動
			self.player.moving_up = True
		elif event.key == pygame.K_DOWN:
			# キャラを下に移動
			self.player.moving_down = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

		if event.key == pygame.K_p and not self.stats.game_active:
			self._start_game()


	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.player.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.player.moving_left = False
		elif event.key == pygame.K_UP:
			self.player.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.player.moving_down = False


	def _start_game(self):
		# ゲームの統計情報をリセットする
		self.stats.reset_stats()
		self.stats.game_active = True
		self.sb.prep_score()

		# 残った弾と敵を廃棄
		self.bullets.empty()
		self.enemies.empty()


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


		self._check_bullet_enemy_collisions()


	def _check_bullet_enemy_collisions(self):
		"""弾と敵の衝突に対応する"""
		for enemy in self.enemies.copy():
			if pygame.sprite.spritecollideany(enemy, self.bullets):
				# 敵の体力が0になったときに衝突した敵と弾を削除する
				collisions = pygame.sprite.spritecollide(
						enemy, self.bullets, True)
				enemy.hp -= 1

				if enemy.hp == 0:
					self.enemies.remove(enemy)
					self.stats.score += self.settings.point_crash
				else:
					self.stats.score += self.settings.point_nomal

				self.sb.prep_score()
				self.sb.check_high_score()


	def _update_enemy(self):
		"""新たな敵を生成し、敵の位置を更新、見えなくなった敵を廃棄"""
		# 敵の位置を更新
		self.enemies.update()

		# 見えなくなった敵を廃棄
		for enemy in self.enemies.copy():
			self.screen_rect = self.screen.get_rect()
			if enemy.rect.top >= self.screen_rect.bottom:
				self.enemies.remove(enemy)

		# 新たな敵を生成
		if self.count == 500:
			self._create_enemy()
			self.count = 0

		if pygame.sprite.spritecollideany(self.player, self.enemies):
			self._player_hit()


	def _create_enemy(self):
		"""新たな敵を生成し、enemiesグループに追加"""
		new_enemy = Enemy(self)
		self.enemies.add(new_enemy)



	def _player_hit(self):
		"""キャラと敵の衝突に対応する"""
		# キャラの残機を減らす
		self.stats.player_limit -= 1

		# 新しくキャラを配置
		self.player.reset_player()

		if self.stats.player_limit <= 0:
			self.stats.game_active = False


	def _update_screen(self):
		"""画面上の画像を更新し、新しい画面に切り替える"""
		self.screen.fill(self.settings.bg_color)
		self.player.draw_player()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		for enemy in self.enemies.sprites():
			enemy.draw_enemy()

		# 得点の情報を描画
		self.sb.show_score()

		# ゲームが非アクティブのときに「Play」ボタンを描画
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()


if __name__ == "__main__":
	"""ゲームのインスタンスを作成し、実行する"""
	sg = ShootingGame()
	sg.run_game()