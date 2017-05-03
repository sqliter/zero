#coding=utf-8

from PySide.QtCore import *
from PySide.QtGui import QTableWidget

class ZPlayListWidget(QTableWidget):
    def __init__(self):
        super(ZPlayListWidget,self).__init__()

        self.row_count=0
        self.header_labels=['.','title','album','filename']
        self.setHorizontalHeaderLabels(self.header_labels)