from random import choice

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem

class Snake(QGraphicsItem):

    def __init__(self, parent):
        super(Snake, self).__init__()
        self.parent = parent.canvas
        self.particleSize = parent.particleSize

        # Random direction at the start
        directions = [[self.particleSize, 0], [-self.particleSize, 0], [0, self.particleSize], [0, -self.particleSize]]
        self.direction = choice(directions)

        # Initial position of the Snake head
        width = range(self.particleSize, int(self.parent.width()) - self.particleSize * 2, self.particleSize)
        height = range(self.particleSize, int(self.parent.height()) - self.particleSize * 2, self.particleSize)
        self.body = [[width[int(len(width) / 2)], height[int(len(height) / 2)]]]

    def ateFood(self, food):
        """
        Compare the snake's head position with the food
        """
        head = self.body[0]

        if food is not None and food.x() == head[0] and food.y() == head[1]:
            self.grow()
            self.parent.removeItem(food)
            return True

        return False

    def grow(self):
        """
        Take the last element of the list, and reinsert it as the last element
        """
        self.body.append(self.body[-1])

    def headInsideOfTail(self):
        """
        Check if the head of the snake has collided with its own body
        """
        return len(self.body) > 2 and self.body[0] in self.body[1:]

    def outOfBounds(self):
        """
        Check if the snake collided with the boundaries
        """
        width = self.parent.width()
        height = self.parent.height()
        head = self.body[0]

        return head[0] > (width - self.particleSize * 2) or \
               head[0] < self.particleSize or \
               head[1] > (height - self.particleSize * 2) or \
               head[1] < self.particleSize

    def changeDirection(self, key):
        """
        Change the Snake's direction according to the key the user has pressed
        """
        if key in [Qt.Key_A, Qt.Key_Left] and self.direction != [self.particleSize, 0]:
            self.direction = [-self.particleSize, 0]
        elif key in [Qt.Key_D, Qt.Key_Right] and self.direction != [-self.particleSize, 0]:
            self.direction = [self.particleSize, 0]
        elif key in [Qt.Key_S, Qt.Key_Down] and self.direction != [0, -self.particleSize]:
            self.direction = [0, self.particleSize]
        elif key in [Qt.Key_W, Qt.Key_Up] and self.direction != [0, self.particleSize]:
            self.direction = [0, -self.particleSize]

    def paint(self, painter, object, widget):
        brush = QBrush(QColor(76, 175, 79), Qt.Dense3Pattern)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)

        for i in range(len(self.body)):
            painter.drawRect(self.body[i][0], self.body[i][1], self.particleSize, self.particleSize)

        # Move Snake
        # Take head and move it around according to the direction
        head = [sum(x) for x in zip(self.body[0], self.direction)]
        # Remove the last element of the list
        self.body.pop()
        # Insert the new head
        self.body.insert(0, head)

    def boundingRect(self):
        return QRectF(0, 0, self.parent.width(), self.parent.height())
