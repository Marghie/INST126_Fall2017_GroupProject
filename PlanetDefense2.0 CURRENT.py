#SAM MOON, EMILY HWANG, Marghie Santos, Zoey Chen
#INST126 - 0201 w/Bill Kules

import os
import random

# Import module to play sounds (SAM)
import winsound

# Import module to add delay (SAM)
import time

# Play background music
winsound.PlaySound("Night_of_Nights_Flowering_nights_remix_", winsound.SND_ASYNC) #(MARGHIE)

# Import the Turtle module
import turtle

# Change window size (SAM)
turtle.setup(650, 650)

# Change window title (SAM)
turtle.title("Planet Defense")

# Required by MacOSX to show the window (SAM)
turtle.fd(0)

# Set the animations speed to the maximum (SAM)
turtle.speed(0)

# Change the background color (SAM)
turtle.bgcolor("black")

# Change background image (SAM)
turtle.bgpic("bg3.gif")

# Hide the default turtle (SAM)
turtle.ht()

# This saves memory (SAM)
turtle.setundobuffer(1)

# This speeds up drawing (SAM)
turtle.tracer(0)

# Register Shapes (SAM)
turtle.register_shape("ship.gif")
turtle.register_shape("meteor.gif")

#Added graphic for ammo (MARGHIE)
turtle.register_shape("pew.gif")

#(SAM)
#Creating a class for sprite
class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    #Defining global move function for all classes that inherit from sprite class
    def move(self):
        self.fd(self.speed)

        # Boundary detection
        if self.xcor() > 330:
            self.setx(330)
            self.rt(60)

        if self.xcor() < -330:
            self.setx(-330)
            self.rt(60)

        if self.ycor() > 330:
            self.sety(330)
            self.rt(60)

        if self.ycor() < -330:
            self.sety(-330)
            self.rt(60)

    #Checking for collisions
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
                (self.xcor() <= (other.xcor() + 20)) and \
                (self.ycor() >= (other.ycor() - 20)) and \
                (self.ycor() <= (other.ycor() + 20)):
                # Add sound when missile and asteroid collide (MARGHIE)
                winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                return True
        else:
            return False

#(SAM)
#Creating class for player
class Player(Sprite): #Creates our first sprite, main character
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None)  # Changes the size of the sprite to help with collision detection (SAM)
        self.speed = 0 #Speed of our player
        self.lives = 3

#Creating left and right movement attributes
    def move_left(self):
        self.setheading(-180)
        self.speed += 10
        if self.speed > 10:
            self.speed -= 10

    def move_right(self):
        self.setheading(360)
        self.speed += 10
        if self.speed > 10:
            self.speed -= 10

    def accelerate(self):
        self.speed += 10

    def decelerate(self):
        self.speed = 0

    def move(self):

        self.fd(self.speed)

        #Border checking for player
        if self.xcor() > 320:
            self.rt(180)

        if self.xcor() < -310:
            self.lt(180)

#(SAM)
#Create class for enemy
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

#(EMILY)
#Creates class for missile
class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty): #Starting attributes of our sprite
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None) #Changes the appearance of the missile
        self.speed = 50 #Speed of missile
        self.status = "ready" #Calls for the missile when it's used, but not visible until it is used
        self.goto(-1000, 1000) #Bullet is moved off screen so it can't be seen
        self.setheading(90) #Makes our missile face upward (change direction)

    #Function for shooting missile
    def fire(self):
        if self.status == "ready": #If the missile is ready, we change the status to shoot
            self.goto(player.xcor(), player.ycor()) #Missile moves to the location of the player
            self.status = "firing"
            # Add sound for when ammo is shot (MARGHIE)
            winsound.PlaySound("laser.wav", winsound.SND_ASYNC)

    #Movement of missile
    def move(self):

        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed) #The missile when called to be "firing" moves forward

        # Border check (Bullet stays within the boundaries of these borders)
        if self.xcor() < -650 or self.xcor() > 650 or \
                        self.ycor() < -300 or self.ycor() > 300:
            self.goto(-1000, 1000)
            self.status = "ready"

#(SAM)
#Creates class for game
class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    #Creating the game window
    def draw_border(self):
        # Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-340, 350)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(690)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

#(EMILY)
#Creating the point system
    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" % self.score
        self.pen.penup()
        self.pen.goto(-480, 300) #Changes the location of the score to outside the border
        self.pen.write(msg, font=("Arial", 16, "normal"))

# (SAM)
# Create game object
game = Game()

# (SAM)
# Draw the game border
game.draw_border()

# (SAM)
# Display Game status
game.show_status()

# (SAM)
# Create my sprites
player = Player("ship.gif", "white", 0, -300)
missile = Missile("pew.gif", "yellow", 0, 0) #(EMILY)

# (EMILY)
enemies =[]
for i in range(15):
    enemies.append(Enemy("meteor.gif", "red", 0, random.randint(200,300)))

# (SAM)
# Keyboard bindings
turtle.onkey(player.move_left, "Left")
turtle.onkey(player.move_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space") #(EMILY)
turtle.listen()

#(SAM)
# Main game loop
while True:
    turtle.update() #(SAM)
    time.sleep(0.05) #(SAM)
    player.move() #(SAM)
    missile.move() #(EMILY)

    for enemy in enemies: #(EMILY)
        enemy.move()

        # Check for a collision with the player (EMILY)
        if player.is_collision(enemy):
            x = random.randint(-250, 250) #Randomizes the location of the enemy as it respawns
            y = random.randint(-250, 250)
            enemy.goto(x, y) #Enemy moves to the randomized x,y coordinates
            game.score -= 100 #Score is deducted by 100 points after a meteor hits a player
            game.show_status() #Updates the score/game

        # Check for a collision between the missile and the enemy (EMILY)
        if missile.is_collision(enemy):
            x = random.randint(-250, 250) #Randomizes the location of the enemy as it respawns
            y = random.randint(-250, 250)
            enemy.goto(x, y) #Enemy moves to the randomized x,y coordinates
            missile.status = "ready"
            # Increase the score
            game.score += 100 #Score earns 100 points as missile hits meteor
            game.show_status() #Updates the score/game

#Prevents the window from closing
delay = raw_input("Press enter to finish. > ")