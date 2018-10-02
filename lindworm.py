
from os.path import join as pjoin

from PyQt5.QtCore import QAbstractAnimation, QBasicTimer, QByteArray, QEasingCurve, QPointF, QPropertyAnimation, Qt, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QGraphicsScene, QMainWindow
from PyQt5.uic import loadUi

from modules.border import Border
from modules.food import Food
from modules.snake import Snake

class Lindworm(QMainWindow):

    def __init__(self, dir, parent=None):
        super(Lindworm, self).__init__(parent)
        loadUi(pjoin(dir, "res", "lindworm.ui"), self)
        self.setWindowIcon(QIcon(pjoin(dir, "res", "icon.png")))

        # The Graphics Scene, for drawing purposes
        # Let's call it canvas to confuse everyone
        self.canvas = QGraphicsScene(self)
        self.canvas.setSceneRect(0, 0, self.graphicsView.width(), self.graphicsView.height())
        self.graphicsView.setScene(self.canvas)

        # Initialize app variables
        self.snake = None
        self.food = None
        self.playing = False
        self.special = None
        self.timer = QBasicTimer()
        self.elapsedtime = QTime()

        # Speed of the Game, the lower the number, the faster it moves
        self.speed = 100

        # Decorative border, just because
        border = Border(self)
        self.canvas.addItem(border)

        # Center the window on the desktop
        # I like it to be the center of the attention, yeah, an attention whore
        self.centerOnScreen()
        self.show()

    def startGame(self):
        """
            Starts a New Game every time the user press [Enter, Return]
            if a game has not started yet
        """
        self.score.setText("0")
        self.playing = True
        self.elapsedtime.start()

        # Start the timer, its speed controlled by the self.speed var
        self.timer.start(self.speed, Qt.PreciseTimer, self)

        # Check if there is an existing instance of the Snake in the screen
        if self.snake is not None and self.snake in self.canvas.items():
            self.canvas.removeItem(self.snake)

        # Create the new Snake and add it to the screen
        self.snake = Snake(self)
        self.canvas.addItem(self.snake)

        # Add the food
        self.addFood()

    def endGame(self):
        """
            Ends the game, stops its timer, and shows a the score for
            placebo reasons
        """
        self.score.setText("Game Over. You scored <b>%d</b> points" % self.getScore())
        self.playing = False
        self.timer.stop()

        # Reset speed to its original value
        self.speed = 100

        # Remove the piece of food that was left on the screen.
        # Mama always said that i needed to eat all my food
        # (or hide it when she wasn't looking)
        if self.food in self.canvas.items():
            self.canvas.removeItem(self.food)
        if self.special is not None and self.special in self.canvas.items():
            self.canvas.removeItem(self.special)

    def addFood(self, special = False):
        """
            Add a piece of Food in the screen
        """
        food = None

        # Check if the food spawned inside the Snake's body
        # and keep trying until its outside
        while food is None:
            food = Food(self)
            pos = [food.x(), food.y()]

            if pos in self.snake.body:
                food = None

        # Check if the program need to treat it like special or
        # or regular food
        if special:
            self.special = food
            self.special.changeBrush()
        else:
            self.food = food

        # Add it to the canvas (scene)
        self.canvas.addItem(food)

    def getScore(self):
        """
            Get the text inside the Score Label and convert it
            to integer for later operations
        """
        return int(self.score.text())

    def keyPressEvent(self, event):
        """
            Listen to the user's input

            The Qt.Key_Enter is the key in the numpad "Intro"
            And the Qt.Key_Return is the big one we always use

            You can also play with the wasd keys
        """
        snakeStart = [Qt.Key_Enter, Qt.Key_Return]
        snakeMove = [Qt.Key_Left, Qt.Key_A, Qt.Key_Right, Qt.Key_D, \
            Qt.Key_Up, Qt.Key_W, Qt.Key_Down, Qt.Key_S]

        # Start a game if not already playing
        if not self.playing and event.key() in snakeStart:
            self.startGame()
        # Change the Snake's movement direction
        if self.playing and event.key() in snakeMove:
            self.snake.changeDirection(event.key())

    def timerEvent(self, event):
        """
            In charge of, in this case, update the game and check the
            conditions to continue playing, grow, spawn food and special
            item
        """

        # Check if the event is from self.timer
        if event.timerId() == self.timer.timerId():
            self.snake.update()
            width = self.graphicsView.width()
            height = self.graphicsView.height()
            x = self.snake.body[0][0]
            y = self.snake.body[0][1]
            score = self.getScore()

            # Spawn a Special Food every 15 points
            if score % 15 == 0 and score != 0 and self.special is None:
                self.addFood(True)

            # Speed up the speed every 60 seconds
            time = self.elapsedtime.elapsed()
            if time >= 60000:
                # Reset the time
                self.elapsedtime.restart()
                # Increase the speed
                self.speed -= 10

                # Stop the old timer, otherwise it won't be possible to
                # change the game speed. There is nothing like timer.setTime()
                self.timer.stop()
                # Set the new speed
                self.timer.start(self.speed, Qt.PreciseTimer, self)

            # Snake eats the food
            if self.food.x() == x and self.food.y() == y:
                self.snake.grow()
                self.score.setText(str(score + 1))
                self.canvas.removeItem(self.food)
                self.addFood()

            # Snake eats the Special Food
            if self.special is not None:
                if self.special.x() == x and self.special.y() == y:
                    self.snake.grow()
                    self.score.setText(str(score + 5))
                    self.canvas.removeItem(self.special)
                    self.special = None

            # Check for collisions - X axis
            if x > width - 20 or x < 10:
                self.shakeItLikeItsHot(40, 0)
                self.endGame()
            # Check for collisions - Y axis
            elif y > height - 20 or y < 10:
                self.shakeItLikeItsHot(0, 40)
                self.endGame()
            # Check for collisions - itself
            # Had to check for the body length, because it was dying every time
            # the snake ate the first piece of food, couldn't figure out why
            elif self.snake.body[0] in self.snake.body[1:] and len(self.snake.body) > 2:
                self.shakeItLikeItsHot(20, 20)
                self.endGame()

    def closeEvent(self, event):
        """
            Always remove junk when closing the application
        """
        if self.timer.isActive():
            self.timer.stop()

        event.accept()

    def centerOnScreen(self):
        frameGeometry = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())

    def shakeItLikeItsHot(self, xoff, yoff):
        """
            Animate the position of the window when the Snake dies
            (I like them funny names)
        """
        self.animation = QPropertyAnimation(self, QByteArray().append("pos"))
        origin = self.pos()

        # Cannot set only to
        #   self.animation.setStartValue(...)
        #   self.animation.setEndValue(...)
        # Because the initial (setKeyValueAt(0.0, ...)) and end (setKeyValueAt(1.0, ...))
        # position are the same, hence the multiple setKeyValueAt
        self.animation.setKeyValueAt(0.0, QPointF(origin.x(), origin.y()))
        self.animation.setKeyValueAt(0.2, QPointF(origin.x() - xoff, origin.y() + yoff))
        self.animation.setKeyValueAt(0.4, QPointF(origin.x() - xoff, origin.y() - yoff))
        self.animation.setKeyValueAt(0.6, QPointF(origin.x() + xoff, origin.y() - yoff))
        self.animation.setKeyValueAt(0.8, QPointF(origin.x() + xoff, origin.y() + yoff))
        self.animation.setKeyValueAt(1.0, QPointF(origin.x(), origin.y()))

        # Set the animation duration, easing curve (type of animation)
        # and delete the animation when done
        self.animation.setDuration(1000)
        self.animation.setEasingCurve(QEasingCurve.InOutElastic)
        self.animation.start(QAbstractAnimation.DeleteWhenStopped)
