from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class AnalogTimer(QWidget):

	def __init__(self, parent = None):
		
		super(AnalogTimer, self).__init__(parent)
		timer = QTimer(self)

		# timer update each 1 s
		timer.timeout.connect(self.update)
		timer.start(1000)
        
       
		self.setWindowTitle('AnalogTimer')
		self.setGeometry(200, 200, 300, 300)
		self.setStyleSheet("background : black;")

		# creating second hand
		self.sPointer = QPolygon([QPoint(1, 1),
								QPoint(-1, 1),
								QPoint(0, -90)])
		
        #set hands colors
		self.bColor = Qt.black
		self.sColor = Qt.red
		self.tik0 = QTime.currentTime()

	def paintEvent(self, event):

		rec = min(self.width(), self.height())
		tik = QTime.currentTime()
		painter = QPainter(self)

		def drawPointer(color, rotation, pointer):
			painter.setBrush(QBrush(color))
			painter.save()
			painter.rotate(rotation)
			painter.drawConvexPolygon(pointer)
			painter.restore()

		painter.setRenderHint(QPainter.Antialiasing)
		painter.translate(self.width() / 2, self.height() / 2)
		painter.scale(rec / 200, rec / 200)
		painter.setPen(QtCore.Qt.NoPen)
		drawPointer(self.sColor, (6 * (tik.second()-self.tik0.second())), self.sPointer)
		painter.setPen(QPen(self.bColor))

		for i in range(0, 60):

			if (i % 5) == 0:
				painter.drawLine(87, 0, 97, 0)

			painter.rotate(6)
		painter.end()


if __name__ == '__main__':
	
    app = QApplication(sys.argv)
    win = AnalogTimer()
    win.show()
    exit(app.exec_())


