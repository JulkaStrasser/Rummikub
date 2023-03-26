import sys, random
print(sys.version)
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog, QSizePolicy
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

from Tile import RummyTile
from Cell import BoardCell
from GridArchive import GridArchiveManager
import time
"""
Todo List.
- dodanie ze nie mozna wylozyc na poczatku gdy suma nie przekroczy 30
- dodanie messageboxa, gdy bedzie blad pierwszej tury
- czy jockery istnieja?
- usuniecie zmiennych globalnych 
 
"""


# ++++++++++++++++++++++++++++++++++++++++++++++
#          GLOBALS
# ++++++++++++++++++++++++++++++++++++++++++++++
tileColors = ["red", "black", "blue", "yellow"]
tileOwner = ["none", "player", "board", "bag"]
tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
numberOfColumns = 15
numberOfTilesToDeal = 15
player_turn = 0
change = False

def getCellCol(cell):
    print("getCellCol")
    return cell.getCol()

def newGame():
    gameBoard.removeAllTiles()
    player1.player_grid.removeAllTiles()
    player2.player_grid.removeAllTiles()
    player3.player_grid.removeAllTiles()
    player4.player_grid.removeAllTiles()
    tileCollection.clearTiles()  # set the owner of each tile to "none"
    tileBag.newGame()
    player1.player_grid.newDeal()
    player2.player_grid.newDeal()
    player3.player_grid.newDeal()
    player4.player_grid.newDeal()


class ImageLabel2(QLabel):
    def __init__(self):
        super(ImageLabel2, self).__init__()
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignTop)
        self.setFrameStyle(QFrame.Panel)
        self.setFixedWidth(120)
        self.setFixedHeight(37)
        # self.setMinimumHeight(40)

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

class MyLabel(QLabel):
    def __init__(self, legend):
        super(MyLabel, self).__init__()

        self.setText(legend)

        self.setFont(QFont('SansSerif', 12))
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), QColor('#F2F2F2'))
        self.pal.setColor(self.foregroundRole(), QColor('#B30000'))  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def updateText(self, newText):
        self.setText(newText)


class RemainingTilesIndicator(QWidget):
    def __init__(self, legend):
        super(RemainingTilesIndicator, self).__init__()

        self.myLayout = QHBoxLayout()
        self.myLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.myLegend = QLabel()
        self.myLegend.setFrameShape(QFrame.Panel)
        self.myLegend.setFrameShadow(QFrame.Sunken)
        self.myLegend.setLineWidth(3)
        # self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.myLegend.setText(legend)
        self.myLayout.addWidget(self.myLegend)
        self.setLayout(self.myLayout)
        self.setFont(QFont('SansSerif', 18))
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), QColor('#F2F2F2'))
        self.pal.setColor(self.foregroundRole(), QColor('#000000'))  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def updateText(self, newText):
        self.myLegend.setText(newText)


class RemainingTilesIndicator2(QLabel):
    def __init__(self, legend):
        super(RemainingTilesIndicator2, self).__init__()

        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(3)
        # self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.setText(legend)

        self.setFont(QFont('SansSerif', 18))
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), QColor('#F2F2F2'))
        self.pal.setColor(self.foregroundRole(), QColor('#000000'))  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def updateText(self, newText):
        self.setText(newText)

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
        self.setMinimumWidth(140)
        self.buttonBar = QVBoxLayout()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create buttons
        # ++++++++++++++++++++++++++++++++++++++++++++++++

        self.newGameButton = MyButton("Nowa gra")
        self.newGameButton.clicked.connect(newGame)

        self.ExitButton = MyButton("Wyjscie")
        self.ExitButton.clicked.connect(self.Exit)

        self.SaveGameStateButton = MyButton("Zapisz")
        self.SaveGameStateButton.clicked.connect(self.saveBoardState)

        self.RestoreGameStateButton = MyButton("Odswiez")
        self.RestoreGameStateButton.clicked.connect(self.restoreBoardState)

       

        self.buttonBar.addWidget(self.newGameButton)
        self.buttonBar.addWidget(self.ExitButton)
        self.buttonBar.addWidget(self.SaveGameStateButton)
        self.buttonBar.addWidget(self.RestoreGameStateButton)
        

        self.layout.addLayout(self.buttonBar)
        self.infoBar = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create info box
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # self.tilesLeftInfoBox = QPlainTextEdit()
        # tileLeftFont = QFont("Consolas", 10)
        # self.tilesLeftInfoBox.setFont(tileLeftFont)
        # self.tilesLeftInfoBox.setPlainText("All tiles in bag")
        # self.infoBar.addWidget(self.tilesLeftInfoBox)
        # self.layout.addLayout(self.infoBar)

        self.NoOfTilesInBagIndicator = RemainingTilesIndicator2("hjhh")
        self.layout.addWidget(self.NoOfTilesInBagIndicator)
        self.NoOfTilesInBagIndicator.updateText("0")

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

    def clearInfoBox(self):
        self.tilesLeftInfoBox.clear()

    def appendInfo(self, tempStr):
        self.tilesLeftInfoBox.appendPlainText(tempStr)

    def saveBoardState(self):
        gridArchiveManager.saveGameState()

    def saveBoardState(self):
        gridArchiveManager.saveGameState()

    def restoreBoardState(self):
        gridArchiveManager.restoreGameState()

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
        self.frozen = False
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
        print("Remove all tiles from the board")
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
            print("ERROR - trying to restore a grid of the wrong size !")
            return
        for n in range(len(grid)):
            index = grid[n]
            if index is not None:
                tile = tileCollection.getTileAtIndex(index)
                self.cellList[n].addTile(tile)




