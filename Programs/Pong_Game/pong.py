import turtle

wn = turtle.Screen()
wn.title('Pong')
wn.bgcolor('black')
wn.setup(width=800, height=600)
wn.tracer(0)

# paddleA
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape('square')
paddle_a.color('white')
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# paddleB
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape('square')
paddle_b.color('white')
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('square')
ball.color('white')
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1
ball.dy = 0.1

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write('Player A:0  Player B:0', align='center', font=('consolas', 24, 'normal'))

# Scores
score_a = 0
score_b = 0


# Function
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


# keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, 'w')
wn.onkeypress(paddle_a_down, 's')
wn.onkeypress(paddle_b_up, 'Up')
wn.onkeypress(paddle_b_down, 'Down')

while True:
    wn.update()

    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -280:
        ball.sety(-280)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        if ball.dx < 2:
            if ball.dx > 0:
                ball.dx += 0.05
            else:
                ball.dx -= 0.05

            if ball.dy > 0:
                ball.dy += 0.05
            else:
                ball.dy -= 0.05

        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write('Player A:{}  Player B:{}'.format(score_a, score_b), align='center', font=('consolas', 24, 'normal'))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        if ball.dx < 2:
            if ball.dx > 0:
                ball.dx += 0.05
            else:
                ball.dx -= 0.05

            if ball.dy > 0:
                ball.dy += 0.05
            else:
                ball.dy -= 0.05

        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write('Player A:{}  Player B:{}'.format(score_a, score_b), align='center', font=('consolas', 24, 'normal'))

    # paddles and ball collisions
    if ball.xcor() > 340 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50 and ball.xcor() < 350:
        ball.dx *= -1

    if ball.xcor() < -340 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50 and ball.xcor() > -350:
        ball.dx *= -1
