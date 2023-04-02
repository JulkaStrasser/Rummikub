import sys, random
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog, QSizePolicy
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

from Tile import RummyTile
from Cell import BoardCell
from GridArchive import GridArchiveManager
import time
from AnalogTimer import AnalogTimer
import logging
from PyQt5 import QtGui, QtCore,QtWidgets

"""
Todo List.
- dodanie ze nie mozna wylozyc na poczatku gdy suma nie przekroczy 30 (to nie dziala do konaca bo nie zapisuje co dodal gracz i jak sie pojawi na planszy cos o, to wszyscy gracze sie ciesza xD)
- koniec tury gracza, gdy nie zmiesci sie w czasie
- czy jockery istnieja?
- logger ?
- .rc obrazki ?
 
"""


# ++++++++++++++++++++++++++++++++++++++++++++++
#          GLOBALS
# ++++++++++++++++++++++++++++++++++++++++++++++
class Main():
    tileColors = ["red", "black", "blue", "yellow"]
    tileOwner = ["none", "player", "board", "bag"]
    tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    numberOfColumns = 15
    numberOfTilesToDeal = 15
    player_turn = 0
    change = False
    players_first_turn = [True,True,True,True]

def getCellCol(cell):
    # logging.debug("getCellCol")
    return cell.getCol()

