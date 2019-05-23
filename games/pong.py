import pygame
import sys
from pygame.locals import *

class Board():
	'''
	Game board

	'''
	def __init__(self, width, height):
		'''
		Game board constructor. Prepares game window.

		'''
		self.width = width
		self.height = height
		self.surface = pygame.display.set_mode((width, height), 0, 32)
		pygame.display.set_caption('Simple pong')

	def draw(self, *args):
		'''
		Draws a game window.

		'''
		background = (230, 255, 255)
		self.surface.fill(background)
		for drawable in args:
			drawable.draw_on(self.surface)

		pygame.display.update()

class PongGame():
	'''
	This class connects all parts of program together

	'''
	def __init__(self, width, height):
		'''
		Initializes pygame and game board

		'''
		pygame.init()
		self.board = Board(width, height)
		# clock for controling frames per second
		self.fps_clock = pygame.time.Clock()
		self.player1 = Racket(width=80, height=20, x=width/2, y=360)
		self.player2 = Racket(width=80, height=20, x=width/2 - 40, y=20, color=(0, 0, 0))
		self.ball = Ball(20, 20, width/2, height/2, self.board, self.player1, self.player2)
		self.ai = Ai(self.player2, self.ball)
		self.judge = Judge(self.board, self.ball, self.player2, self.ball)

	def run(self):
	    '''
	    Main loop
	    '''
	    while not self.handle_events():
	        # it works until any event happens
	        self.ball.move()
	        self.board.draw(
	        	self.ball,
	        	self.player1,
	        	self.player2,
	        	self.judge,
	        )

	        x, y = pygame.mouse.get_pos()
	        delta = x - self.player1.rect[0]
	        if(delta) != 0:
	        	position = x if delta > 0 else - x
	        	self.player1.move(position)

	        self.ai.move()
	        self.fps_clock.tick(30)

	def handle_events(self):
	    '''
	    Event handling method. 

	    :return True if pygame send game exit signal
	    '''
	    for event in pygame.event.get():
	        if event.type == pygame.locals.QUIT:
	            pygame.quit()
	            return True

	        if event.type == pygame.locals.MOUSEMOTION:
	            # myszka steruje ruchem pierwszego gracza
	            x, y = event.pos
	            self.player1.move(x)


class Drawable():
	'''
	Base class for drawed objects

	'''
	def __init__(self, width, height, x, y, color=(0, 255, 0)):
		self.width = width
		self.height = height
		self.color = color
		self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
		self.rect = self.surface.get_rect(x=x, y=y)

	def draw_on(self, surface):
		surface.blit(self.surface, self.rect)

class Ball(Drawable):
	'''
	Ball class. It's speed and movement direction is controled by itself. 
	'''
	def __init__(self, width, height, x, y, board, *args, color=(255, 0, 0), x_speed=6, y_speed=6):
		Drawable.__init__(self, width, height, x, y, color)
		pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.start_x = x
		self.start_y = y
		self.board = board
		self.args = args


	def bounce_y(self):
		'''
		Bounce speed vector in Y axis.
		'''
		self.y_speed *= -1

	def bounce_x(self):
		'''
		Bounce speed vector in X axis
		'''
		self.x_speed *= -1

	def reset(self):
		'''
		Set ball's position at start and bounce speed in Y axis.
		'''
		self.rect.x = self.start_x
		self.rect.y = self.start_y

		self.bounce_y()

	def move(self):
		'''
		Move ball by the default speed. Check if there is a collision with boarder or rackets.
		'''
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed

		if self.rect.x < 0 or self.rect.x > (self.board.surface.get_width() - self.width):
			self.bounce_x()

		if self.rect.y < 0 or self.rect.y > (self.board.surface.get_height() - self.width):
			self.bounce_y()

		for racket in self.args:
			if self.rect.colliderect(racket.rect):
				self.bounce_y()

class Racket(Drawable):
    '''
    Rocket moves along X axixs with default speed.
    '''

    def __init__(self, width, height, x, y, color=(0, 255, 0), max_speed=5):
        Drawable.__init__(self, width, height, x, y, color)
        self.max_speed = max_speed
        self.surface.fill(color)

    def move(self, x):
        '''
        Move rocket towards given coordinate.
        '''
        delta = x - self.rect.x
        if abs(delta) > self.max_speed:
            delta = self.max_speed if delta > 0 else -self.max_speed
        self.rect.x += delta

class Ai():
	'''
	Ai moves towards ball's current location.
	'''
	def __init__(self, racket, ball):
	    self.ball = ball
	    self.racket = racket

	def move(self):
	    '''
	    Check direction and move racket.
	    '''
	    if self.ball.rect.centerx > self.racket.rect.centerx:
	        self.racket.rect.x += self.racket.max_speed
	   
	    elif self.ball.rect.centerx < self.racket.rect.centerx:
	        self.racket.rect.x -= self.racket.max_speed

class Judge():
	'''
	Game judge.
	'''

	def __init__(self, board, ball, *args):
	    self.ball = ball
	    self.board = board
	    self.rackets = args
	    self.score = [0, 0]

	    #Font initialization.
	    pygame.font.init()
	    font_path = pygame.font.match_font('arial')
	    self.font = pygame.font.Font(font_path, 64)

	def update_score(self, board_height):
	    '''
	    If there is a need give player a point and reset ball.
	    '''
	    if self.ball.rect.y < 0:
	        self.score[0] += 1
	        self.ball.reset()
	    elif self.ball.rect.y > (board_height - self.ball.width):
	        self.score[1] += 1
	        self.ball.reset()

	def draw_text(self, surface,  text, x, y):
	    '''
	    Draw text at the given position.
	    '''
	    text = self.font.render(text, True, (150, 150, 150))
	    rect = text.get_rect()
	    rect.center = x, y
	    surface.blit(text, rect)

	def draw_on(self, surface):
	    '''
	    Check if there is a point for sombody and draw score table.
	    '''
	    height = self.board.surface.get_height()
	    self.update_score(height)

	    width = self.board.surface.get_width()
	    self.draw_text(surface, "Player: {}".format(self.score[0]), width/2, height * 0.3)
	    self.draw_text(surface, "Computer: {}".format(self.score[1]), width/2, height * 0.7)

#here the game starts

if __name__ == "__main__":
    game = PongGame(800, 400)
    game.run()