# ++++++++++++++++++++++++++++++++++++++++++++++
#          PLAYER CONTROLS
# ++++++++++++++++++++++++++++++++++++++++++++++
class PlayerControls(QFrame):
    def __init__(self, bgColor, fgColor, playerGrid, playerName):
        super(PlayerControls, self).__init__()
        self.playerGrid = playerGrid
        self.playerName = playerName
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))
        self.setLayout(self.layout)

        self.TakeTileButton = MyButton("Dobierz plytke")
        self.TakeTileButton.clicked.connect(self.takeTile)

        self.FreezeButton = MyButton("Zakoncz ture")
        # self.FreezeButton.clicked.connect(self.freeze)

        self.FrozenStateLabel = MyLabel("Twoja tura")

        self.playerNameLabel = MyLabel(playerName)

        self.layout.addWidget(self.playerNameLabel)
        self.layout.addWidget(self.TakeTileButton)
        self.layout.addWidget(self.FreezeButton)
        self.layout.addWidget(self.FrozenStateLabel)

        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def freeze(self):
        global change
        global player_turn
        print(self.playerName[6])
        if player_turn == int(self.playerName[6])-1:
            if self.playerGrid.isFrozen():
                self.playerGrid.thaw()
                self.FrozenStateLabel.updateText("Twoja tura")
            else:
                self.playerGrid.freeze()
                self.FrozenStateLabel.updateText("Nie twoja tura")
                change = True
                player_turn = (player_turn+1) % 4
                print(change)


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

# ++++++++++++++++++++++++++++++++++++++++++++++
#          GAME BOARD
# ++++++++++++++++++++++++++++++++++++++++++++++
class GameBoard(TileGridBaseClass):
    def __init__(self, bgColor, fgColor, gridName, rows, cols):
        super(GameBoard, self).__init__(rows, cols, bgColor, fgColor, gridName)
        self.listItems()
        self.all_sequences = []

    def listItems(self):
        print("List grid contents")
        cellsList = self.findChildren(BoardCell)
        for cell in cellsList:
            print(cell.row, cell.col)
            status = cell.getCellStatus()
            print(status[0])
            print(status[1])
            print()
    
    def detectSequences(self):
        print("Print neighbours")
        cellsList = self.findChildren(BoardCell)
        seq = []
        detected_sequence = False
        self.all_sequences = []
        for cell in cellsList:
            
            if cell.left != None:
                left_neighbour_status = cell.left.getCellStatus()
               
            else:
                left_neighbour_status ='Empty'

            if cell.right != None:
                right_neighbour_status = cell.right.getCellStatus()
               
            else:
                right_neighbour_status = 'Empty'
            
            # the first element of a squence
            if left_neighbour_status == 'Empty' and right_neighbour_status != 'Empty' and cell.getCellStatus() !='Empty':
                seq.append(cell)
                detected_sequence = True
            elif detected_sequence == True and left_neighbour_status != 'Empty' and right_neighbour_status != 'Empty':
                seq.append(cell)
            #the last element of a sequence
            elif left_neighbour_status != 'Empty' and right_neighbour_status == 'Empty' and cell.getCellStatus() !='Empty' and detected_sequence == True:
                seq.append(cell)
                detected_sequence = False
                if len(seq) > 2:
                    self.all_sequences.append(seq)
                else:
                    print('Blad ciag musi miec co najmniej 3 elementy !')
                    QMessageBox.warning(self,'Niedozwolony ruch','Sekwencja musi miec co najmniej 3 plytki !')
                    return False
                print(seq)
                seq = []
                # seq.clear()
        
        if len(self.all_sequences) == 0:
            return True
        else:
        #self.printAllSequences()
            return self.checkAllSequences()
    
    def printAllSequences(self):
        for i,seq in enumerate(self.all_sequences):
            print('Zbior ')
            print(seq)
            for cell in seq:
                status = cell.getCellStatus()
                print(status[0])
                print(status[1])
                print()
            print('---------')

    def checkAllSequences(self):
        ok = True
        for i,seq in enumerate(self.all_sequences):
            print('Check sequence')

            # 1. Create tokens color and number lists
            token_color_list = []
            token_number_list = []

            for cell in seq:
                status = cell.getCellStatus()
                token_color_list.append(status[0])
                token_number_list.append(int(status[1]))

            # 2. CHECK IF CORRECT SEQUENCE
            # Option1 : more than 3 in different colors
            check_diff_colors = self.check3diffColor(token_color_list, token_number_list)
            print('Option 1'+ str(check_diff_colors))

            # Option2: 1 color number, each one +1
            check_plus_num = self.checkPlusNumber(token_color_list, token_number_list)
            print('Option 2'+ str(check_plus_num))

            # IF BAD SEQ
            if check_diff_colors == False and check_plus_num == False:
                print('Nie mozna wykonac takiego ruchu !')
                for cell in seq:
                    cell.errorHighLightOn()
                QMessageBox.warning(self,'Niedozwolony ruch','Nie mozesz wykonac takiego ruchu')
                for cell in seq:
                    cell.errorHighLightOff()
                ok = False
                
        return ok
        

    def check3diffColor(self,token_color_list, token_number_list):
        #check if all numbers are the same
        numbers_equal = token_number_list.count(token_number_list[0]) == len(token_number_list)
        print('Numbers are equal'+ str(numbers_equal))

        #check if all colors are unique
        colors_unique = False
        if(len(set(token_color_list)) == len(token_color_list)):
            colors_unique = True
        print('Colors are unique' + str(colors_unique))

        if numbers_equal == True and colors_unique == True:
            return True
        else:
            return False
            
    def checkPlusNumber(self,token_color_list,token_number_list):
        #Check if colors are the same
        colors_equal = token_color_list.count(token_color_list[0]) == len(token_color_list)
        print('Colors are equal'+ str(colors_equal))

        #check +1 sequence
        numPlus = True
        last_item = token_number_list[0]
        num_len = len(token_number_list)
        for i in range(1,num_len):
            item = token_number_list[i]
            if(item - last_item) == 1:
                last_item = item
            else:
                numPlus = False
        print('Each number is +1 number before'+str(numPlus))
        
        if colors_equal == True and numPlus == True:
            return True
        else:
            return False
                
    
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

