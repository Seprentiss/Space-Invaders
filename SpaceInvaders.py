
import turtle
import os
import math

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("~/PycharmProjects/SpaceInvaders/giphy.gif")

# Register shapes
wn.register_shape("player.gif")
wn.register_shape("invader.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)

for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()
# Set the number of kills
num_of_kills = 0

# Set the score to 0
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 20

# Choose a number of enemies
number_of_enemies = 10
# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())
    for enemy in enemies:
        enemy.color("red")
        enemy.shape("invader.gif")
        enemy.penup()
        enemy.speed(0)
        x = 0
        if (enemies.index(enemy) % 2) == 0:
            x = (enemies.index(enemy) * -25)
        else:
            x = (enemies.index(enemy) + 1) * 25
        y = 200
        enemy.setposition(x, y)

enemyspeed = 2

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 40

# Create the enemies bullets
e_bullet = turtle.Turtle()
e_bullet.color("white")
e_bullet.shape("triangle")
e_bullet.speed(0)
e_bullet.setheading(-90)
e_bullet.shapesize(.5, .5)
e_bullet.hideturtle()

e_bullet_speed = 40

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"

# Define enemy bullet state
# ready - ready to fire
# fire - bullet is firing

e_bulletstate = "ready"

# Create towers

tower1 = turtle.Turtle()
tower1.color("green")
tower1.shape("square")
tower1.penup()
tower1.speed(0)
tower1.shapesize(1.75, 1.75)
tower1.setposition(-150, -200)

tower2 = turtle.Turtle()
tower2.color("green")
tower2.shape("square")
tower2.penup()
tower2.speed(0)
tower2.shapesize(1.75, 1.75)
tower2.setposition(150, -200)

tower3 = turtle.Turtle()
tower3.color("green")
tower3.shape("square")
tower3.penup()
tower3.speed(0)
tower3.shapesize(1.75, 1.75)
tower3.setposition(0, -200)


# Move the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = - 280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)


'''
def fire_enemy_bullet():
    index = randint(0, 9)
    global e_bulletstate
    if e_bulletstate == "ready":
        os.system("afplay laser.wav&")
        e_bulletstate = "fire"
        x = enemies[index].xcor()
        y = enemies[index].ycor() + 10
        e_bullet.setposition(x, y)
        e_bullet.showturtle()
'''


def fire_bullet():
    # Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        os.system("afplay laser.wav&")
        bulletstate = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# Create keyboard bindings
wn.listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(fire_bullet, "space")

# Main game loop
while True:

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed += .5
            enemyspeed *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)

            # Change enemy direction
            enemyspeed -= .5
            enemyspeed *= -1

        # Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            os.system("afplay explosion.wav&")
            # Reset the bullet
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            enemy.setposition(0, -500)
            enemy.hideturtle()
            # Update the score
            score += 10
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
            # Update number of kills
            num_of_kills += 1

        if isCollision(player, enemy):
            player.hideturtle()
            for e in enemies:
                e.hideturtle()

            print("Game Over")
            break
        if isCollision(bullet, tower1) | isCollision(bullet, tower2) | isCollision(bullet, tower3):
            bulletstate = "ready"
            bullet.setposition(0, -400)

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)
    '''
    if e_bulletstate == "fire":
        y = e_bullet.ycor()
        y -= e_bullet_speed
        e_bullet.sety(y)
    '''

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    if num_of_kills == number_of_enemies:
        print("Congrats you beat this level! ")
        break

    wn.update()
