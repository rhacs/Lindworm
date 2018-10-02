from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem

class Border(QGraphicsItem):

    def __init__(self, parent):
        super(Border, self).__init__()

        self.canvas = parent.canvas
        self.topBottom = range(0, int(self.canvas.width()), 10)
        self.leftRight = range(0, int(self.canvas.height()), 10)

    def paint(self, painter, object, widget):
        brush = QBrush(QColor(63, 81, 181), Qt.Dense4Pattern)

        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)

        for spot in self.topBottom:
            painter.drawRect(spot, 0, 10, 10)
            painter.drawRect(spot, self.canvas.height() - 10, 10, 10)

        for spot in self.leftRight:
            painter.drawRect(0, spot, 10, 10)
            painter.drawRect(int(self.canvas.width()) - 10, spot, 10, 10)

    def boundingRect(self):
        return QRectF(0, 0, self.canvas.width(), self.canvas.height())