def newGame():
    gameBoard.removeAllTiles()
    players[0].player_grid.removeAllTiles()
    players[1].player_grid.removeAllTiles()
    players[2].player_grid.removeAllTiles()
    players[3].player_grid.removeAllTiles()
    tileCollection.clearTiles()  # set the owner of each tile to "none"
    tileBag.newGame()
    players[0].player_grid.newDeal()
    players[1].player_grid.newDeal()
    players[2].player_grid.newDeal()
    players[3].player_grid.newDeal()


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
        # logging.debug("Taking a tile")
        #logging.debug("Taking a tile")
        if tileBag.getNoOfTilesInBag() > 0:
            nextTile = tileBag.getTileFromBag()
            gameBoard.AddTileFromBag(nextTile)


    def Exit(self):
        # logging.debug("Exiting....")
        logging.info('Exiting')
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
                #logging.debug("Cell ", str(row), " ", str(col), " has neighbours ", "None", " and ", str(right.getPosition()))
                ##logging.debug("Cell ", str(row), " ", str(col), " has neighbours ", "None", " and ", str(right.getPosition()))
            elif col == self.cols - 1:
                left = self.cellList[n - 1]
                right = None
                #logging.debug("Cell ", str(row), " ", str(col), " has neighbours ", str(left.getPosition()), " and ", "None")
                ##logging.debug("Cell ", str(row), " ", str(col), " has neighbours ", str(left.getPosition()), " and ", "None")
            else:
                left = self.cellList[n - 1]
                right = self.cellList[n + 1]
                # logging.debug("Cell ", str(row), " ", str(col), " has neighbours ", str(left.getPosition()), " and ",
                #       str(right.getPosition()))
                ##logging.debug("Cell ", str(row), " ", str(col), " has neighbours ", str(left.getPosition()), " and ",
                        #str(right.getPosition()))
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
        logging.debug("Remove all tiles from the board")
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
            logging.debug("ERROR - trying to restore a grid of the wrong size !")
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
        logging.debug(self.playerName[6])
        if main.player_turn == int(self.playerName[6])-1:
            if self.playerGrid.isFrozen():
                self.playerGrid.thaw()
                self.FrozenStateLabel.updateText("Twoja tura")
            else:
                self.playerGrid.freeze()
                self.FrozenStateLabel.updateText("Nie twoja tura")
                main.change = True
                main.player_turn = (main.player_turn+1) % 4
                logging.debug(main.change)


    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setBackgroundColor(color)

    def takeTile(self, tile):
        if players[main.player_turn-1].drawedTile == False:
            if tileBag.getNoOfTilesInBag() > 0:
                nextTile = tileBag.getTileFromBag()
                logging.debug(self.playerName + " takes a tile. It's " + str(nextTile.getColor()) + str(nextTile.getValue()))
                for cell in self.playerGrid.cellList:
                    status = cell.getCellStatus()
                    if status == "Empty":
                        cell.addTile(nextTile)
                        players[main.player_turn-1].drawedTile = True
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
        logging.debug("List grid contents")
        cellsList = self.findChildren(BoardCell)
        for cell in cellsList:
            logging.debug(str(cell.row) + str(cell.col))
            status = cell.getCellStatus()
            logging.debug(status[0])
            logging.debug(status[1])
    
    def detectSequences(self):
        logging.debug("Print neighbours")
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
                    logging.debug('Blad ciag musi miec co najmniej 3 elementy !')
                    QMessageBox.warning(self,'Niedozwolony ruch','Sekwencja musi miec co najmniej 3 plytki !')
                    return False
                logging.debug(seq)
                seq = []
                # seq.clear()
            elif left_neighbour_status == 'Empty' and right_neighbour_status == 'Empty' and cell.getCellStatus() != 'Empty':
                QMessageBox.warning(self,'Niedozwolony ruch','Sekwencja musi miec co najmniej 3 plytki !')
                return False
        
        if len(self.all_sequences) == 0:
            return True
        else:
        #self.printAllSequences()
            return self.checkAllSequences()
    
    def printAllSequences(self):
        for i,seq in enumerate(self.all_sequences):
            logging.debug('Zbior ')
            logging.debug(seq)
            for cell in seq:
                status = cell.getCellStatus()
                logging.debug(status[0])
                logging.debug(status[1])
                logging.debug()
            logging.debug('---------')

    def checkAllSequences(self):
        ok = True
        for i,seq in enumerate(self.all_sequences):
            logging.debug('Check sequence')

            # 1. Create tokens color and number lists
            token_color_list = []
            token_number_list = []

            for cell in seq:
                status = cell.getCellStatus()
                token_color_list.append(status[0])
                token_number_list.append(int(status[1]))

            # 2. CHECK IF CORRECT SEQUENCE
            #check if player first turn
            if (self.checkSum(token_number_list) == False):
                ok = False
            # Option1 : more than 3 in different colors
            else:
                check_diff_colors = self.check3diffColor(token_color_list, token_number_list)
                logging.debug('Option 1'+ str(check_diff_colors))

                # Option2: 1 color number, each one +1
                check_plus_num = self.checkPlusNumber(token_color_list, token_number_list)
                logging.debug('Option 2'+ str(check_plus_num))

                # IF BAD SEQ
                if check_diff_colors == False and check_plus_num == False:
                    logging.debug('Nie mozna wykonac takiego ruchu !')
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
        logging.debug('Numbers are equal'+ str(numbers_equal))

        #check if all colors are unique
        colors_unique = False
        if(len(set(token_color_list)) == len(token_color_list)):
            colors_unique = True
        logging.debug('Colors are unique' + str(colors_unique))

        if numbers_equal == True and colors_unique == True:
            return True
        else:
            return False
            
    def checkPlusNumber(self,token_color_list,token_number_list):
        #Check if colors are the same
        colors_equal = token_color_list.count(token_color_list[0]) == len(token_color_list)
        logging.debug('Colors are equal'+ str(colors_equal))

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
        logging.debug('Each number is +1 number before'+str(numPlus))
        
        if colors_equal == True and numPlus == True:
            return True
        else:
            return False
                
    def checkSum(self, token_number_list):
        sum = 0
        last_turn = main.player_turn-1
        if last_turn == -1:
            last_turn = 3
        logging.debug('player turn:')
        logging.debug(last_turn)
        logging.debug("Czy pierwsza tura ?")
        logging.debug(main.players_first_turn[last_turn])
        if main.players_first_turn[last_turn] == True:
            for item in token_number_list:
                sum += item
            logging.debug(sum)

            if(sum<30):
                QMessageBox.warning(self,'Niedozwolony ruch','W pierwszej turze suma plytek musi byc wieksza od 30 !')
                logging.debug("Czy pierwsza tura2 ?")
                logging.debug(main.players_first_turn[last_turn])
                return False
            else:
                main.players_first_turn[last_turn] = False
                logging.debug("Czy pierwsza tura2 ?")
                logging.debug(main.players_first_turn[last_turn])
                return True
        else:
            return True
        

    def AddTileFromBag(self, tile):
        logging.debug("AddTileFromBag")

        for cell in self.cellList:
            status = cell.getCellStatus()
            if status == "Empty":
                cell.addTile(tile)
                break

    def GetNextEmptyCellPosition(self):
        logging.debug("GetNextEmptyCellPosition")

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
        self.pal.setColor(self.foregroundRole(), fgColor)  
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def newDeal(self):
        
        for n in range(main.numberOfTilesToDeal):
            if tileBag.getNoOfTilesInBag() > 0:
                nextTile = tileBag.getTileFromBag()
                logging.debug( " dobieranie plytki. Jest to : " + str(nextTile.getColor()) + str(nextTile.getValue()))
                for cell in self.cellList:
                    status = cell.getCellStatus()
                    if status == "Empty":
                        cell.addTile(nextTile)
                        break
            else:
                logging.debug("Worek z plytkami jest pusty!")
                break

    def checkWinner(self):
        isWinner = True
        for cell in self.cellList:
                status = cell.getCellStatus()
                if status != "Empty":
                    isWinner = False
                    break
        if isWinner == True:
            QMessageBox.information(self,'Koniec gry','Zwyciezyl gracz '+ str(main.player_turn))
        return isWinner
    
    
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
        logging.debug("finished filling tile bag")

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
        logging.debug("finished filling tile bag")
        logging.debug("Shake the tile bag")
        random.shuffle(self.tileBag)


