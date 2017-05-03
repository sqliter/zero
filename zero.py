import sys
import logging
from PySide.QtGui import QApplication
from mainwindow import ZMainWindow

def main():
    logging.basicConfig(filename='zero.log',level=logging.DEBUG)
    app=QApplication(sys.argv)
    mw=ZMainWindow()
    #mw.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