# ++++++++++++++++++++++++++++++++++++++++++++++
#          PLAYER GRID
# ++++++++++++++++++++++++++++++++++++++++++++++
class PlayerGrid(TileGridBaseClass):
    def __init__(self, bgColor, fgColor, gridName, rows, cols):
        super(PlayerGrid, self).__init__(rows, cols, bgColor, fgColor, gridName)
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  # 6600cc
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def newDeal(self):
        global tileBag, numberOfTilesToDeal
        for n in range(numberOfTilesToDeal):
            if tileBag.getNoOfTilesInBag() > 0:
                nextTile = tileBag.getTileFromBag()
                print( " takes a tile. It's ", str(nextTile.getColor()), str(nextTile.getValue()))
                for cell in self.cellList:
                    status = cell.getCellStatus()
                    if status == "Empty":
                        cell.addTile(nextTile)
                        break
            else:
                print("Whoops - tile bag is empty")
                break


# ++++++++++++++++++++++++++++++++++++++++++++++
#          TILE BAG
# ++++++++++++++++++++++++++++++++++++++++++++++
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
            RummyKub.controlPanel.NoOfTilesInBagIndicator.setText(str(len(self.tileBag) - 1))
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
        for n in [1,2]:
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


class TileDestinations():
    def __init__(self):
        self.validDestinations = []


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()


        self.controlPanel = ControlPanel()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Add everything to the grid layout
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.gameLayout = QGridLayout()
        self.gameLayout.addWidget(player1.player_grid, 0, 0)
        self.gameLayout.addWidget(player1.player_controls, 0, 1)

        self.gameLayout.addWidget(player3.player_grid, 0, 2)
        self.gameLayout.addWidget(player3.player_controls, 0, 3)

        self.gameLayout.addWidget(gameBoard, 1, 0, 3, 3)

        self.gameLayout.addWidget(player2.player_grid, 4, 0)
        self.gameLayout.addWidget(player2.player_controls, 4, 1)

        self.gameLayout.addWidget(player4.player_grid, 4, 2)
        self.gameLayout.addWidget(player4.player_controls, 4, 3)
        
        self.gameLayout.addWidget(self.controlPanel, 1, 3, 3 ,1)

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

def play():
    global player_turn
    gameTurn = 1
    game = True

    # Czy pierwsza tura
    first_turn = True

    #Sprawdzanie czy mozesz wziac zeton albo czy mozesz spasowac, na razie zawsze mozna zpasowac
    # pas_option = False 
    takeToken = True
    global change
    print(change)
    print(player_turn)
    freezePlayers(player_turn)
    
    if change == True:
            freezePlayers(player_turn)
    

