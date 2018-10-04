# Python
from os.path import join as pjoin

# PyQt5
from PyQt5.QtCore import QAbstractAnimation, QBasicTimer, QByteArray, QEasingCurve, QPointF, QPropertyAnimation, Qt, QTime, QRectF
from PyQt5.QtGui import QBrush, QColor, QIcon, QPen
from PyQt5.QtWidgets import QDesktopWidget, QGraphicsScene, QMainWindow
from PyQt5.uic import loadUi

# Lindworm
from modules.food import Food
from modules.snake import Snake

class Lindworm(QMainWindow):

    def __init__(self, dir, parent = None):
        super(Lindworm, self).__init__(parent)
        loadUi(pjoin(dir, "res", "lindworm.ui"), self)
        self.setWindowIcon(QIcon(pjoin(dir, "res", "icon.png")))

        # This is where all the objects are handled (drawn, updated, moved, painted, etc.)
        self.canvas = QGraphicsScene(self)
        # Use all the QGraphicsView area
        self.canvas.setSceneRect(0, 0, self.graphicsView.width(), self.graphicsView.height())
        self.canvas.setBackgroundBrush(QBrush(QColor(52, 56, 56), Qt.SolidPattern))
        self.graphicsView.setScene(self.canvas)

        # Application variables
        self.playing = False            # Is the player playing? (obviously)
        self.timer = QBasicTimer()      # Used for controlling the game speed, and the canvas update
        self.speed = 100                # Refresh rate which the game is updated (in milliseconds,
                                        # the greater it is, the slower is refresh)
        self.particleSize = 10          # Particle's size of the snake, food, border, ... (scale?)
        self.score = 0                  # Keep track of the user's score
        self.playtime = QTime()         # Keep track of the play time, uses later to increase the game speed

        self.snake = None
        self.food = None
        self.special = None

        self.drawBorder()
        self.centerOnScreen()
        self.show()

    # ####### Application Methods

    def startGame(self):
        """
        Starts a New Game every time the user press [Enter, Return]
        if a game has not started yet
        """
        self.playing = True

        # Reset the score
        self.score = 0
        self.scoreLabel.setText(str(self.score))

        # Start counting the time and the timer which controlls the game cycle
        self.speed = 100
        self.playtime.start()
        self.timer.start(self.speed, Qt.PreciseTimer, self)

        # Check if there is a snake drawn on the canvas
        if self.snake is not None and self.snake in self.canvas.items():
            self.canvas.removeItem(self.snake)

        # The same for the food and special food
        if self.food is not None and self.food in self.canvas.items():
            self.canvas.removeItem(self.food)
        if self.special is not None and self.special in self.canvas.items():
            self.canvas.removeItem(self.special)

        # Add the new Snake object to the canvas
        self.snake = Snake(self)
        self.canvas.addItem(self.snake)

        # Call the function to add a piece of Food
        self.addFood()

    def endGame(self):
        """
        Handles the event when the Snake dies
        """
        self.playing = False

        # Show the user the final score
        point = "point" if self.score == 1 else "points"
        self.scoreLabel.setText("Game Over. You scored <b>%d</b> %s" % (self.score, point))

        # Stop the timer
        self.timer.stop()

        # Animate the Window
        self.shakeIt()

    def addFood(self, special=False):
        """
        Add a piece of Food to the canvas
        """
        food = None

        # Check that the food doesn't spawns inside the snake's body
        while food is None:
            food = Food(self)
            position = [food.x(), food.y()]

            # If it's inside the body, try again
            if position in self.snake.body:
                food = None

        if special:
            self.special = food
            self.special.changeBrush()
        else:
            self.food = food

        self.canvas.addItem(food)

    def updateScore(self, points):
        self.score += points
        self.scoreLabel.setText(str(self.score))

    # ####### QMainWindow events

    def closeEvent(self, event):
        """
        Always remove junk when closing an application
        """
        # Stop the Timer if it's active
        if self.timer.isActive():
            self.timer.stop()

        # Continue with the closing event
        event.accept()

    def keyPressEvent(self, event):
        """
        Listen to the user's input
        """
        # Enter is the key located in the keypad, usually denoted by the text "Intro"
        # Return is the big key we usually use to create a break in a sentence
        start = [Qt.Key_Return, Qt.Key_Enter]
        # Game can be played using Arrow keys and WASD
        directions = [Qt.Key_Left, Qt.Key_A, Qt.Key_Right, Qt.Key_D, Qt.Key_Up, Qt.Key_W, Qt.Key_Down, Qt.Key_S]

        # Starts a new game if not already playing
        if not self.playing and event.key() in start:
            self.startGame()

        # Change the Snake's movement direction
        if self.playing and event.key() in directions:
            self.snake.changeDirection(event.key())

    def timerEvent(self, event):
        """
        In charge of, in this case, update the game and check the
        conditions to continue playing, grow, spawn food and special item
        """

        # Check if the event if from the self.timer
        if event.timerId() is self.timer.timerId():
            self.snake.update()

            # Add a piece of Special Food every 15 points
            if self.score % 15 == 0 and self.score != 0 and self.special is None:
                self.addFood(True)

            # Increase the movement speed of the Snake every 60 seconds
            if self.playtime.elapsed() > 60000:
                self.playtime.restart()
                self.speed -= 10

                # Stop and start the timer, there is no method timer.setTime or
                # the like for changing the timer's speed of refresh
                self.timer.stop()
                self.timer.start(self.speed, Qt.PreciseTimer, self)

            # Check if the Snake ate the food
            if self.snake.ateFood(self.food):
                self.updateScore(1)
                self.addFood()
            # Same process for the Special food
            if self.snake.ateFood(self.special):
                self.updateScore(5)
                self.special = None

            # Check if Snake is out of bounds, or its head collided with
            # its body
            if self.snake.outOfBounds() or self.snake.headInsideOfTail():
                self.endGame()
        else:
            super(Lindworm, self).timerEvent(event)

    # ####### "Beautifying" methods (graphics-wise)

    def drawBorder(self):
        """
        Draw a decorative border in the perimeter of the QGraphicsView
        """
        # Remove the outline
        outline = QPen(Qt.NoPen)

        # Change the background color for the object being drawn
        background = QBrush(QColor(0, 95, 107), Qt.Dense3Pattern)

        # [0, 10, 20, 30, ... , self.canvas.width()] with particle size set to 10
        topBottom = range(0, int(self.canvas.width()), self.particleSize)

        # [10, 20, 30, 40, ... , self.canvas,height() - 10] with particle size set to 10
        leftRight = range(self.particleSize, int(self.canvas.height()) - self.particleSize, self.particleSize)

        size = self.particleSize
        width = self.canvas.width()
        height = self.canvas.height()

        # Top, Bottom, Left, Right borders (in that order)
        areas = [
            QRectF(0, 0, width, size),
            QRectF(0, height - size, width, size),
            QRectF(0, size, size, height - size * 2),
            QRectF(width - size, size, size, height - size * 2)
        ]

        for area in areas:
            self.canvas.addRect(area, outline, background)

    def shakeIt(self):
        """
        Animate the Position of the Window when the Snake dies a horrible death due
        to the user's fault.

        In this case, the use of setStartValue and setEndValue cannot be implemented
        due to the fact that the initial and end position of the window are the same,
        hence the multiple calls of setKeyValueAt.
        """

        self.animation = QPropertyAnimation(self, QByteArray().append("pos"))

        # Save the window's original position
        origin = self.pos()

        # Amount of pixels that the window is going to be moved
        offset = 40

        self.animation.setKeyValueAt(0.0, QPointF(origin.x(), origin.y()))
        self.animation.setKeyValueAt(0.3, QPointF(origin.x() - offset, origin.y()))
        self.animation.setKeyValueAt(0.6, QPointF(origin.x() + offset, origin.y()))
        self.animation.setKeyValueAt(1.0, QPointF(origin.x(), origin.y()))

        # Duration of the animation, in milliseconds (1s = 1000ms)
        self.animation.setDuration(1000)

        # QEasingCurve.InOutElastic is a type of animation path
        self.animation.setEasingCurve(QEasingCurve.InOutElastic)

        # Start and Delete the animation when done
        self.animation.start(QAbstractAnimation.DeleteWhenStopped)

    def centerOnScreen(self):
        """
        Centers the window on the screen keeping in mind the available space for
        the window to show
        """
        frameGeometry = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())
