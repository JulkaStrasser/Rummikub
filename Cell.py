import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog

from PyQt5.QtGui import QFont, QColor

from PyQt5.QtCore import QRect, QPoint

from Tile import RummyTile


def getCellValue(cell):
    value = cell.getResidentTile().getValue()
    return value

class BoardCell(QFrame):
    dragStartCell = 0
    multiDragList = []
    NoOfVacantCellsAvailableForMultiMove = 0
    def __init__(self, row, col, bgColor, fgColor, parent):
        super(BoardCell, self).__init__()
        self.setFrameStyle(QFrame.Box)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.layout)
        self.setFixedHeight(48)
        self.setFixedWidth(38)
        self.row = row
        self.col = col
        self.left = None  #left neighbour
        self.right = None #right neighbour
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.highlightIsOn = False
        self.parentGridName = parent
        self.frozen = False

    def freeze(self):
        self.frozen = True
        tile = self.getResidentTile()
        if tile is not None:
            tile.freeze()

    def thaw(self):
        self.frozen = False
        tile = self.getResidentTile()
        if tile is not None:
            tile.thaw()

    def setNeighbours(self, left, right):
        self.left = left
        self.right = right

    def getCol(self):
        return self.col

    def printMultiDragList(self):
        print("The multi drag list contains the following tiles")
        if len(BoardCell.multiDragList) > 0:
            for cell in BoardCell.multiDragList:
                color = cell.getResidentTile().getColor()
                value = cell.getResidentTile().getValue()
                print(cell.getParentGridName(), " - ", str(color), " ", str(value))
        else:
            print("Empty")



    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.frozen:
            return

        print("cell mouse release event")
        global getCellValue
        if self.getResidentTile():
            #This cell contains a tile so toggle the highlight
            print("cell Mouse press")
            if self.highlightIsOn:
                self.highlightOff()
            else:
                self.highlightOn()
            return
        else:
            #sort by values
            BoardCell.multiDragList.sort(key=getCellValue) 
         
            BoardCell.NoOfVacantCellsAvailableForMultiMove = 0
            if len(BoardCell.multiDragList) > 0:
                self.countEmptyCells()

    def countEmptyCells(self):
        if self.getResidentTile() == None:
            BoardCell.NoOfVacantCellsAvailableForMultiMove += 1
            if BoardCell.NoOfVacantCellsAvailableForMultiMove == len(BoardCell.multiDragList):
                # We've got enough empty cells to do the multi move
                self.handleMultiDrop()
            elif self.right:
                self.right.countEmptyCells()
            else:
                print("Not enough empty cells for move operation")
        else:
            print("Not enough empty cells for move operation")

    def handleMultiDrop(self):
        if self.frozen:
            return

        if BoardCell.multiDragList == []:
            return
        else:
            cell = BoardCell.multiDragList.pop()
            tile = cell.getResidentTile()
            cell.removeTile()
            self.addTile(tile)
            cell.highlightOff()
            if len(BoardCell.multiDragList) > 0 and self.left:
                self.left.handleMultiDrop()

    def setDragStartCell(self, cell):
        BoardCell.dragStartCell = cell

    def getDragStartCell(self):
        return BoardCell.dragStartCell

    def enterEvent(self, a0: QtCore.QEvent):
        # print("Mouse entered", self.row, self.col)
        self.getCellStatus()
        return

    def addTile(self, newTile):
        print("Cell ", str(self.row), str(self.col), " add tile ", str(newTile.getColor()), " ",
              str(newTile.getValue()))
        # newTile.show()
        self.layout.addWidget(newTile)

        newTile.show()
        print("show tile")

    def addTileWithPreShow(self, newTile):
        print("Cell ", str(self.row), str(self.col), " add tile ", str(newTile.getColor()), " ",
              str(newTile.getValue()))
        newTile.show()
        self.layout.addWidget(newTile)

    def getParentGridName(self):
        return self.parentGridName

    def getResidentTile(self):
        residentCell = self.findChild(RummyTile)
        return residentCell

    def removeTile(self):
        print("Remove tile in cell ", str(self.row), str(self.col))
        cellContents = self.findChild(RummyTile)
        if cellContents != None:
            cellContents.setParent(None)

    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)

    def highlightOn(self):
        self.setBackgroundColor(QColor('#FFA64D'))
        self.highlightIsOn = True
        BoardCell.multiDragList.append(self)
        self.printMultiDragList()

    def highlightOff(self):
        self.setBackgroundColor(self.bgColor)
        self.highlightIsOn = False
        if self in BoardCell.multiDragList:
            BoardCell.multiDragList.remove(self)
        self.printMultiDragList()

    def errorHighLightOn(self):
        self.setBackgroundColor(QColor('#FF1A1A'))

    def errorHighLightOff(self):
        self.setBackgroundColor(self.bgColor)
        
    def setForegroundColor(self, color):
        self.pal.setColor(self.foregroundRole(), QColor(color))
        self.setPalette(self.pal)

    def getCellStatus(self):
        cellContents = self.findChild(RummyTile)
        if cellContents == None:
            # print("Cell Status: cell ", str(self.row), str(self.col), " is empty", " grid = ", str(self.parentGridName))
            return "Empty"
        else:
            # print("Cell Status:-", str(self.row), str(self.col), " contains ", cellContents.color, cellContents.value, " grid = ", str(self.parentGridName))
            return cellContents.color, cellContents.value

    def getPosition(self):
        return self.row, self.col

    def getTileMasterIndex(self):
        cellContents = self.findChild(RummyTile)
        if cellContents == None:
            return
        else:
            return cellContents.getMasterIndex()

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

    # dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if self.getDragStartCell().getPosition() == self.getPosition() and self.getDragStartCell().getParentGridName() == self.parentGridName:
            print("Drag start and end position was the same - toggle highlight")
            if self.highlightIsOn:
                self.highlightOff()
            else:
                self.highlightOn()
            return
        if self.getDragStartCell().highlightIsOn:
            self.getDragStartCell().highlightOff()
        if event.mimeData().hasFormat('text/plain'):
            mime = event.mimeData()
            sourceTile = RummyTile.dragTile
            residentTile = self.getResidentTile()
            self.getDragStartCell().removeTile()
            if residentTile != None:
                # the cell we are dropping onto already contains a tile. So we want to put this tile into
                # the cell where the drag started. Thereby swapping the tiles
                self.removeTile()
                self.getDragStartCell().addTile(residentTile)

            self.addTileWithPreShow(sourceTile)

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()