class TileCollection():
    def __init__(self):
        self.tiles = []
        index = 0
        for n in [1,2]:
            for tileColor in main.tileColors:
                for tileVal in main.tileValues:
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
            logging.debug("ERROR: getTileAtIndex was asked for the tile at index ", str(index), " which is out of range")
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

class MyView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)

        self.scene = QGraphicsScene(self)
        self.item = QGraphicsRectItem(200,300,1000,800)
        self.scene.addItem(self.item)
        self.setScene(self.scene)

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()

        self.view=MyView()
        self.setCentralWidget(self.view)

        self.controlPanel = ControlPanel()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Add everything to the grid layout
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.gameLayout = QGridLayout()
        self.gameLayout.addWidget(players[0].player_grid, 0, 0)
        self.gameLayout.addWidget(players[0].player_controls, 0, 1)

        self.gameLayout.addWidget(players[2].player_grid, 0, 2)
        self.gameLayout.addWidget(players[2].player_controls, 0, 3)

        self.gameLayout.addWidget(gameBoard, 1, 0, 3, 3)

        self.gameLayout.addWidget(players[1].player_grid, 4, 0)
        self.gameLayout.addWidget(players[1].player_controls, 4, 1)

        self.gameLayout.addWidget(players[3].player_grid, 4, 2)
        self.gameLayout.addWidget(players[3].player_controls, 4, 3)
        
        self.gameLayout.addWidget(self.controlPanel, 1, 3, 2 ,1)

        self.AnalogTimer = AnalogTimer()
        self.AnalogTimer.setGeometry(QtCore.QRect(110, 290, 200, 200))
        self.gameLayout.addWidget(self.AnalogTimer, 3, 3, 1 ,1)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.gameLayout)

        self.setCentralWidget(self.mainWidget)

        


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
    
    gameTurn = 1
    game = True

    # Czy pierwsza tura
    first_turn = True

    #Sprawdzanie czy mozesz wziac zeton albo czy mozesz spasowac, na razie zawsze mozna zpasowac
    # pas_option = False 
    takeToken = True
    
    logging.debug(main.change)
    logging.debug(main.player_turn)
    freezePlayers(main.player_turn)
    
    if main.change == True:
            freezePlayers(main.player_turn)
    

