
from random import randrange

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem

class Food(QGraphicsItem):

    def __init__(self, parent):
        super(Food, self).__init__()

        # Set the brush style for the Food
        self.brush = QBrush(QColor(244, 66, 54), Qt.Dense2Pattern)

        # Choose a random spot on the available screen
        x = randrange(10, parent.canvas.width() - 20, 10)
        y = randrange(10, parent.canvas.height() - 20, 10)

        self.setPos(x, y)

    def changeBrush(self):
        # Color change when the Special item is added to the screen
        self.brush = QBrush(QColor(245, 127, 23), Qt.Dense1Pattern)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        painter.drawRect(0, 0, 10, 10)

    def boundingRect(self):
        return QRectF(0, 0, 10, 10)
