# -*- coding: utf-8 -*-
import logging
from PySide import QtCore
from PySide.QtGui import *
from PySide.QtCore import *
import backend
from ctrl_panel import ZCtrlPanel

# class ZVWSignals(QObject):
#     fullscreenDisabled=QtCore.Signal()

class ZVideoWidget(QWidget):
    def __init__(self,on_fullscreen):
        QWidget.__init__(self)

        #self.signals=ZVWSignals()

        self.fullscreen = False
        self.moveControls = False
        self.frameHeight = 0

        self.controlTimer = QTimer()
        self.controlTimer.setInterval(2000)

        self.on_fullscreen=on_fullscreen
        self.createUI()
        self.controlTimer.timeout.connect(self.hideCtrlPanel)
      
        self.setMouseTracking(True)
        self.setWindowTitle("Video Widget")
      
    def createUI(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
      
        self.video_view = ZVideoView(self)

        self.ctrl_panel = ZCtrlPanel(self)
        self.ctrl_panel.hide()
        self.ctrl_panel.signals.mouseInCtrls.connect(self.controlTimer.stop)
        self.ctrl_panel.btn_fullscreen.clicked.connect(self.on_fullscreen)

        backend.mplayer.signals.foundAspect.connect(self.setAspect)
        #Backend.mplayer.fileFinished.connect(self.nextClicked)
        #self.mplayer.playbackStarted.connect(self.playbackStarted)
        #self.mplayer.foundAspect.connect(self.setAspect)
        #self.mplayer.foundVolume.connect(self.volumeSlider.setValue)


    def setSize(self, width, height):
        self.video_view.videoWidth = width
        self.video_view.videoHeight = height
        self.video_view.setSize(width, height)
            
    def resizeEvent(self, event):
        self.video_view.aspectResize(event.size().width(), 
                event.size().height())
        if self.moveControls:
            x = self.size().width() / 2 + self.pos().x() - self.ctrl_panel.frameGeometry().width() / 2
            y = self.size().height() + self.pos().y() - self.ctrl_panel.frameGeometry().height() - self.frameHeight
            self.ctrl_panel.move(x, y)
            self.moveControls = False
            
    # def setFullscreen(self):
    #     self.fullscreen=not self.fullscreen
    #
    #     if self.fullscreen:
    #         self.setParent(None)
    #         self.showFullScreen()
    #         self.moveControls = True
    #
    #         self.ctrl_panel.show()
    #         self.controlTimer.start()
    #     else:
    #         self.ctrl_panel.hide()
    #         self.controlTimer.stop()
    #         self.signals.fullscreenDisabled.emit()

    def setFitToWidth(self, fit):
        self.video_view.fitToWidth = fit
        self.video_view.aspectResize(self.width(), self.height())
                  
    def mouseMoveEvent(self, event):
        if self.fullscreen:
            self.ctrl_panel.show()
            self.controlTimer.start()
         
         
    def mouseDoubleClickEvent(self, event):
         self.on_fullscreen()

    def mousePressEvent(self, event):
        #pass
        self.ctrl_panel.hide()

    def keyPressEvent(self,event):
        if not self.fullscreen:
            event.accept
            return

        #if event.key()==Qt.Key_Esc:
        #    self.setFullscreen(False)

        event.accept

    def hideCtrlPanel(self):
        self.ctrl_panel.hide()

    def setAspect(self):
        if backend.mplayer.aspect > .0001:
            self.setSize(backend.mplayer.aspect * 1000, 1000)
            self.resize(1, 1)
            self.resize(self.width(), self.height())


class ZVideoView(QLabel):
    def __init__(self, parent = None):
        QLabel.__init__(self, parent)
        self.videoWidth = 1
        self.videoHeight = 1
        self.fitToWidth = False
        self.setMouseTracking(True)
   
    def setSize(self, width, height):
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.resize(width, height)
      
    def aspectResize(self, width, height):
        if (float(width) / float(height) < float(self.videoWidth) / float(self.videoHeight)) or self.fitToWidth:
            newHeight = int(float(self.videoHeight * width) / self.videoWidth)
            self.setSize(width, newHeight)
            self.move(0, (height - newHeight) / 2)
        else:
            newWidth = int(float(self.videoWidth * height) / self.videoHeight)
            self.setSize(newWidth, height)
            self.move((width - newWidth) / 2, 0)

