import logging
from PyQt5 import QtGui, QtCore,QtWidgets


# w nawiasie od jakiego poziomu zaczynamy
# logging.basicConfig(level = logging.DEBUG, filename="rumikub.log", filemode="w", format = "%(asctime)s - %(levelname)s - %(message)s")

# #Poziomy logowania:
# # logging.debug()
# # logging.info()
# # logging.warning()
# # logging.error()
# # logging.critical()

# logging.debug("debugujemy")
# logging.info("info")
# logging.warning("uwaga")
# logging.error("blad")
# logging.critical("blad krytyczny")

# try:
#     1/0
# except ZeroDivisionError as e:
#     logging.exception("ZeroDivisionError")

import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')



import sys
from PyQt5 import QtWidgets
import logging

# Uncomment below for terminal log messages
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)
        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(logTextBox.widget)
        self.setLayout(layout)

        # Connect signal to slot
        self.test()

    def test(self):
        logging.debug('damn, a bug')
        logger.debug('damn, a bug')
        logging.info('something to remember')
        logger.info('something to remember')
        logging.warning('that\'s not right')
        logger.warning('that\'s not right')
        logging.error('foobar')
        logger.error('foobar')


def window_logger():
    app = QtWidgets.QApplication(sys.argv)
    dlg = MyDialog()
    logging.warning('Uwazaj')
    logger.warning('Uwazaj')
    logging.info('OKI')
    logger.info('OKI')
    logging.critical('Tragedia')
    logger.critical('Tragedia')
    dlg.show()
    dlg.raise_()
    sys.exit(app.exec_())

window_logger()
