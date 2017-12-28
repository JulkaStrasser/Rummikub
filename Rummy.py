import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog, QSizePolicy

from PyQt5.QtGui import QFont, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

from Tile import RummyTile
from Cell import BoardCell


# from Board import player1Grid, player2Grid, gameBoard, tileCollection, tileBag

# ++++++++++++++++++++++++++++++++++++++++++++++
#          GLOBALS
# ++++++++++++++++++++++++++++++++++++++++++++++
tileColors = ["red", "black", "blue", "yellow"]
tileOwner = ["none", "player", "board", "bag"]
tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

def getCellCol(cell):
    print("getCellCol")
    return cell.getCol()

def newGame():
    gameBoard.removeAllTiles()
    player1Grid.removeAllTiles()
    player2Grid.removeAllTiles()
    tileCollection.clearTiles()  # set the owner of each tile to "none"
    tileBag.newGame()
    player1Grid.newDeal()
    player2Grid.newDeal()


class ImageLabel2(QLabel):
    def __init__(self):
        super(ImageLabel2, self).__init__()
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignTop)
        self.setFrameStyle(QFrame.Panel)

        self.setMinimumHeight(40)

    def showImageByPath(self, path):

        if path:
            image = QImage(path)
            pp = QPixmap.fromImage(image)
            pixmapHeight = pp.height()
            labelHeight = self.height()
            if pixmapHeight < labelHeight:
                scalingFactor = float(pixmapHeight) / labelHeight
            else:
                scalingFactor = 1.0
            print(" Scaling factor = %f", scalingFactor)
            self.setPixmap(pp.scaled(
                self.size()*scalingFactor,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation))
            self.show()

class MyButton(QPushButton):
    def __init__(self, text):
        super(MyButton, self).__init__()
        self.setFixedWidth(120)
        self.setFixedHeight(25)
        self.setFont(QFont('SansSerif', 10))
        self.setText(text)

class MyLabel(QWidget):
    def __init__(self, legend):
        super(MyLabel, self).__init__()
        self.myLayout = QHBoxLayout()
        self.myLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.myLegend = QLabel()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.myLegend.setText(legend)
        self.myLayout.addWidget(self.myLegend)
        self.setLayout(self.myLayout)
        self.setFont(QFont('SansSerif', 12))
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), QColor('#FFFF00'))
        self.pal.setColor(self.foregroundRole(), QColor('#7030A0'))  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)
    def updateText(self, newText):
        self.myText.setText(newText)

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
        self.setMinimumHeight(300)
        self.setMinimumWidth(200)
        self.buttonBar = QVBoxLayout()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create buttons
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.addTileButton = MyButton("Take Tile")
        self.addTileButton.clicked.connect(self.takeTile)

        self.newGameButton = MyButton("New Game")
        self.newGameButton.clicked.connect(newGame)

        self.ExitButton = MyButton("Exit")
        self.ExitButton.clicked.connect(self.Exit)

        self.ChangeBackgroundColorButton = MyButton("Bg Color")
        self.ChangeBackgroundColorButton.clicked.connect(self.ChangeBackgroundColor)

        self.ChangeForegroundColorButton = MyButton("Fg Color")
        self.ChangeForegroundColorButton.clicked.connect(self.ChangeForegroundColor)

        self.ListBoardButton = MyButton("List Board")
        self.ListBoardButton.clicked.connect(self.listBoard)

        self.MasterListButton = MyButton("Master Tile List")
        self.MasterListButton.clicked.connect(self.masterTileList)

        self.buttonBar.addWidget(self.addTileButton)
        self.buttonBar.addWidget(self.newGameButton)
        self.buttonBar.addWidget(self.ExitButton)
        self.buttonBar.addWidget(self.ChangeBackgroundColorButton)
        self.buttonBar.addWidget(self.ChangeForegroundColorButton)
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
        for row in range(self.rows):
            for col in range(self.cols):
                newCell = BoardCell(row, col, bgColor, fgColor, gridName)
                # newCell.setCellListIndex(len(self.cellList))
                self.tileGrid.addWidget(newCell, row, col)  # i=row j=col
                self.cellList.append(newCell)
        self.setLayout(self.tileGrid)
        # tell each cell who it's neighbours are
        for n in range(len(self.cellList)):
            cell = self.cellList[n]
            (row, col) = cell.getPosition()
            if col == 0:
                left = None
                right = self.cellList[n+1]
                print("Cell ", str(row), " ", str(col), " has neighbours ", "None", " and ", str(right.getPosition()))
            elif col == self.cols - 1:
                left = self.cellList[n - 1]
                right = None
                print("Cell ", str(row), " ", str(col), " has neighbours ", str(left.getPosition()), " and ", "None")
            else:
                left = self.cellList[n - 1]
                right = self.cellList[n + 1]
                print("Cell ", str(row), " ", str(col), " has neighbours ", str(left.getPosition()), " and ",
                      str(right.getPosition()))
            cell.setNeighbours(left, right)

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




class PlayerControls(QFrame):
    def __init__(self, bgColor, fgColor, playerGrid, playerName):
        super(PlayerControls, self).__init__()
        self.playerGrid = playerGrid
        self.playerName = playerName
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop))
        self.setLayout(self.layout)
        self.TakeTileButton = MyButton("Take Tile")
        self.TakeTileButton.clicked.connect(self.takeTile)

        # self.playerNameLabel = MyLabel(playerName)
        self.playerNameLabel = ImageLabel2()
        self.playerNameLabel.showImageByPath("images/player1.png")

        self.layout.addWidget(self.playerNameLabel)
        self.layout.addWidget(self.TakeTileButton)

        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setBackgroundColor(color)

    def takeTile(self, tile):
        global tileBag
        if tileBag.getNoOfTilesInBag() > 0:
            nextTile = tileBag.getTileFromBag()
            print(self.playerName, " takes a tile. It's ", str(nextTile.getColor()), str(nextTile.getValue()))
            for cell in self.playerGrid.cellList:
                status = cell.getCellStatus()
                if status == "Empty":
                    cell.addTile(nextTile)
                    break

    def getPlayerName(self):
        return self.playerName

class GameBoard(TileGridBaseClass):
    def __init__(self, bgColor, fgColor, gridName):
        super(GameBoard, self).__init__(8, 28, bgColor, fgColor, gridName)
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
    def __init__(self, bgColor, fgColor, gridName):
        super(PlayerGrid, self).__init__(2, 28, bgColor, fgColor, gridName)
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
        for tileColor in tileColors:
            for tileVal in tileValues:
                self.tiles.append(RummyTile(tileColor, tileVal, index))
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
        self.gameLayout.addWidget(player1Grid, 0, 0)
        self.gameLayout.addWidget(player1Controls, 0, 1)
        self.gameLayout.addWidget(gameBoard, 1, 0, 3, 1)
        self.gameLayout.addWidget(player2Grid, 4, 0)
        self.gameLayout.addWidget(player2Controls, 4, 1)
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

    player1Grid = PlayerGrid(playerBgColor, playerFgColor, "Player1")
    player1Controls = PlayerControls(playerBgColor, playerFgColor, player1Grid, "Player 1")

    player2Grid = PlayerGrid(playerBgColor, playerFgColor, "Player2")
    player2Controls = PlayerControls(playerBgColor, playerFgColor, player1Grid, "Player 2")

    gameBoard = GameBoard(boardBgColor, boardFgColor, "GameBoard")

    tileCollection = TileCollection()
    tileBag = TileBag()
    RummyKub = MainWin()
    RummyKub.show()
    newGame()
sys.exit(app.exec_())