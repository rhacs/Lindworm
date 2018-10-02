from random import choice

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem

class Snake(QGraphicsItem):

    def __init__(self, parent):
        super(Snake, self).__init__()
        self.parent = parent.canvas

        # Random direction at the start (Left or Down)
        directions = [[10, 0], [0, 10]]
        self.direction = choice(directions)

        # Initial position of the Snake head
        self.body = [[20, 20]]

    def grow(self):
        # Take the last element of the list, and reinsert it as
        # the last element
        self.body.append(self.body[-1])

    def changeDirection(self, key):
        if key in [Qt.Key_A, Qt.Key_Left] and self.direction != [10, 0]:
            self.direction = [-10, 0]
        elif key in [Qt.Key_D, Qt.Key_Right] and self.direction != [-10, 0]:
            self.direction = [10, 0]
        elif key in [Qt.Key_S, Qt.Key_Down] and self.direction != [0, -10]:
            self.direction = [0, 10]
        elif key in [Qt.Key_W, Qt.Key_Up] and self.direction != [0, 10]:
            self.direction = [0, -10]

    def paint(self, painter, object, widget):
        brush = QBrush(QColor(76, 175, 79), Qt.Dense3Pattern)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)

        for i in range(len(self.body)):
            painter.drawRect(self.body[i][0], self.body[i][1], 10, 10)

        # Move Snake
        # Take head and move it around according to the direction
        head = [sum(x) for x in zip(self.body[0], self.direction)]
        # Remove the last element of the list
        self.body.pop()
        # Insert the new head
        self.body.insert(0, head)

    def boundingRect(self):
        return QRectF(0, 0, self.parent.width(), self.parent.height())
