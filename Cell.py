import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog

from PyQt5.QtGui import QFont, QColor

from PyQt5.QtCore import QRect, QPoint

from Tile import RummyTile

class BoardCell(QFrame):
    dragStartCell = 0

    def __init__(self, row, col, bgColor, fgColor):
        super(BoardCell, self).__init__()
        self.setFrameStyle(QFrame.Box)
        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(left, top, right, bottom)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.layout)
        self.setFixedHeight(48)
        self.setFixedWidth(38)
        self.row = row
        self.col = col
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.highlightIsOn = False

    def setDragStartCell(self, cell):
        BoardCell.dragStartCell = cell

    def getDragStartCell(self):
        return BoardCell.dragStartCell

    def enterEvent(self, a0: QtCore.QEvent):
        print("Mouse entered", self.row, self.col)
        self.getCellStatus()
        return

    def addTile(self, newTile):
        print("Cell ", str(self.row), str(self.col), " add tile ", str(newTile.getColor()), " ",
              str(newTile.getValue()))

        newTile.show()
        self.layout.addWidget(newTile)

    def getResidentTileValue(self):
        residentCell = self.findChild(RummyTile)
        if residentCell != None:
            print("Found resident tile at cell ", str(self.row), str(self.col), str(residentCell.getColor()), " ",
                  str(residentCell.getValue()))
            return residentCell
        else:
            print("No resident tile at cell ", str(self.row), str(self.col))
            return

    def removeTile(self):
        print("Remove tile in cell ", str(self.row), str(self.col))
        cellContents = self.findChild(RummyTile)
        if cellContents != None:
            cellContents.setParent(None)

    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)

    def hightlightOn(self):
        self.setBackgroundColor(QColor('#FF9999'))
        self.highlightIsOn = True

    def highlightOff(self):
        self.setBackgroundColor(self.bgColor)
        self.highlightIsOn = False

    def setForegroundColor(self, color):
        self.pal.setColor(self.foregroundRole(), QColor(color))
        self.setPalette(self.pal)

    def getCellStatus(self):
        cellContents = self.findChild(RummyTile)

        if cellContents == None:
            print("Cell Status: cell ", str(self.row), str(self.col), " is empty")
            return "Empty"
        else:
            print("Cell Status:-", str(self.row), str(self.col), " contains ", cellContents.color, cellContents.value)
            return cellContents.color, cellContents.value

    def getPosition(self):
        return self.row, self.col

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-fridgemagnet'):
            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        elif event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if self.getDragStartCell().getPosition() == self.getPosition():
            print("Drag start and end position was the same - toggle highlight")
            if self.highlightIsOn:
                self.highlightOff()
            else:
                self.hightlightOn()
            return
        if self.getDragStartCell().highlightIsOn:
            self.getDragStartCell().highlightOff()
        if event.mimeData().hasFormat('text/plain'):
            mime = event.mimeData()
            sourceTile = RummyTile.dragTile
            residentTile = self.getResidentTileValue()
            self.getDragStartCell().removeTile()
            if residentTile != None:
                # the cell we are dropping onto already contains a tile. So we want to put this tile into
                # the cell where the drag started. Thereby swapping the tiles
                self.removeTile()
                self.getDragStartCell().addTile(residentTile)

            self.addTile(sourceTile)

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
                # elif event.mimeData().hasText():
                # pieces = event.mimeData().text().split()
                # position = event.pos()
                #
                # for piece in pieces:
                #     newLabel = RummyTile.DragLabel(piece, self)
                #     newLabel.move(position)
                #     newLabel.show()
                #
                #     position += QtCore.QPoint(newLabel.width(), 0)
                #
                # event.acceptProposedAction()
        else:
            event.ignore()