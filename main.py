import sys
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from player import Player
from bullet import Bullet, EnemyBullet
from enemy import Enemy

class ShootingGame:

	def __init__(self):
		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("shooting_game")

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.player = Player(self)
		self.bullets = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.enemy_count = 0
		self.enemybullets = pygame.sprite.Group()

		# Playボタンを作成
		self.play_button = Button(self, "Play")


	def run_game(self):
		while True:
			self._check_events()

			if self.stats.game_active:
				self.player.update()
				self._update_bullet()
				self._update_enemy()

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
		self.enemybullets.empty()

		# プレイヤーの無敵時間を解除してからスタート
		self.player.invincible = False

		# マウスカーソルを非表示にする
		pygame.mouse.set_visible(False)


	def _fire_bullet(self):
		"""新しい弾を生成、bulletsグループに追加"""
		new_bullet = Bullet(self)
		self.bullets.add(new_bullet)


	def _update_bullet(self):
		"""弾の位置を更新、古い弾を廃棄"""
		# 弾の位置を更新
		self.bullets.update()
		self.enemybullets.update()

		# 見えなくなった弾を廃棄
		self._bullet_remove()

		# 弾と敵の衝突に対応する
		self._check_bullet_enemy_collisions()

		# プレイヤーと敵の弾の衝突に対応
		if not self.player.invincible and pygame.sprite.spritecollideany(self.player, self.enemybullets):
			self._player_hit()


	def _bullet_remove(self):
		"""見えなくなった弾を廃棄"""
		# プレイヤーの弾の廃棄
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		# 敵の弾の廃棄
		for bullet in self.enemybullets.copy():
			screen_rect = self.screen.get_rect()

			remove_bottom = bullet.rect.top >= screen_rect.bottom
			remove_top = bullet.rect.bottom <= 0
			remove_right = bullet.rect.left >= screen_rect.right
			remove_left = bullet.rect.right <= 0
			if remove_bottom or remove_top or remove_right or remove_left:
				self.enemybullets.remove(bullet)


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
		if self.enemy_count >= self.settings.next_enemy:
			self._create_enemy()
			self.enemy_count = 0

		# 敵の弾を生成
		for enemy in self.enemies:
			if enemy.bullet_count >= self.settings.bullet_count_limit:
				self._fire_enemy_bullet(enemy)
				enemy.bullet_count = 0
			enemy.bullet_count += 1

		# プレイヤーと敵の衝突に対応
		if not self.player.invincible and pygame.sprite.spritecollideany(self.player, self.enemies):
			self._player_hit()

		self.enemy_count += 1


	def _create_enemy(self):
		"""新たな敵を生成し、enemiesグループに追加"""
		new_enemy = Enemy(self)
		self.enemies.add(new_enemy)


	def _fire_enemy_bullet(self, enemy):
		"""新しい敵の弾を生成し、enemy_bulletsグループに追加"""
		new_enemy_bullet = EnemyBullet(self, enemy)
		self.enemybullets.add(new_enemy_bullet)


	def _player_hit(self):
		"""キャラと敵の衝突に対応する"""
		# キャラの残機を減らす
		self.stats.player_limit -= 1

		# 新しくキャラを配置
		self.player.reset_player()

		# 復帰後、無敵時間を発生
		self.player.invincible = True

		if self.stats.player_limit <= 0:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)


	def _update_screen(self):
		"""画面上の画像を更新し、新しい画面に切り替える"""
		self.screen.fill(self.settings.bg_color)

		if self.player.invincible:
			invincible_count_pd = "{:0>2}".format(self.player.invincible_count)
			lower_limit = int(invincible_count_pd[-2]) >= 0
			upper_limit = int(invincible_count_pd[-2]) <= 4
			if lower_limit and upper_limit:
				self.player.draw_player()
		else:
			self.player.draw_player()

		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		for enemy in self.enemies.sprites():
			enemy.draw_enemy()
		for bullet in self.enemybullets.sprites():
			bullet.draw_bullet()

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