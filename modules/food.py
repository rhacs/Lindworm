
from random import randrange

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem

class Food(QGraphicsItem):

    def __init__(self, parent):
        super(Food, self).__init__()

        self.particleSize = parent.particleSize

        # Set the brush style for the Food
        self.brush = QBrush(QColor(244, 66, 54), Qt.Dense2Pattern)

        # Choose a random spot on the available screen
        x = randrange(self.particleSize, parent.canvas.width() - self.particleSize * 2, self.particleSize)
        y = randrange(self.particleSize, parent.canvas.height() - self.particleSize * 2, self.particleSize)

        self.setPos(x, y)

    def changeBrush(self):
        # Color change when the Special item is added to the screen
        self.brush = QBrush(QColor(245, 127, 23), Qt.Dense1Pattern)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        painter.drawRect(0, 0, self.particleSize, self.particleSize)

    def boundingRect(self):
        return QRectF(0, 0, self.particleSize, self.particleSize)
