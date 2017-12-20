from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import QTableView, QAbstractItemView
# import cPickle
import pickle

class DragTable(QTableView):
    def __init__(self, parent = None):
        super(DragTable, self).__init__(parent)
        self.setDragEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/pubmedrecord"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, event):
        indices = self.selectedIndexes()
        selected = set()
        for index in indices:
            selected.add(index.row())
        bstream = pickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/pubmedrecord", bstream)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = QtGui.QPixmap(":/drag.png")

        drag.setHotSpot(QtCore.QPoint(pixmap.width() / 3, pixmap.height() / 3))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)

    def mouseMoveEvent(self, event):
        self.startDrag(event)

class TagLabel(QtGui.QLabel):
    def __init__(self, text, color, parent=None):
        super(TagLabel, self).__init__(parent)
        self.tagColor = color
        self.setText(text)
        self.setStyleSheet("QLabel { background-color: %s; font-size: 14pt; }" % self.tagColor)
        self.defaultStyle = self.styleSheet()
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/pubmedrecord"):
            self.set_bg(True)
            event.accept()
        else:
            event.reject()

    def dragLeaveEvent(self, event):
        self.set_bg(False)
        event.accept()

    def dropEvent(self, event):
        self.set_bg(False)
            data = event.mimeData()
            bstream = data.retrieveData("application/pubmedrecord", QtCore.QVariant.ByteArray)
            selected = pickle.loads(bstream.toByteArray())
            event.accept()
            self.emit(QtCore.SIGNAL("dropAccepted(PyQt_PyObject)"), (selected, str(self.text()), str(self.tagColor)))

        def set_bg(self, active=False):
            if active:
                style = "QLabel {background: yellow; font-size: 14pt;}"
                self.setStyleSheet(style)
            else:
                self.setStyleSheet(self.defaultStyle)



app = QtGui.QApplication([])

l = TagLabel("bla bla bla bla bla bla bla", "red")
l.show()

m = QtGui.QStandardItemModel()
for _ in range(4):
    m.appendRow([QtGui.QStandardItem(x) for x in ["aap", "noot", "mies"]])

t = DragTable()
t.setModel(m)
t.show()

def h(o):
    print("signal handled", o)
l.connect(l, QtCore.SIGNAL("dropAccepted(PyQt_PyObject)"), h)

app.exec_()