def freezePlayers():
    
    main.change = False
    
    if players[main.player_turn-1].player_grid.checkWinner() == True:
        logging.debug('Gracz'+str(main.player_turn)+' jest zwyciezca')
        sys.exit()

    if gameBoard.detectSequences() != True:
        pass
    
    else:
        players[main.player_turn-1].drawedTile = False
        if main.player_turn == 0:
            #budzimy playera 1
            players[0].player_controls.playerGrid.thaw()
            players[0].player_controls.FrozenStateLabel.updateText("Twoja tura")
            players[0].player_controls.setEnabled(True)

            players[1].player_controls.playerGrid.freeze()
            players[1].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[1].player_controls.setEnabled(False)

            players[2].player_controls.playerGrid.freeze()
            players[2].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[2].player_controls.setEnabled(False)

            players[3].player_controls.playerGrid.freeze()
            players[3].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[3].player_controls.setEnabled(False)

        elif(main.player_turn == 1):
            players[1].player_controls.playerGrid.thaw()
            players[1].player_controls.FrozenStateLabel.updateText("Twoja tura")
            players[1].player_controls.setEnabled(True)

            players[0].player_controls.playerGrid.freeze()
            players[0].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[0].player_controls.setEnabled(False)

            players[2].player_controls.playerGrid.freeze()
            players[2].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[2].player_controls.setEnabled(False)

            players[3].player_controls.playerGrid.freeze()
            players[3].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[3].player_controls.setEnabled(False)
        elif(main.player_turn == 2):
            players[2].player_controls.playerGrid.thaw()
            players[2].player_controls.FrozenStateLabel.updateText("Twoja tura")
            players[2].player_controls.setEnabled(True)
            
            players[0].player_controls.playerGrid.freeze()
            players[0].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[0].player_controls.setEnabled(False)

            players[1].player_controls.playerGrid.freeze()
            players[1].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[1].player_controls.setEnabled(False)

            players[3].player_controls.playerGrid.freeze()
            players[3].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[3].player_controls.setEnabled(False)
        elif(main.player_turn == 3):
            players[3].player_controls.playerGrid.thaw()
            players[3].player_controls.FrozenStateLabel.updateText("Twoja tura")
            players[3].player_controls.setEnabled(True)

            players[0].player_controls.playerGrid.freeze()
            players[0].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[0].player_controls.setEnabled(False)

            players[2].player_controls.playerGrid.freeze()
            players[2].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[2].player_controls.setEnabled(False)

            players[1].player_controls.playerGrid.freeze()
            players[1].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            players[1].player_controls.setEnabled(False)

        main.player_turn = (main.player_turn+1)%4
    
    # gameBoard.listItems()

    
        

class Player():
    def __init__(self, player_id, player_name,player_first_turn):
        self.player_id = player_id
        self.player_name = player_name
        self.player_grid = PlayerGrid(playerBgColor, playerFgColor, "PlayerGrid", 2, main.numberOfColumns)
        self.player_controls = PlayerControls(playerBgColor, playerFgColor, self.player_grid, self.player_name)
        self.player_first_turn = player_first_turn
        self.drawedTile = False
    
    def change_first_turn(self,first_turn):
        self.player_first_turn = first_turn
        

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class MyDialog(QtWidgets.QDialog, QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

        logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('file.log')
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().addHandler(c_handler)
        logging.getLogger().addHandler(f_handler)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)
        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(logTextBox.widget)
        self.setLayout(layout)

        self.show()
        self.raise_()
        self.app = QtWidgets.QApplication(sys.argv)
        #sys.exit(self.app.exec_())

        # Connect signal to slot
        MyDialog.test()
        MyDialog.instance = self

    def test():
        #logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')
        
if __name__ == "__main__":
    main = Main()
    app = QApplication(sys.argv)
    dlg = MyDialog()

    playerBgColor = QColor('#A5A5A5')
    playerFgColor = QColor('#000000')

    boardBgColor = QColor('#F2F2F2')
    boardFgColor = QColor('#A5A5A5')

    players = []
    players.append(Player(0,'Gracz 1',True))
    players[0].player_controls.FreezeButton.clicked.connect(freezePlayers)
    
    players.append(Player(1,'Gracz 2', True)) 
    players[1].player_controls.FreezeButton.clicked.connect(freezePlayers)

    players.append(Player(2,'Gracz 3', True))
    players[2].player_controls.FreezeButton.clicked.connect(freezePlayers)

    players.append(Player(3,'Gracz 4', True))
    players[3].player_controls.FreezeButton.clicked.connect(freezePlayers)


    gameBoard = GameBoard(boardBgColor, boardFgColor, "GameBoard", 8, main.numberOfColumns*2)
    logging.debug("gameBoard is of type " + str(type(gameBoard)))

    gridArchiveManager = GridArchiveManager(players[0].player_grid, players[1].player_grid, players[2].player_grid, players[3].player_grid, gameBoard)

    tileCollection = TileCollection()
    tileBag = TileBag()
    RummyKub = MainWin()
    RummyKub.show()
    
    newGame()
    
    freezePlayers()
   
    
    
  
sys.exit(app.exec_())