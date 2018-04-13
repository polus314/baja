import pygame
from math import pi
import math
import pygame.camera
import sys
from pygame import Rect

pygame.init()
pygame.camera.init()

class Radial_Dial:
	large_font = pygame.font.SysFont('Comic Sans MS', 30)
	small_font = pygame.font.SysFont('Comic Sans MS', 15)

	def __init__(self, min, max, step, cur_value, rect, text, demo_step):
		self.min = min
		self.max = max
		self.step = step
		self.cur_value = cur_value
		self.rectangle = rect
		self.text = text
		self.range = self.max - self.min

		self.demo_step = demo_step	# TODO - remove this later
		
	# Method for drawing the entire radial dial. Draws a semicircle with
	# hash marks showing different values in the legal range. Pointer shows
	# current value in that range
	def draw(self):
		x = self.rectangle.x		# x and y of top-left corner of bounding rectangle
		y = self.rectangle.y
		width = self.rectangle.width	# width of the bounding rectangle
		height = self.rectangle.height	# height of the bounding rectangle
		cx = x + width / 2		# x coordinate of center of circle
		cy = y + height			# y coordinate of center of circle
		screen = pygame.display.get_surface()

		#drawing the baseline, arc and pointer base
		pygame.draw.circle(screen, BLACK, [x + width / 2, cy], 10)

		textsurface = Radial_Dial.large_font.render(self.text, True, (0, 0, 0))
		text_width, text_height = Radial_Dial.large_font.size(self.text)
		screen.blit(textsurface, (cx - text_width / 2, cy - text_height - height / 4))

		#drawing the hash marks, both major and minor
		num_major = int(math.floor(self.range / self.step))
		num_minor = 5
		for i in range(0, num_major):
			angle = pi - (pi * (self.step * i) / self.range)
			cur_x = math.cos(angle) * width / 2
			cur_y = math.sin(angle) * height
			pygame.draw.line(screen, BLACK, [cx + cur_x, cy - cur_y], [cx + (cur_x * 0.9), cy - (cur_y * 0.9)], 5)
			text = str(int(self.step * i + self.min))
			textsurface = Radial_Dial.small_font.render(text, True, (0,0,0))
			text_width, text_height = Radial_Dial.small_font.size(text)
			if i != 0:
				screen.blit(textsurface, (cx + (cur_x * 0.8) - (text_width / 2), cy - (cur_y * 0.8) - text_height / 2 ))
			else:
				screen.blit(textsurface, (cx + (cur_x * 0.8) - (text_width / 2), cy - text_height ))

			for j in range(0, num_minor):
				angle = pi - (pi * (self.step * (i + float(j)/num_minor)) / self.range)
				cur_x = math.cos(angle) * width / 2
				cur_y = math.sin(angle) * height
				pygame.draw.line(screen, BLACK, [cx + cur_x, cy - cur_y], [cx + (cur_x * 0.95), cy - (cur_y * 0.95)], 2)
		
		#draw max hash mark
		pygame.draw.line(screen, BLACK, [cx + width / 2, cy], [cx + (width / 2 * 0.9), cy], 5)
		text = str(int(self.max))
		textsurface = Radial_Dial.small_font.render(text, True, (0,0,0))
		text_width, text_height = Radial_Dial.small_font.size(text)
		screen.blit(textsurface, (cx + (cur_x * 0.8) - (text_width / 2), cy - text_height))

		#drawing the pointer part
		angle = pi - (pi * (self.cur_value - self.min) / self.range) 	# 0 is on the right by convention, but we want 0 on the left
		cur_x = math.cos(angle) * (width / 2)
		cur_y = math.sin(angle) * height				# not divided by 2 since height only refers to top half of circle
		pygame.draw.line(screen, RED, [cx, cy], [cx + cur_x, cy - cur_y], 3)

	def update(new_cur_value):
		self.cur_value = new_cur_value


class Rectangle:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

class Mode:
	DIALS = 1
	CAMERA = 2
	DEBUG = 3

class Bar:
	large_font = pygame.font.SysFont('Comic Sans MS', 30)

	def __init__(self, min, max, rect, cur_value):
		self.min = min
		self.max = max
		self.rect = rect
		self.cur_value = cur_value
		self.range = self.max - self.min

	def draw(self):
		r = self.rect
		screen = pygame.display.get_surface()
		pygame.draw.rect(screen, BLACK, r, 2)

		color = GREEN
		percent = float(self.cur_value - self.min) / float(self.range)
		if percent < 0.25:
			color = RED
		elif percent < 0.50:
			color = YELLOW

		cur_rect = Rect(r.x + 2, r.y + 2, (r.width - 3) * percent, r.height - 3)
		pygame.draw.rect(screen, color, cur_rect, 0)

		text = str(int(self.cur_value)) + "%"
		textsurface = Bar.large_font.render(text, True, (0, 0, 0))
		text_width, text_height = Bar.large_font.size(text)
		screen.blit(textsurface, (r.right - text_width, r.top - text_height))
			
