import pygame
from Assets import Paddle, Ball
pygame.init()

WIDTH, HEIGHT =  700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

BLACK = (0, 0, 0)

PADDLE_WIDTH ,PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont('comicsans', 50)
WINNING_SCORE = 5
PAUSE_BETWEEN_ROUNDS = 3000

def draw(win, paddles, ball, left_score, right_score): 
	win.fill(BLACK)

	left_score_text = SCORE_FONT.render(f'{left_score}', 1, (255,255,255))
	right_score_text = SCORE_FONT.render(f'{right_score}', 1, (255,255,255))
	win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
	win.blit(right_score_text, ((WIDTH * 3/4) - right_score_text.get_width() // 2, 20))

	for paddle in paddles:
		paddle.draw(win)

	ball.draw(win)

	for i in range(10):
		pygame.draw.rect(win, (255,255,255), (WIDTH//2 - 6 // 2, 10 * (5 * i), 6, 30))



	pygame.display.update()

def handle_paddle_movement(keys, left_paddle, right_paddle):
	if keys[pygame.K_w]:
		left_paddle.move(up=True)
	if keys[pygame.K_s]:
		left_paddle.move(up=False)

	if keys[pygame.K_UP]:
		right_paddle.move(up=True)
	if keys[pygame.K_DOWN]:
		right_paddle.move(up=False)

def handle_collision(ball, left_paddle, right_paddle):
	if ball.x_vel < 0:
		if ball.y >= left_paddle.y and ball.y <=left_paddle.y + left_paddle.height:
			if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
				ball.x_vel *= -1

				middle_y = left_paddle.y + left_paddle.height / 2
				difference_in_y = middle_y - ball.y
				reducution_factor = (left_paddle.height / 2) / ball.MAX_VEL
				ball.y_vel = difference_in_y / reducution_factor * -1

	else:
		if ball.y >= right_paddle.y and ball.y <=right_paddle.y + right_paddle.height:
			if ball.x + ball.radius >= right_paddle.x:
				ball.x_vel *= -1

				middle_y = right_paddle.y + right_paddle.height / 2
				difference_in_y = middle_y - ball.y
				reducution_factor = (right_paddle.height / 2) / ball.MAX_VEL
				ball.y_vel = difference_in_y / reducution_factor * -1

def reset_game(ball, paddles, **data):
	ball.reset()
	for paddle in paddles:
		paddle.reset()

	text = data.get('win_text')
	font = SCORE_FONT.render(text, 1, (255,255,255))
	width = WIDTH * 1/4 - font.get_width() // 2 if text == 'Left Wins!' else	WIDTH * 3/4 - font.get_width() // 2

	WIN.blit(font, (width, HEIGHT//2 - font.get_height() // 2))
	pygame.display.update()
	pygame.time.delay(PAUSE_BETWEEN_ROUNDS)

def main():
	run = True
	clock = pygame.time.Clock()

	left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2,PADDLE_WIDTH ,PADDLE_HEIGHT, WIN)
	right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2,PADDLE_WIDTH ,PADDLE_HEIGHT, WIN)
	ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, WIN)

	left_score = 0
	right_score = 0

	while run: # Game Loop
		clock.tick(FPS)
		draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

		keys = pygame.key.get_pressed()
		handle_paddle_movement(keys, left_paddle, right_paddle)
	
		ball.move()
		handle_collision(ball, left_paddle,right_paddle)

		if ball.x < 0:
			right_score += 1
			ball.reset()
		elif ball.x > WIDTH:
			left_score += 1
			ball.reset()	

		if left_score >= WINNING_SCORE:
			left_score=0
			right_score=0
			reset_game(ball, [left_paddle, right_paddle], win_text='Left Wins!')
		elif right_score >= WINNING_SCORE:
			left_score=0
			right_score=0
			reset_game(ball, [left_paddle, right_paddle], win_text='Right Wins!')

	pygame.quit()


if __name__ == '__main__':
	main()