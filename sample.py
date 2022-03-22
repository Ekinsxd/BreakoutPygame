import pygame as pg
import random
import math

X_RES = 800
Y_RES = 600

BRICK_WID = 10
BRICK_LEN = 5
PADDLE_WID = 200
PADDLE_HIG = 15

BALL_SIZE = 10


class Paddle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((PADDLE_WID, PADDLE_HIG))
        self.image.fill((0xd, 0xd, 0xd))
        self.rect = self.image.get_rect()
        self.rect.x = X_RES // 2
        self.rect.y = Y_RES * 0.9

    def moveLeft(self):
        if self.rect.x > 1:
            self.rect.x -= 5
    def moveRight(self):
        if self.rect.x + PADDLE_WID < X_RES:
            self.rect.x += 5

class Ball(pg.sprite.Sprite):
    bricks = None
    paddle = None
    def __init__(self):
        super().__init__()
        # r = random.randint
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, (0, 101, 164), (32, 32), 32)
        self.rect.x = X_RES // 2
        self.rect.y = Y_RES // 2
        self.velocity = [3, 3]
        self.dead = False

    def update(self):
        collisions = pg.sprite.spritecollide(self, Ball.bricks, False)
        if collisions:
            # Ball.bricks.boom.play()
            ballx, bally = self.rect.x + BALL_SIZE / 2, self.rect.y + BALL_SIZE / 2
            brickWid = [collisions[0].rect.x, collisions[0].rect.x + X_RES / BRICK_WID]
            brickHig = [collisions[0].rect.y, collisions[0].rect.y + Y_RES / BRICK_LEN / 2]
            print('x')
            print(ballx, brickWid)
            print('y')
            print(bally, brickHig)
            if brickWid[0] < ballx < brickWid[1]:
                # print('within top bottom bounds')
                self.velocity[1] *= -1
            if brickHig[0] < bally < brickHig[1]:
                # print('within left right bounds')
                self.velocity[0] *= -1
            collisions[0].health -= 25
            if collisions[0].health <= 0:
                Ball.bricks.remove_internal(collisions[0])
            pass
        
        collisions = pg.sprite.spritecollide(self, Ball.paddle, False)
        if collisions:
            x = ((self.rect.x - collisions[0].rect.x) / PADDLE_WID * (math.pi / 2)) - (math.pi / 4)
            self.velocity[0] = round(5 * math.sin(x))
            self.velocity[1] = -abs(round(5 * math.cos(x)))
        
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.x < 0:
            self.velocity[0] *= -1
        elif self.rect.x > 800 - BALL_SIZE:
            self.velocity[0] *= -1
        elif self.rect.y < 0:
            self.velocity[1] *= -1
        elif self.rect.y > 600:
            self.dead = True

    def setBricks(self, bricks):
        self.bricks = bricks

    def setPaddle(self, paddle):
        self.paddle = paddle

class Brick(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        r = random.randint
        self.image = pg.Surface((X_RES / BRICK_WID, Y_RES / BRICK_LEN / 2))
        self.colors = [r(0,255), r(0,255), r(0,255)]
        self.health = sum(self.colors)
        self.image.fill((self.colors[0], self.colors[1], self.colors[2]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.boom = pg.mixer.Sound("./boom.mp3")


class Game:
    def __init__(self):
        pg.init()
        self.__running = False
        self.screen = pg.display.set_mode( (X_RES, Y_RES) )
        self.clock = pg.time.Clock()
        self.bricks = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.paddle = pg.sprite.Group()

    def run(self):
        while self.__running:
            if (self.isGamerOver()):
                pg.display.set_caption('Show Text')
                font = pg.font.Font('freesansbold.ttf', 32)
                text = font.render('YOU LOST!', True, (255, 0, 0), (0,0,0))
                textRect = text.get_rect()
                textRect.center = (X_RES // 2, Y_RES // 8 * 7)
                print("Game over!!!")
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.__running = False
                    pg.quit()
                    exit()
            key = pg.key.get_pressed()
            if key[pg.K_LEFT]:
                for paddle in self.paddle:
                    paddle.moveLeft()
            if key[pg.K_RIGHT]:
                for paddle in self.paddle:
                    paddle.moveRight()
            # Take events

            # Update updateable objects
            # self.bricks.update()
            self.balls.update()
            self.paddle.update()
            for ball in self.balls:
                if ball.dead == True:
                    self.balls.remove_internal(ball)
            # Redraw
            self.screen.fill( (255, 255, 255) )
            self.bricks.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)

    def isGamerOver(self):
        return len(self.balls) < 1

    def setRunning(self, running):
        self.__running = running

    def addBrick(self, brick):
        self.bricks.add(brick)

    def addBall(self, ball):
        self.balls.add(ball)

    def addPaddle(self, paddle):
        self.paddle.add(paddle)

    def getBalls(self):
        return self.balls

    def getBricks(self):
        return self.bricks

    def getPaddle(self):
        return self.paddle

def main():
    game = Game()
    for x in range(0, BRICK_WID):
        for y in range(0, BRICK_LEN):
            game.addBrick( Brick(x / BRICK_WID * X_RES, y / BRICK_LEN * Y_RES / 2))

    game.addBall(Ball())
    game.addPaddle(Paddle())
    Ball.bricks = game.getBricks()
    Ball.paddle = game.getPaddle()
    # Brick.balls = game.getBalls()
    game.setRunning(True)
    game.run()

if __name__ == '__main__':
    main()