class Timer:
	large_font = pygame.font.SysFont('Comic Sans MS', 30)
	def __init__(self):
		self.time = 0
		
	def update(self):
		self.time += 1

	def draw(self):
		time = self.time
		hours = time / 3600
		minutes = (time / 60) - (hours * 60)
		seconds = time - (hours * 3600 + minutes * 60)

		screen = pygame.display.get_surface()
		#text = str(hours) + ':' + str(minutes) + ':' + str(seconds)
		text = "{:0>2d}:{:0>2d}:{:0>2d}".format(hours, minutes, seconds)
		textsurface = Bar.large_font.render(text, True, (0, 0, 0))
		text_width, text_height = Bar.large_font.size("00:00:00")
		screen.blit(textsurface, (screen_width - text_width, 0))



# Hex color constants
BLACK  = ( 0,   0,    0)
WHITE  = (255, 255, 255)
BLUE   = ( 0,   0,  255)
GREEN  = ( 0, 255,    0)
RED    = (255,   0,   0)
YELLOW = (255, 255,   0)

screen_width = 640
screen_height = 480

# Initialize the dials that will be shown on-screen. So far this includes a
# tachometer, speedometer, and temperature gauge.
def create_dials():
	cur_speed = 0
	cur_rpms = 0
	cur_temp = 125

	tach_x = 5
	tach_y = screen_height - ((screen_width / 2 - 10) / 2) - 10
	tach_w = screen_width / 2 - 10
	tach_h = (screen_width / 2 - 10) / 2

	rect = Rectangle(tach_x, tach_y, tach_w, tach_h)
	tachometer = Radial_Dial(0, 4000, 500, cur_rpms, rect, 'RPM', 30)

	speedo_x = screen_width / 2 + 5
	speedo_y = screen_height - ((screen_width / 2 - 10) / 2) - 10
	speedo_w = screen_width / 2 - 10
	speedo_h = (screen_width / 2 - 10) / 2

	rect = Rectangle(speedo_x, speedo_y, speedo_w, speedo_h)
	speedometer = Radial_Dial(0, 50, 10, cur_speed, rect, 'MPH', 5)

	temp_x = screen_width * 3 / 8
	temp_y = (screen_height - (screen_width / 2 - 10) / 2) - ((screen_width / 4) / 2)
	temp_w = screen_width / 4
	temp_h = (screen_width / 4) / 2

	rect = Rectangle(temp_x, temp_y, temp_w, temp_h)
	temp_gauge = Radial_Dial(100, 300, 50, cur_temp, rect, 'Temp', 10)

	return [tachometer, speedometer, temp_gauge]


# Finds and starts the USB webcam that is connected
def init_webcam():
	#pygame.camera.init()
	cam_list = pygame.camera.list_cameras()
	webcam = pygame.camera.Camera(cam_list[0],(64,48))
	webcam.start()
	return webcam


# DEMO BEHAVIOR
# For each of the dials, advance the current value pointer forward. If the max
# value has been hit, reverse the direction until hitting 0, etc.
def update_dials(dials):
	for dial in dials:
		dial.cur_value += dial.demo_step
		if dial.cur_value > dial.max:
			dial.cur_value = dial.max
			dial.demo_step *= -1
		elif dial.cur_value < dial.min:
			dial.cur_value = dial.min
			dial.demo_step *= -1


fuel_value = 0
timer = Timer()

# Draws the display to the screen. Depending on the mode passed in, different
# things will be shown.
def draw_screen(screen, dials, webcam, mode):
	# Clear the screen and set the screen background
	screen.fill(WHITE)

	if mode == Mode.DIALS:
		for dial in dials:
			dial.draw()
	elif mode == Mode.CAMERA:
		#grab image, scale and blit to screen
		imagen = webcam.get_image()
		imagen = pygame.transform.scale(imagen,(507,380))
		screen.blit(imagen,((screen_width - 507) / 2,100))

	global fuel_value, timer
	fuel = Bar(0, 100, Rect(50,50,200, 40), fuel_value)
	fuel_value = (fuel_value + 0.1) % 100
	fuel.draw()

	timer.draw()
	timer.update()

	pygame.display.flip()



def main():
	size = [screen_width, screen_height]
	screen = pygame.display.set_mode(size)

	paused = False
	done = False
	clock = pygame.time.Clock()

	dials = create_dials()
	webcam = init_webcam()
	mode = Mode.CAMERA

	pygame.display.set_caption("Baja Display")

	while not done:
		clock.tick(30)
     
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done=True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					paused = not paused;
				elif event.key == pygame.K_c:
					mode = Mode.CAMERA
				elif event.key == pygame.K_d:
					mode = Mode.DEBUG
				else:
					mode = Mode.DIALS

		draw_screen(screen, dials, webcam, mode)
		if paused:
			continue

		update_dials(dials)
	
	webcam.stop()
	pygame.quit() 
	sys.exit()

main()














