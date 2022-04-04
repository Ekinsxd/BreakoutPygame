import pygame as pg
import random
import math

X_RES = 800
Y_RES = 600

BRICK_WID = 10
BRICK_LEN = 5
PADDLE_WID = 200
PADDLE_HIG = 15
SCORE_WID = 200
SCORE_HIG = 50

BALL_SIZE = 10

# class Text(pg.sprite.Sprite):
#     def __init__(self, text, size, color, width, height):
#         # Call the parent class (Sprite) constructor  
#         pg.sprite.Sprite.__init__(self)
    
#         self.font = pg.font.SysFont("Arial", size)
#         self.textSurf = self.font.render(text, 1, color)
#         self.image = pg.Surface((width, height))
#         W = self.textSurf.get_width()
#         H = self.textSurf.get_height()
#         self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])

# class Score(pg.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pg.Surface((SCORE_WID, SCORE_HIG))
#         self.font = pg.font.Font(pg.font.get_default_font(), 32)
#         self.text = self.font.render('0', False, (5,255,5), (0,0,255))
#         self.rect = self.image.get_rect()
#         self.rect.x = X_RES - SCORE_WID
#         self.rect.y = Y_RES - SCORE_HIG
#         self.rect.center = (X_RES // 2, Y_RES // 2)

#     def update(self):
#         pass

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
        r = random.randint
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, (0, 101, 164), (32, 32), 32)
        self.rect.x = X_RES // 2
        self.rect.y = Y_RES // 2
        self.velocity = [r(-3,3), r(2,4)]
        self.dead = False
        self.boom = pg.mixer.Sound("boom.mp3")
        # self.pew = pg.mixer.Sound('./pew.wav')
        # self.pew.play()

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


class Game:
    def __init__(self):
        pg.init()
        self.__running = False
        self.screen = pg.display.set_mode( (X_RES, Y_RES) )
        self.clock = pg.time.Clock()
        self.bricks = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.paddle = pg.sprite.Group()
        self.score = pg.sprite.Group()
        self.bg = pg.image.load("bg.jpg")
        self.lives = 3


    def run(self):
        myfont = pg.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('Some Text', False, (0, 0, 0))
        while self.__running:
            if (self.isAlive()):
                if self.lives > 0:
                    self.balls.add(Ball())
                    self.lives -= 1
                else:
                    print("Game over!!!")
            events = pg.event.get()
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.balls.add(Ball())
                if event.type == pg.QUIT:
                    self.__running = False
                    pg.quit()
                    exit()
            key = pg.key.get_pressed()
            # if key[pg.K_r]:
            #     self.balls.add(Ball())
            if key[pg.K_LEFT]:
                for paddle in self.paddle:
                    paddle.moveLeft()
            if key[pg.K_RIGHT]:
                for paddle in self.paddle:
                    paddle.moveRight()
            # Take events

            # Update updateable objects
            self.balls.update()
            for ball in self.balls:
                if ball.dead == True:
                    self.balls.remove_internal(ball)
            # Redraw#
            # INSIDE OF THE GAME LOOP
            self.screen.blit(textsurface,(0,0))
            self.screen.blit(self.bg, (0, 0))
            self.bricks.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)
            self.score.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)

    def isAlive(self):
        return len(self.balls) < 1

    def setRunning(self, running):
        self.__running = running

    def addBrick(self, brick):
        self.bricks.add(brick)

    def addBall(self, ball):
        self.balls.add(ball)

    def addScore(self, score):
        self.score.add(score)

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
    # game.addScore(Text("text", 32, (0,255,0), 200, 50))
    Ball.bricks = game.getBricks()
    Ball.paddle = game.getPaddle()
    # Brick.balls = game.getBalls()
    game.setRunning(True)
    game.run()

if __name__ == '__main__':
    main()
