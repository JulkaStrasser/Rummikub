import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QRect, QPoint

class DragLabel(QLabel):
    def __init__(self, color, text, parent):
        super(DragLabel, self).__init__(parent)
        widthText = "13"
        tileFont = QFont("DejaVu Sans Mono", 12)
        self.setFont(tileFont)
        metric = QtGui.QFontMetrics(self.font())
        size = metric.size(QtCore.Qt.TextSingleLine, widthText)

        image = QtGui.QImage(28, 39, QtGui.QImage.Format_ARGB32_Premultiplied)

        image.fill(QtGui.qRgba(0, 0, 0, 0))

        painter = QtGui.QPainter()
        painter.begin(image)
        if color == "red":
            painter.setBrush(QColor('#FFF7E6'))
            painter.setPen(QColor('#EA2D00'))
        elif color == "blue":
            painter.setBrush(QColor('#FFF7E6'))
            painter.setPen(QColor('#2E75B6'))
        elif color == "yellow":
            painter.setBrush(QColor('#FFF7E6'))
            painter.setPen(QColor('#FFCC00'))
        else:
            painter.setBrush(QColor('#FFF7E6'))
            painter.setPen(QColor('#262626'))
            

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawRoundedRect(QtCore.QRectF(0.5, 0.5, image.width() - 1,
                                              image.height() - 4), 30, 30, QtCore.Qt.RelativeSize)

        painter.setFont(tileFont)

        painter.drawText(QRect(QPoint(4, 3), size), QtCore.Qt.AlignCenter, text)
        painter.end()

        self.setPixmap(QtGui.QPixmap.fromImage(image))
        self.labelText = text


class RummyTile(QWidget):
    dragTile = None
    def __init__(self, color, value, index):
        super(RummyTile, self).__init__()
        self.tileLabel = DragLabel(color, str(value), self)

        self.color = color
        self.value = value
        self.owner = "none"
        self.setObjectName("rummyTile")
        self.MasterIndex = index
        self.labelText = "hello world"
        self.cellListIndex = 0

        self.setMinimumWidth(28)
        self.setMinimumHeight(38)
        self.frozen = False

    def freeze(self):
        self.frozen = True

    def thaw(self):
        self.frozen = False

    def setDragTile(self, val):
        RummyTile.dragTile = val

    def mouseMoveEvent(self, event):
        if self.frozen:
            return

        print("Mouse press")
        self.setDragTile(self)
        mimeData = QtCore.QMimeData()
        mimeData.setText("hello world")
        self.parent().setDragStartCell(self.parent())
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.setPixmap(self.tileLabel.pixmap())

        if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
            self.close()
        else:
            self.show()
    def getColor(self):
        return self.color

    def getValue(self):
        return self.value

    def setCellListIndex(self, listIndex):
        self.cellListIndex = listIndex

    def getCellListIndex(self, listIndex):
        return self.cellListIndex

    def setOwner(self, owner):
        self.owner = owner

    def getMasterIndex(self):
        return self.MasterIndex

    def __str__(self):
        myStr = ""
        if self.tileBag == []:
            return "bag is empty"
        else:
            return "Here's the tile bag"
           