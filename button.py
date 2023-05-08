import pygame.font

class Button:

	def __init__(self, main_game, msg):
		self.screen = main_game.screen
		self.screen_rect = self.screen.get_rect()

		# ボタンの大きさと属性を設定
		self.width, self.height = 200, 50
		self.button_color = (0, 0, 200)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# ボタンのrectオブジェクトを生成し画面の中央に配置する
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		# ボタンのメッセージの準備
		self._prep_msg(msg)


	def _prep_msg(self, msg):
		"""msgを画像に変換しボタンの中央に配置する"""
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center


	def draw_button(self):
		# 空白のボタンを描画し、メッセージを描画する
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)