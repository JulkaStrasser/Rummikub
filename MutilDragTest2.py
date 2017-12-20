import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog

from PyQt5.QtGui import QFont, QColor

from PyQt5.QtCore import QRect, QPoint, pyqtSignal, QObject

from Tile import RummyTile

class multiDrag(QObject):
    multiDragStartSig = pyqtSignal()
    multiDropSig = pyqtSignal()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     TILE
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DragLabel(QLabel):
    def __init__(self, color, text, parent):
        super(DragLabel, self).__init__(parent)
        widthText = "13"
        tileFont = QFont("DejaVu Sans Mono", 12)
        self.setFont(tileFont)
        metric = QtGui.QFontMetrics(self.font())
        size = metric.size(QtCore.Qt.TextSingleLine, widthText)

        # image = QtGui.QImage(size.width() + 12, size.height() + 22,
        #                      QtGui.QImage.Format_ARGB32_Premultiplied)

        image = QtGui.QImage(28, 39, QtGui.QImage.Format_ARGB32_Premultiplied)

        # image = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.qRgba(0, 0, 0, 0))

        # font = QtGui.QFont()
        # font.setStyleStrategy(QtGui.QFont.ForceOutline)

        painter = QtGui.QPainter()
        painter.begin(image)

        painter.setBrush(QtCore.Qt.lightGray)
        painter.setPen(QtCore.Qt.black)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # painter.setBrush(QtCore.Qt.white)
        # painter.setBrush(QColor('#FFFFCC'))
        painter.drawRoundedRect(QtCore.QRectF(0.5, 0.5, image.width() - 1,
                                              image.height() - 4), 3, 3, QtCore.Qt.RelativeSize)

        painter.setFont(tileFont)

        # painter.setPen(QtCore.Qt.blue)

        painter.drawText(QRect(QPoint(4, 3), size), QtCore.Qt.AlignCenter, text)
        painter.end()

        self.setPixmap(QtGui.QPixmap.fromImage(image))
        self.labelText = text


class RummyTile(QWidget):
    dragTile = None
    mdrag = multiDrag()
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
        RummyTile.mdrag.multiDragStartSig.connect(self.handleStartMultiDrag)

    def setDragTile(self, val):
        RummyTile.dragTile = val

    # def getDragTile():
    #     return RummyTile.dragTile



    def handleStartMultiDrag(self):
        if self.parent():
            if self.parent() in self.parent().getMultiDragList():
                print("Start multi drag at ", str(self.parent().getPosition()))

                self.setDragTile(self)
                mimeData = QtCore.QMimeData()
                mimeData.setText("hello world")
                self.parent().setDragStartCell(self.parent())
                # self.setParent(None)
                drag = QtGui.QDrag(self)
                drag.setMimeData(mimeData)
                (row, col) = self.parent().getPosition()
                drag.setHotSpot(QPoint(col, row))
                drag.setPixmap(self.tileLabel.pixmap())
                # self.hide()

                if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction,
                              QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
                    self.close()
                else:
                    self.show()

    def mouseMoveEvent(self, event):
        print("Mouse move")
        RummyTile.mdrag.multiDragStartSig.emit()
        self.setDragTile(self)
        mimeData = QtCore.QMimeData()
        mimeData.setText("hello world")
        self.parent().setDragStartCell(self.parent())
        # self.setParent(None)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
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

    def setOwner(self, owner):
        self.owner = owner

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


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     CELL
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoardCell(QFrame):
    dragStartCell = 0
    multiDragList = []
    mdrop = multiDrag()
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
        self.pal.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.pal.setColor(self.foregroundRole(), QtCore.Qt.black)  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.highlightIsOn = False

        BoardCell.mdrop.multiDropSig.connect(self.handleMultiDrop)

    def getMultiDragList(self):
        return BoardCell.multiDragList

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        print("cell Mouse press")
        if self.highlightIsOn:
            self.highlightOff()
            BoardCell.multiDragList.remove(self)
            print("Remove from multi drag list ", str(self.getPosition()))
        else:
            self.hightlightOn()
            BoardCell.multiDragList.append(self)
            print("Add to multi drag list ", str(self.getPosition()))
        return
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
            # print("Cell Status: cell ", str(self.row), str(self.col), " is empty")
            return "Empty"
        else:
            # print("Cell Status:-", str(self.row), str(self.col), " contains ", cellContents.color, cellContents.value)
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

    def handleMultiDrop(self):
        if self in BoardCell.multiDragList:
            print("Cell ", str(self.getPosition()), "received multi drop signal")

    def dropEvent(self, event):
        BoardCell.mdrop.multiDropSig.emit()
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
        else:
            event.ignore()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     BOARD
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++
#          CONTROL PANEL
# ++++++++++++++++++++++++++++++++++++++++++++++
class ControlPanel(QFrame):
    def __init__(self):

        super(ControlPanel, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop))
        self.setLayout(self.layout)
        self.setMinimumHeight(50)
        self.setMinimumWidth(200)
        self.buttonBar = QVBoxLayout()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create buttons
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.addTileButton = QPushButton("Take Tile")
        self.addTileButton.clicked.connect(self.takeTile)

        self.ExitButton = QPushButton("Exit")
        self.ExitButton.clicked.connect(self.Exit)

        self.ListBoardButton = QPushButton("List Board")
        self.ListBoardButton.clicked.connect(self.listBoard)

        self.MasterListButton = QPushButton("Master Tile List")
        self.MasterListButton.clicked.connect(self.masterTileList)

        self.buttonBar.addWidget(self.addTileButton)

        self.buttonBar.addWidget(self.ExitButton)
        # self.buttonBar.addWidget(self.ListBoardButton)
        # self.buttonBar.addWidget(self.MasterListButton)

        self.layout.addLayout(self.buttonBar)
        self.infoBar = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create info box
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.tilesLeftInfoBox = QPlainTextEdit()
        tileLeftFont = QFont("Consolas", 10)
        self.tilesLeftInfoBox.setFont(tileLeftFont)
        self.tilesLeftInfoBox.setPlainText("All tiles in bag")
        self.infoBar.addWidget(self.tilesLeftInfoBox)
        self.layout.addLayout(self.infoBar)

    def masterTileList(self):
        tileCollection.printTileList()

    def listBoard(self):
        self.tilesLeftInfoBox.clear()
        for cell in gameBoard.cellList:
            index = cell.getCellListIndex()
            cellStr = str(index) + " - " + str(cell.getCellStatus())
            self.tilesLeftInfoBox.appendPlainText(cellStr)

    def takeTile(self):
        print("Taking a tile")
        if tileBag.getNoOfTilesInBag() > 0:
            nextTile = tileBag.getTileFromBag()
            gameBoard.AddTileFromBag(nextTile)


    def Exit(self):
        print("Exiting....")
        sys.exit()

    def setNumberOfTiles(self, NoOfTiles):
        tempStr = str(NoOfTiles) + " tiles left in bag"
        self.tilesLeftInfoBox.setPlainText(tempStr)

    def ChangeBackgroundColor(self):
        color = QColorDialog.getColor(QColor('#888844'))
        gameBoard.setBackgroundColor(color)

    def ChangeForegroundColor(self):
        color = QColorDialog.getColor()
        gameBoard.setForegroundColor(color)

    def clearInfoBox(self):
        self.tilesLeftInfoBox.clear()

    def appendInfo(self, tempStr):
        self.tilesLeftInfoBox.appendPlainText(tempStr)

