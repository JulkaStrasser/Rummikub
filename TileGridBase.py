import logging
from PyQt5.QtWidgets import QFrame, QGridLayout
from Cell import BoardCell
from PyQt5.QtGui import QColor

class TileGridBaseClass(QFrame):
    def __init__(self, rows, cols, bgColor, fgColor, gridName):
        super(TileGridBaseClass, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.tileGrid = QGridLayout()
        self.tileGrid.setHorizontalSpacing(0)
        self.tileGrid.setVerticalSpacing(0)
        self.rows = rows
        self.cols = cols
        self.cellList = []
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)
        self.frozen = False
        for row in range(self.rows):
            for col in range(self.cols):
                newCell = BoardCell(row, col, bgColor, fgColor, gridName)
                self.tileGrid.addWidget(newCell, row, col)  
                self.cellList.append(newCell)
        self.setLayout(self.tileGrid)

        # tell each cell who it's neighbours are
        for n in range(len(self.cellList)):
            cell = self.cellList[n]
            (row, col) = cell.getPosition()
            if col == 0:
                left = None
                right = self.cellList[n+1]
            elif col == self.cols - 1:
                left = self.cellList[n - 1]
                right = None
                
            else:
                left = self.cellList[n - 1]
                right = self.cellList[n + 1]
            cell.setNeighbours(left, right)

    def isFrozen(self):
        return self.frozen

    def freeze(self):
        self.frozen = True
        for cell in self.cellList:
            cell.freeze()

    def thaw(self):
        self.frozen = False
        for cell in self.cellList:
            cell.thaw()

    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setBackgroundColor(color)

    def setForegroundColor(self, color):
        self.pal.setColor(self.foregroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setForegroundColor(color)

    def removeAllTiles(self):
        logging.debug("Usun wszystkie plytki z planszy")
        for cell in self.cellList:
            cell.removeTile()

    def getGridState(self):
        gridState = []
        for cell in self.cellList:
            tileIndex = cell.getTileMasterIndex()
            gridState.append(tileIndex)
        return gridState

    def restoreGridState(self, grid):
        self.removeAllTiles()
        if len(self.cellList) != len(grid):
            logging.error("Problem z zaladowaniem planszy ")
            return
        for n in range(len(grid)):
            index = grid[n]
            if index is not None:
                tile = self.main.tileCollection.getTileAtIndex(index)
                self.cellList[n].addTile(tile)