import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QAction, QTableView, QTabWidget, \
    QMessageBox, \
    QComboBox, QStyleFactory, QCheckBox, QFileDialog, QFontComboBox

from PyQt5.QtGui import QFont, QColor

from PyQt5.QtCore import QRect, QPoint

# ++++++++++++++++++++++++++++++++++++++++++++++
#          GLOBALS
# ++++++++++++++++++++++++++++++++++++++++++++++
tileColors = ["red", "black", "blue", "yellow"]
tileOwner = ["player", "board", "bag"]
tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]



class DragLabel(QLabel):
    def __init__(self, color, text, parent):
        super(DragLabel, self).__init__(parent)
        widthText = "13"
        tileFont = QFont("Consolas", 10)
        self.setFont(tileFont)
        metric = QtGui.QFontMetrics(self.font())
        size = metric.size(QtCore.Qt.TextSingleLine, widthText)

        image = QtGui.QImage(size.width() + 12, size.height() + 22,
                             QtGui.QImage.Format_ARGB32_Premultiplied)

        # image = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.qRgba(0, 0, 0, 0))

        # font = QtGui.QFont()
        # font.setStyleStrategy(QtGui.QFont.ForceOutline)

        painter = QtGui.QPainter()
        painter.begin(image)
        if color == "red":
            painter.setBrush(QtCore.Qt.red)
            painter.setPen(QtCore.Qt.red)
        elif color == "blue":
            painter.setBrush(QtCore.Qt.blue)
            painter.setPen(QtCore.Qt.blue)
        elif color == "yellow":
            painter.setBrush(QtCore.Qt.yellow)
            painter.setPen(QtCore.Qt.yellow)
        else:
            painter.setBrush(QtCore.Qt.black)
            painter.setPen(QtCore.Qt.black)


        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # painter.setBrush(QtCore.Qt.white)
        painter.setBrush(QColor('#999999'))
        painter.drawRoundedRect(QtCore.QRectF(0.5, 0.5, image.width() - 1,
                                              image.height() - 4), 30, 30, QtCore.Qt.RelativeSize)

        painter.setFont(tileFont)


        painter.setBrush(QtCore.Qt.blue)

        painter.drawText(QRect(QPoint(6, 6), size), QtCore.Qt.AlignCenter, text)
        painter.end()

        self.setPixmap(QtGui.QPixmap.fromImage(image))
        self.labelText = text




class RummyTile(QWidget):
    def __init__(self, color, value):
        super(RummyTile, self).__init__()
        self.tileLabel = DragLabel(color, str(value), self)

        self.color = color
        self.value = value
        self.owner = "bag"
        self.setObjectName("rummyTile")
        self.cellListIndex = 0
        self.labelText = "hello world"

    def mousePressEvent(self, event):
        # itemData = QtCore.QByteArray()
        # dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        # dataStream << QtCore.QByteArray(self.labelText) << QtCore.QPoint(event.pos() - self.rect().topLeft())
        #
        # mimeData = QtCore.QMimeData()
        # mimeData.setData('application/x-fridgemagnet', itemData)
        # mimeData.setText(self.cellListIndex)
        #
        drag = QtGui.QDrag(self)
        # drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.setPixmap(self.tileLabel.pixmap())

        self.hide()

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

    def __str__(self):
        myStr = ""
        if self.tileBag == []:
            return "bag is empty"
        else:
            return "Here's the tile bag"
            # for tile in self.tileBag:
            #     myStr += tile.getColor() + "  " + str(tile.getValue()) + "\n"
            #  # return '<%s => %s>' % (self.__class__.__name__, self.name)
            # return myStr

