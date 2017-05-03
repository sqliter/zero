# -*- coding: utf-8 -*-

from PySide import QtCore
from PySide.QtGui import *
from PySide.QtCore import *
import backend

class ZCtrlPanelSignals(QtCore.QObject):
    mouseInCtrls=QtCore.Signal()

class ZCtrlPanel(QFrame):

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.signals=ZCtrlPanelSignals()

        # self.lbl_time=QLabel(self.tr('time:'))
        self.slider_time = QSlider(Qt.Horizontal)
        self.slider_vol = QSlider(Qt.Horizontal)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.valueChanged.connect(self.on_vol_setting)

        self.btn_play = QPushButton()
        self.btn_play.setIcon(QIcon('./icon/play.svg'))
        self.btn_play.setIconSize(QSize(16, 16))
        self.btn_play.setToolTip(self.tr('play/pause'))
        self.btn_play.clicked.connect(self.on_play)

        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(QIcon('./icon/first.svg'))
        self.btn_prev.setIconSize(QSize(16, 16))
        self.btn_prev.setToolTip(self.tr('previous'))
        self.btn_prev.clicked.connect(self.on_prev)

        self.btn_next = QPushButton()
        self.btn_next.setIcon(QIcon('./icon/last.svg'))
        self.btn_next.setIconSize(QSize(16, 16))
        self.btn_next.setToolTip(self.tr('last'))
        self.btn_next.clicked.connect(self.on_next)

        self.lbl_pos = QLabel(self.tr('0:00/0:00'))

        self.btn_vol = QPushButton()
        self.btn_vol.setIcon(QIcon('./icon/vol.svg'))
        self.btn_vol.setIconSize(QSize(16, 16))
        self.btn_vol.setToolTip(self.tr('mute'))
        #self.btn_vol.clicked.connect(self.on_mute)

        self.btn_fullscreen = QPushButton()
        self.btn_fullscreen.setIcon(QIcon('./icon/fullscreen.svg'))
        self.btn_fullscreen.setToolTip(self.tr('fullscreen'))
        self.btn_fullscreen.setIconSize(QSize(16, 16))
        #self.btn_fullscreen.clicked.connect(self.on_fullscreen)

        hbox1 = QHBoxLayout()
        # hbox1.addWidget(self.lbl_time)
        hbox1.addWidget(self.slider_time, 1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.btn_prev)
        hbox2.addWidget(self.btn_play)
        hbox2.addWidget(self.btn_next)
        hbox2.addWidget(self.btn_fullscreen)
        hbox2.addWidget(self.lbl_pos)
        hbox2.addStretch(1)
        hbox2.addWidget(self.btn_vol)
        hbox2.addWidget(self.slider_vol)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        self.oldPos = None
        self.setMouseTracking(True)
        self.setWindowTitle("Control Panel")
      

    def hideEvent(self, event):
        self.oldPos = self.pos()


    def showEvent(self, event):
        if self.oldPos:
            self.move(self.oldPos)
         
    def moveEvent(self, event):
        self.signals.mouseInCtrls.emit()

    def mouseMoveEvent(self, event):
        self.signals.mouseInCtrls.emit()
      
    def on_play(self):
        backend.mplayer.play()
        if backend.mplayer.playing:
            self.btn_play.setIcon(QIcon('./icon/pause.svg'))
        else:
            self.btn_play.setIcon(QIcon('./icon/play.svg'))


    def on_prev(self):
        backend.mplayer.prev()

    def on_next(self):
        backend.mplayer.next()

    def on_fullscreen(self):
        backend.mplayer.fullscreen()

    def on_vol_setting(self,vol):
        backend.mplayer.setVolume(vol)