# ++++++++++++++++++++++++++++++++++++++++++++++
#          BOARD
# ++++++++++++++++++++++++++++++++++++++++++++++
class TileGridBaseClass(QFrame):
    def __init__(self, rows, cols, bgColor, fgColor):
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
        for row in range(self.rows):
            for col in range(self.cols):
                newCell = BoardCell(row, col, bgColor, fgColor)
                # newCell.setCellListIndex(len(self.cellList))
                self.tileGrid.addWidget(newCell, row, col)  # i=row j=col
                self.cellList.append(newCell)
        self.setLayout(self.tileGrid)

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
        print("Remove all tiles from the board")
        for cell in self.cellList:
            cell.removeTile()





class GameBoard(TileGridBaseClass):
    def __init__(self, bgColor, fgColor):
        super(GameBoard, self).__init__(5, 5, bgColor, fgColor)
        self.listItems()

    def listItems(self):
        print("List grid contents")
        cellsList = self.findChildren(BoardCell)
        for cell in cellsList:
            print(cell.row, cell.col)

    def AddTileFromBag(self, tile):
        print("AddTileFromBag")
        # take a tile from the bag and put it in the
        # next empty cell
        # go through the cell list calling getStatus(). The first
        # cell that returns empty is the one to add the tile to
        for cell in self.cellList:
            status = cell.getCellStatus()
            if status == "Empty":
                # cellIndex = cell.getCellListIndex()
                # tile.setCellListIndex(cellIndex)
                cell.addTile(tile)
                break

    def GetNextEmptyCellPosition(self):
        print("GetNextEmptyCellPosition")

    def removeTile(self, index):
        self.cellList[index].removeTile()

class PlayerGrid(TileGridBaseClass):
    def __init__(self, bgColor, fgColor):
        super(PlayerGrid, self).__init__(2, 28, bgColor, fgColor)
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def newDeal(self):
        global tileBag, player1Controls
        for n in range(14):
            if tileBag.getNoOfTilesInBag() > 0:
                nextTile = tileBag.getTileFromBag()
                print(player1Controls.getPlayerName(), " takes a tile. It's ", str(nextTile.getColor()), str(nextTile.getValue()))
                for cell in self.cellList:
                    status = cell.getCellStatus()
                    if status == "Empty":
                        cell.addTile(nextTile)
                        break
            else:
                print("Whoops - tile bag is empty")
                break