def freezePlayers():
    global change, player_turn
    change = False
    
    if gameBoard.detectSequences() != True:
        pass
    # self.playerGrid.thaw()
    #     player_turn = (player_turn+1) % 4
    #         self.FrozenStateLabel.updateText("Twoja tura")
    #     else:
    #         self.playerGrid.freeze()
    #         self.FrozenStateLabel.updateText("Nie twoja tura")
    else:
        if player_turn == 0:
            #budzimy playera 1
            player1.player_controls.playerGrid.thaw()
            player1.player_controls.FrozenStateLabel.updateText("Twoja tura")
            player1.player_controls.setEnabled(True)

            player2.player_controls.playerGrid.freeze()
            player2.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player2.player_controls.setEnabled(False)

            player3.player_controls.playerGrid.freeze()
            player3.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player3.player_controls.setEnabled(False)

            player4.player_controls.playerGrid.freeze()
            player4.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player4.player_controls.setEnabled(False)

        elif(player_turn == 1):
            player2.player_controls.playerGrid.thaw()
            player2.player_controls.FrozenStateLabel.updateText("Twoja tura")
            player2.player_controls.setEnabled(True)

            player1.player_controls.playerGrid.freeze()
            player1.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player1.player_controls.setEnabled(False)

            player3.player_controls.playerGrid.freeze()
            player3.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player3.player_controls.setEnabled(False)

            player4.player_controls.playerGrid.freeze()
            player4.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player4.player_controls.setEnabled(False)
        elif(player_turn == 2):
            player3.player_controls.playerGrid.thaw()
            player3.player_controls.FrozenStateLabel.updateText("Twoja tura")
            player3.player_controls.setEnabled(True)
            
            player1.player_controls.playerGrid.freeze()
            player1.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player1.player_controls.setEnabled(False)

            player2.player_controls.playerGrid.freeze()
            player2.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player2.player_controls.setEnabled(False)

            player4.player_controls.playerGrid.freeze()
            player4.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player4.player_controls.setEnabled(False)
        elif(player_turn == 3):
            player4.player_controls.playerGrid.thaw()
            player4.player_controls.FrozenStateLabel.updateText("Twoja tura")
            player4.player_controls.setEnabled(True)

            player1.player_controls.playerGrid.freeze()
            player1.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player1.player_controls.setEnabled(False)

            player3.player_controls.playerGrid.freeze()
            player3.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player3.player_controls.setEnabled(False)

            player2.player_controls.playerGrid.freeze()
            player2.player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            player2.player_controls.setEnabled(False)

        player_turn = (player_turn+1)%4
    
    # gameBoard.listItems()

    
        

class Player():
    def __init__(self, player_id, player_name):
        self.player_id = player_id
        self.player_name = player_name
        self.player_grid = PlayerGrid(playerBgColor, playerFgColor, "PlayerGrid", 2, numberOfColumns)
        self.player_controls = PlayerControls(playerBgColor, playerFgColor, self.player_grid, self.player_name)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    playerBgColor = QColor('#A5A5A5')
    playerFgColor = QColor('#000000')

    boardBgColor = QColor('#F2F2F2')
    boardFgColor = QColor('#A5A5A5')

    player1 = Player(0,'Gracz 1')
    player1.player_controls.FreezeButton.clicked.connect(freezePlayers)
    
    player2 = Player(1,'Gracz 2')
    player2.player_controls.FreezeButton.clicked.connect(freezePlayers)

    player3 = Player(2,'Gracz 3')
    player3.player_controls.FreezeButton.clicked.connect(freezePlayers)

    player4 = Player(3,'Gracz 4')
    player4.player_controls.FreezeButton.clicked.connect(freezePlayers)


    gameBoard = GameBoard(boardBgColor, boardFgColor, "GameBoard", 8, numberOfColumns*2)
    print("gameBoard is of type ", str(type(gameBoard)))

    gridArchiveManager = GridArchiveManager(player1.player_grid, player2.player_grid, player3.player_grid, player4.player_grid, gameBoard)

    tileCollection = TileCollection()
    tileBag = TileBag()
    RummyKub = MainWin()
    RummyKub.show()
    newGame()
    freezePlayers()
    # #wyswietlanie plytek gracza
    # print("Gracz 3")
    # for cell in player3.player_grid.cellList:
    #     status = cell.getCellStatus()
    #     print(status)
    #     # print(status[0])
    #     # print(status[1])

    # play()
    #wyswietlanie planszy, nie dziala bo nie ma petli gownej
    print('Plansza do gry:')
    # gameBoard.listItems()
    # for cell in gameBoard.cellList:
    #     status = cell.getCellStatus()
sys.exit(app.exec_())