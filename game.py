import pygame
from vector2 import *
from button import *
from image import *
from filemanager import *

class Game:
	def __init__(self):
		self.running = False
		self.fps_cap = 60
		self.delta_time = self.fps_cap
		self.fps = 0
		self.test_height = 1080
		self.multiplier = 1
		self.mouse_down = False
		self.unmanaged_click = False
		self.current_menu = "menu"

		#Debug options
		self.force_screen_size = True

	def play_sound(self, sound):
		pygame.mixer.Sound.play(sound)

	def tuple_to_vector(self, t):
		return Vector2(t[0], t[1])

	def change_menu(self, new_menu):
		self.current_menu = new_menu
		self.get_saves()

	def setup_files(self):
		if not dir_exists("./saves"):
			create_dir("./saves")


	def start(self):
		self.setup_files()
		self.running = True
		print("Game running...")
		pygame.init()

		self.clock = pygame.time.Clock()
		if self.force_screen_size:
			self.screen_height = 1080
			self.screen_width = 1920
		else:
			self.screen_height = int(pygame.display.Info().current_h)
			self.screen_width = int(pygame.display.Info().current_w)
		self.multiplier = self.screen_height / self.test_height
		self.small_font = pygame.font.Font("./fonts/arcade.TTF", int(25 * self.multiplier))
		self.font = pygame.font.Font("./fonts/arcade.TTF", int(45 * self.multiplier))
		self.flags = pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.FULLSCREEN
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), self.flags)

		self.menu_image = Image("./images/menu.png", 1920 * self.multiplier, 1080 * self.multiplier)
		self.click_sound = pygame.mixer.Sound("./sounds/click.wav")

		self.buttons = [
			Button("Start Game", Vector2(172, 128), 675, 75, onclick="start"),
			Button("Settings", Vector2(132, 224), 675, 75),
			Button("Achievements", Vector2(92, 224+96), 675, 75),
			Button("Quit", Vector2(52, 224 + 96+96), 675, 75, onclick="quit")
		]
		self.saves_buttons = [

		]

		while self.running:
			exit_loop = self.manage_events()
			if exit_loop:
				self.running = False
				break
			self.update()
			self.draw()
			self.delta_time = self.clock.tick(self.fps_cap)
			self.fps = int(round(self.clock.get_fps()))

	def update(self):
		self.mouse_pos = self.tuple_to_vector(pygame.mouse.get_pos())
		if self.current_menu == "menu":
			for button in self.buttons:
				if self.box_collides(self.mouse_pos, button.get_position(self.multiplier), Vector2(1, 1), button.get_size(self.multiplier)):
					button.hover(True, self.delta_time)
					if self.unmanaged_click:
						self.unmanaged_click = False
						a = button.click()
						if len(a) > 1:
							self.manage_event(a[0], a[1])
						else:
							self.manage_event(a[0])
				else:
					button.hover(False, self.delta_time)
		elif self.current_menu == "saves":
			for button in self.saves_buttons:
				if self.box_collides(self.mouse_pos, button.get_position(self.multiplier), Vector2(1, 1), button.get_size(self.multiplier)):
					button.hover(True, self.delta_time)
					if self.unmanaged_click:
						self.unmanaged_click = False
						a = button.click()
						if len(a) > 1:
							self.manage_event(a[0], a[1])
						else:
							self.manage_event(a[0])
				else:
					button.hover(False, self.delta_time)

	def draw(self):
		self.screen.fill((25, 25, 25))
		if self.current_menu == "menu":
			self.menu_image.draw(self.screen, Vector2(0, 0))
			for button in self.buttons:
				button.draw(self.screen, self.multiplier, self)
				if button.manage_hover():
					self.play_sound(self.click_sound)
		elif self.current_menu == "saves":
			for button in self.saves_buttons:
				button.draw(self.screen, self.multiplier, self)
				if button.manage_hover():
					self.play_sound(self.click_sound)
		self.draw_text(f"FPS " + str(self.fps), Vector2(), color=(0, 255, 0), text_shadow=True, font=self.small_font)
		pygame.display.flip()

	def get_saves(self):
		self.saves_buttons = []
		s = get_files_in_dir("./saves/")
		y = 150
		for file in s:
			values = parse_save(read_file("./saves/" + file))
			self.saves_buttons.append(Button(values["name"], Vector2(self.screen_width * 0.5, y), self.screen_width * 0.725, self.screen_height * 0.1, center_x=True, onclick="open save", arg=values["name"]))
			y += 150

	def manage_events(self):
		"""Loops through all of PyGame's events and manages them"""
		exit_loop = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_loop = True
				break
			elif event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key) == "q":
					exit_loop = True
					break
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.mouse_down = True
				self.unmanaged_click = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.mouse_down = False
				self.unmanaged_click = False
		return exit_loop

	def draw_text(self, text="", position=Vector2(), color=(0,0,0), text_shadow=True, font=None, vertical_center=None, center=None):
		"""Draws text to the screen based on the provided parameters"""
		if font == None:
			font = self.font

		draw_position = Vector2(position.x, position.y)
		if vertical_center != None:
			h = self.measure_text(text, font).y
			draw_position.y = (position.y + vertical_center.y * 0.5) - h * 0.5
		if center != None:
			w = self.measure_text(text, font).x
			h = self.measure_text(text, font).y
			draw_position = Vector2((position.x + center.x * 0.5) - w * 0.5, (position.y + center.y * 0.5) - h * 0.5)
		if text_shadow:
			text_surface = font.render(text, True, (0,0,0))
			self.screen.blit(text_surface, (draw_position.x + self.multiplier * 4, draw_position.y + self.multiplier * 4))
		text_surface = font.render(text, True, color)
		self.screen.blit(text_surface, draw_position.tuple())

	def manage_event(self, event_name, arg=None):
		"""Manages a provided event, used mainly for button clicks"""
		if event_name == None:
			return
		if event_name == "quit":
			self.running = False
		elif event_name == "start":
			self.change_menu("saves")
		elif event_name == "open save":
			print("Opening save '" + arg + "'")

	def measure_text(self, text, font=None):
		"""Returns the size (in pixels) of the provided text"""
		if font == None:
			font = self.font
		text_width, text_height = self.font.size(text)
		return Vector2(text_width, text_height)

	def collides(self, x, y, r, b, x2, y2, r2, b2):
		return not (r <= x2 or x > r2 or b <= y2 or y > b2);

	# Returns True if 2 boxes collide
	def box_collides(self, pos, pos2, size1, size2):
		return self.collides(pos.x, pos.y,
			pos.x + size1.x, pos.y + size1.y,
			pos2.x, pos2.y,
			pos2.x + size2.x, pos2.y + size2.y);