class TileBag():
    def __init__(self):
        self.tileBag = []
        self.nextTileToDeal = 0
        tile = tileCollection.getTile()

        while tile != []:
            tile.owner = "bag"
            self.tileBag.append(tile)
            tile = tileCollection.getTile()

        random.shuffle(self.tileBag)
        print("finished filling tile bag")

    def getTileFromBag(self):

        if self.tileBag == []:
            return "empty"
        else:
            tile = self.tileBag.pop()
            tile.owner = "board"
            # controlPanel.setNumberOfTiles(len(self.tileBag) - 1)
            return tile

    def getNoOfTilesInBag(self):
        return len(self.tileBag) - 1

    def newGame(self):
        self.tileBag = []
        self.nextTileToDeal = 0
        tile = tileCollection.getTile()

        while tile != []:
            tile.owner = "bag"
            self.tileBag.append(tile)
            tile = tileCollection.getTile()

        random.shuffle(self.tileBag)
        print("finished filling tile bag")
        print("Shake the tile bag")
        random.shuffle(self.tileBag)

class TileCollection():
    def __init__(self):
        self.tiles = []
        index = 0

        for tileVal in range(10):
            self.tiles.append(RummyTile("black", tileVal, index))
            index += 1

    def getTile(self):
        if self.tiles == []:
            return []
        else:
            for tile in self.tiles:
                if tile.owner == "none":
                    return tile
                    break

            return []

    def getTileAtIndex(self, index):
        if index >= len(self.tiles):
            print("ERROR: getTileAtIndex was asked for the tile at index ", str(index), " which is out of range")
            return
        else:
            return self.tiles[index]

    def printTileList(self):
        # controlPanel.clearInfoBox()
        for tile in self.tiles:
            fred1 = str(tile.MasterIndex)
            fred2 = str(tile.color)
            fred3 = str(tile.value)
            fred4 = str(tile.owner)
            cellStr = fred1 + " - " + fred2 + " " + fred3 + " owner = " + fred4
            # controlPanel.appendInfo(cellStr)

    def clearTiles(self):
        for tile in self.tiles:
            tile.owner = "none"

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()


        self.controlPanel = ControlPanel()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Add everything to the grid layout
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.gameLayout = QGridLayout()

        self.gameLayout.addWidget(gameBoard, 1, 0, 3, 1)

        self.gameLayout.addWidget(self.controlPanel, 1, 1, 3 ,1)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.gameLayout)

        self.setCentralWidget(self.mainWidget)

        # self.setGeometry(200, 200, 850, 500)

class FontSelector(QWidget):
    def __init__(self):
        super(FontSelector, self).__init__()
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout = QHBoxLayout(self.frame)

        self.textBold = QPushButton(self.frame)
        self.textBold.setMaximumSize(QtCore.QSize(25, 25))
        self.textBold.setCheckable(True)
        self.textBold.setText("B")
        self.horizontalLayout.addWidget(self.textBold)

        self.textItalic = QPushButton(self.frame)
        self.textItalic.setMaximumSize(QtCore.QSize(25, 25))
        self.textItalic.setCheckable(True)
        self.textItalic.setText("I")
        self.horizontalLayout.addWidget(self.textItalic)

        self.textUnderline = QPushButton(self.frame)
        self.textUnderline.setMaximumSize(QtCore.QSize(25, 25))
        self.textUnderline.setCheckable(True)
        self.textUnderline.setText("U")
        self.horizontalLayout.addWidget(self.textUnderline)

        self.fontComboBox = QFontComboBox(self.frame)
        self.horizontalLayout.addWidget(self.fontComboBox)
        self.setLayout(self.horizontalLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    playerBgColor = QColor('#EBFFEB')
    playerFgColor = QColor('#AAFF99')

    boardBgColor = QColor('#F2F2F2')
    boardFgColor = QColor('#FFCC00')

    # player1Grid = PlayerGrid(playerBgColor, playerFgColor)
    # player1Controls = PlayerControls(playerBgColor, playerFgColor, player1Grid, "Player 1")
    #
    # player2Grid = PlayerGrid(playerBgColor, playerFgColor)
    # player1Controls = PlayerControls(playerBgColor, playerFgColor, player1Grid, "Player 2")

    gameBoard = GameBoard(boardBgColor, boardFgColor)

    tileCollection = TileCollection()
    tileBag = TileBag()
    RummyKub = MainWin()
    RummyKub.show()
    # newGame()
sys.exit(app.exec_())