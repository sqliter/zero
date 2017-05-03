#coding=utf-8
from PySide.QtGui import *
from PySide.QtCore import *
from video_view import ZVideoWidget
from playlist_widget import ZPlayListWidget
from ctrl_panel import ZCtrlPanel
import backend
import os
from zmplayer import ZMPlayer
import logging

class ZMainWindow(QMainWindow):

    def __init__(self):
        super(ZMainWindow,self).__init__()

        self.init_actions()
        self.init_menubar()
        self.init_sidebar()

        self.playpane=ZCtrlPanel()
        self.playpane.btn_fullscreen.clicked.connect(self.on_fullscreen)

        self.main_view=QWidget()

        self.splitter=QSplitter()

        self.content_view=QStackedWidget()
        self.video_widget=ZVideoWidget(self.on_fullscreen)
        # self.video_widget.signals.fullscreenDisabled.connect(
        #         self.on_exit_fullscreen)
        self.content_view.addWidget(self.video_widget)

        self.list_widget=ZPlayListWidget()
        self.content_view.addWidget(self.list_widget)

        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.content_view)
        self.splitter.setStretchFactor(0,0)
        self.splitter.setStretchFactor(1,1)
        self.sidebar.setMinimumWidth(180)

        vbox=QVBoxLayout()
        vbox.addWidget(self.splitter,1)
        vbox.addWidget(self.playpane)

        self.main_view.setLayout(vbox)

        self.setCentralWidget(self.main_view)
        self.resize(1024,600)
        self.setWindowTitle(self.tr('zero online media player'))

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_update)
        self.currentTime = 0

        self.init_mplayer()

        self.show()

    def closeEvent(self,event):
        logging.debug("closeEvent")
        # Check that mplayer is ended
        backend.mplayer.end()
        event.accept()

    def init_mplayer(self):
        # self.mplayer.signals.fileFinished.connect(self.on_last)
        # self.mplayer.signals.playbackStarted.connect(self.playbackStarted)
        # self.mplayer.signals.foundAspect.connect(self.setAspect)
        # self.mplayer.signals.foundVolume.connect(self.volumeSlider.setValue)
        backend.mplayer.set_render_wid(self.video_widget.video_view.winId())
        #backend.mplayer.process.finished.connect(self.sync_with_mplayer)
        #backend.mplayer.signals.fullscreenChanged.connect(self.on_fullscreen)
        self.player=ZMPlayer()
        self.player.set_render_wid(self.video_widget.video_view.winId())
    def init_actions(self):
        #video menu
        self.open_act=QAction(QIcon('./icon/open.svg'),
                self.tr('open'),self)
        self.open_act.triggered.connect(self.on_open)

        self.options_act=QAction(QIcon('./icon/setting16.svg'),
                self.tr('options'),self)
        self.options_act.triggered.connect(self.on_options)

        self.exit_act=QAction(QIcon('./icon/exit16.svg'),
                self.tr('exit'),self)
        self.exit_act.triggered.connect(self.on_exit)
        #view menu
        self.sidebar_act=QAction(self.tr('show sidebar'),self)
        self.sidebar_act.triggered.connect(self.on_sidebar)
        
        #self.playlist_act=QAction(self.tr('play list'),self)
        #self.playlist_act.triggered.connect(self.on_playlist)

        self.fullscreen_act=QAction(QIcon('./icon/fullscreen.svg'),
                self.tr('fullscreen'),self)
        self.fullscreen_act.triggered.connect(self.on_fullscreen)

        #help menu
        self.about_act=QAction(QIcon(''),self.tr('about'),self)
        self.about_act.triggered.connect(self.on_about)

    def init_menubar(self):
        menubar=self.menuBar()

        self.video_menu=menubar.addMenu(self.tr('video'))
        self.video_menu.addAction(self.open_act)
        self.video_menu.addSeparator()
        self.video_menu.addAction(self.options_act)
        self.video_menu.addSeparator()
        self.video_menu.addAction(self.exit_act)

        self.view_menu=menubar.addMenu(self.tr('view'))
        self.view_menu.addAction(self.fullscreen_act)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.sidebar_act)

        self.help_menu=menubar.addMenu(self.tr('help'))
        self.help_menu.addAction(self.about_act)

    def init_sidebar(self):
        self.sidebar=QTabWidget()
        
        #self.category_view=QTreeWidget()
        #self.sidebar.addTab(self.category_view,
        #        self.tr('category'))

        self.soku_view=QWidget()
        self.txt_key=QLineEdit()
        self.btn_search=QPushButton(self.tr('search'))
        self.btn_search.clicked.connect(self.on_soku_search)
        self.list_result=QListWidget()

        hbox=QHBoxLayout()
        hbox.addWidget(self.txt_key,1)
        hbox.addWidget(self.btn_search)
        vbox=QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.list_result,1)
        self.soku_view.setLayout(vbox)

        self.sidebar.addTab(self.soku_view,self.tr('soku'))
        
        self.local_view=QTreeWidget()
        self.local_view.setHeaderLabel(self.tr('my videos'))
        self.sidebar.addTab(self.local_view,self.tr('local'))

        self.playlist_view=QListWidget()
        self.playlist_view.addItem('playing list')
        self.playlist_view.currentRowChanged.connect(self.show_playlist_details)
        self.sidebar.addTab(self.playlist_view,self.tr('playlist'))

    # def sync_with_mplayer(self):
    #     if os.name=='nt':
    #         pass
    #     else:
    #         logging.debug('sync_with_mplayer')
    #         if backend.mplayer.playing:
    #             if backend.mplayer.inPlayback:
    #                 self.timer.start()
    #             self.btn_play.setIcon(QIcon('./icon/pause.svg'))
    #         else:
    #             self.timer.stop()
    #             self.btn_play.setIcon(QIcon('./icon/play.svg'))

            
    def on_video_keyevents(self):
        pass

    def on_open(self):
        qfilename,ok=QFileDialog.getOpenFileName(self,
                self.tr('get open video file'))

        self.video_file=qfilename
        print self.video_file
        backend.mplayer.loadFile(qfilename.encode('utf-8'))
        #self.player.loadFile(qfilename.encode('utf-8'))

    def on_options(self):
        pass

    def on_exit(self):
        pass

    def on_fullscreen(self):
        self.video_widget.fullscreen=not self.video_widget.fullscreen

        if self.video_widget.fullscreen:
            self.content_view.removeWidget(self.video_widget)
            self.video_widget.setParent(None)
            self.video_widget.showFullScreen()
            self.video_widget.moveControls = True

            self.video_widget.ctrl_panel.show()
            self.video_widget.controlTimer.start()
        else:
            self.video_widget.ctrl_panel.hide()
            self.video_widget.controlTimer.stop()
            #self.signals.fullscreenDisabled.emit()
            self.video_widget.hide()
            self.content_view.addWidget(self.video_widget)
            #self.video_widget.showNormal()
            self.content_view.setCurrentWidget(self.video_widget)
        #self.video_widget.setFullscreen()

    # def on_exit_fullscreen(self):
    #     self.video_widget.hide()
    #     self.video_widget.setParent(self.content_view)
    #     #self.content_view.addWidget(self.video_widget)
    #     self.video_widget.showNormal()
    #     self.content_view.setCurrentWidget(self.video_widget)

    def on_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def on_about(self):
        pass

    def on_soku_search(self):
        pass

    def timer_update(self):
        logging.debug("timer_update")
        self.currentTime += 1
        self.disableSeek = True
        # if self.currentTime > self.mplayer.length:
        #     self.mplayer.length = self.currentTime
        #     self.timeSlider.setMaximum(self.mplayer.length)
        #     self.videoOutput.controls.timeSlider.setMaximum(self.mplayer.length)
        #
        # if not self.timeSlider.isSliderDown() and not self.videoOutput.controls.timeSlider.isSliderDown():
        #     self.fillTimeLabel()
        #     self.timeSlider.setValue(self.currentTime)
        #     self.videoOutput.controls.timeSlider.setValue(self.currentTime)
        self.disableSeek = False

    def show_playlist_details(self):
        self.playlist_view