import pygame
import random

class Ball:
    def __init__(self, radius, x, y, dx, dy, color):
        self.radius = radius
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color

def Overlap(x, y, balls):
    for i in range(len(balls)):
        b = balls[i]
        if x >= b.x and x <= b.x + b.radius * 2 and y >= b.y and y <= b.y + b.radius * 2:
            return True
        elif x + BALL_RADIUS * 2 >= b.x and x + BALL_RADIUS * 2 <= b.x + b.radius * 2 and y >= b.y and y <= b.y + b.radius * 2:
            return True
        elif x + BALL_RADIUS * 2 >= b.x and x + BALL_RADIUS * 2 <= b.x + b.radius * 2 and y + BALL_RADIUS * 2 >= b.y and y + BALL_RADIUS * 2 <= b.y + b.radius * 2:
            return True
        elif x >= b.x and x <= b.x + b.radius * 2 and y + BALL_RADIUS * 2 >= b.y and y + BALL_RADIUS * 2 <= b.y + b.radius * 2:
            return True
    return False

def MoveOrBounce(balls, index, minX, minY, maxX, maxY):
    if balls[index].x <= minX:
        balls[index].dx = 1
    if balls[index].y <= minY:
        balls[index].dy = 1
    if balls[index].x + balls[index].radius * 2 >= maxX:
        balls[index].dx = -1
    if balls[index].y + balls[index].radius * 2 >= maxY:
        balls[index].dy = -1
    balls[index].x += balls[index].dx
    balls[index].y += balls[index].dy
    sumDx = 0
    sumDy = 0
    for i in range(len(balls)):
        if i != index:
            b = balls[i]
            if balls[index].x >= b.x and balls[index].x <= b.x + b.radius * 2 and balls[index].y >= b.y and balls[index].y <= b.y + b.radius * 2:
                balls[index].dx = 1
                balls[index].dy = 1
                sumDx += balls[index].dx
                sumDy += balls[index].dy
            elif balls[index].x + balls[index].radius * 2 >= b.x and balls[index].x + balls[index].radius * 2 <= b.x + b.radius * 2 and balls[index].y >= b.y and balls[index].y <= b.y + b.radius * 2:
                balls[index].dx = -1
                balls[index].dy = 1
                sumDx += balls[index].dx
                sumDy += balls[index].dy
            elif balls[index].x + balls[index].radius * 2 >= b.x and balls[index].x + balls[index].radius * 2 <= b.x + b.radius * 2 and balls[index].y + balls[index].radius * 2 >= b.y and balls[index].y + balls[index].radius * 2 <= b.y + b.radius * 2:
                balls[index].dx = -1
                balls[index].dy = -1
                sumDx += balls[index].dx
                sumDy += balls[index].dy
            elif balls[index].x >= b.x and balls[index].x <= b.x + b.radius * 2 and balls[index].y + balls[index].radius * 2 >= b.y and balls[index].y + balls[index].radius * 2 <= b.y + b.radius * 2:
                balls[index].dx = 1
                balls[index].dy = -1
                sumDx += balls[index].dx
                sumDy += balls[index].dy
    if sumDx != 0:
        sumDx //= abs(sumDx)
    if sumDy != 0:
        sumDy //= abs(sumDy)
    balls[index].x += sumDx
    balls[index].y += sumDy

pygame.init()
pygame.display.set_caption('Bounce')
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
BALL_RADIUS = 20
LIMIT = ((SCREEN_WIDTH * SCREEN_HEIGHT) // ((BALL_RADIUS * 2) ** 2)) // 2

running = True
balls = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            if len(balls) < LIMIT:
                legalXY = []
                for x in range(SCREEN_WIDTH - BALL_RADIUS * 2):
                    for y in range(SCREEN_HEIGHT - BALL_RADIUS * 2):
                        if not Overlap(x, y, balls):
                            legalXY.append((x, y))
                L = len(legalXY)
                if L > 0:
                    index = random.randint(0, L - 1)
                    x = legalXY[index][0]
                    y = legalXY[index][1]
                    dx = 2 * random.randint(0, 1) - 1
                    dy = 2 * random.randint(0, 1) - 1
                    R = random.randint(0, 255)
                    G = random.randint(0, 255)
                    B = random.randint(0, 255)
                    ball = Ball(BALL_RADIUS, x, y, dx, dy, (R, G, B))
                    balls.append(ball)
    screen.fill((0, 255, 255))
    for i in range(len(balls)):
        pygame.draw.circle(screen, balls[i].color, [balls[i].x + balls[i].radius, balls[i].y + balls[i].radius], balls[i].radius)
        MoveOrBounce(balls, i, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.time.delay(10)
    pygame.display.update()