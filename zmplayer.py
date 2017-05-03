# -*- coding: utf-8 -*-

from PySide import QtCore
import time, sys, os

class ZMPlayerSignals(QtCore.QObject):
    fileFinished=QtCore.Signal()
    playbackStarted=QtCore.Signal()
    foundAspect=QtCore.Signal()
    foundVolume=QtCore.Signal(int)
    fullscreenChanged=QtCore.Signal()

class ZMPlayer(QtCore.QObject):
    @staticmethod
    def formatTime(time):
        hours = time / 3600
        tempTime = time - hours * 3600
        minutes = tempTime / 60
        seconds = tempTime - minutes * 60
        if hours > 0:
            return '%s:%s:%s' % (str(hours),
                    str(minutes).zfill(2),
                    str(seconds).zfill(2))
        else:
            return '%s:%s' % (str(minutes).zfill(2),
                    str(seconds).zfill(2))

    def __init__(self, extraOptions = ""):
        QtCore.QObject.__init__(self)

        self.signals=ZMPlayerSignals() 

        self.extraOptions = extraOptions
        self.clear()
        self.render_wid = ''
        self.filelist= []
        self.current_index=0
        self.in_fullscreen = False
        self.logWidget = None
        self.lastVolume = time.time()

        self.process = QtCore.QProcess()
        self.process.readyReadStandardOutput.connect(self.readStdout)
        self.process.finished.connect(self.finished)
        #self.ensureRunning()
      
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.getVolume)
        # self.timer.timeout.connect(self.checkEOF)
        # self.timer.start()

    def clear(self):
        self.filename = ""
        self.playing = True  # It appears that MPlayer starts unpaused even if you don't give it a filename to play
        self.inPlayback = False
        self.title = "n/a"
        self.album = "n/a"
        self.artist = "n/a"
        self.length = 0
        self.seekScale = 1
        self.pending = 0
        self.aspect = 0


    def set_render_wid(self,wid):
        if os.name == 'nt':
            self.render_wid = str(int(wid))
        else:
            self.render_wid = str(wid)

    def append_to_list(self,filename):
        self.filelist.append(filename)

    def remove_from_list(self,filename):
        self.filelist.remove(filename)

    def play(self):
        if self.filename == "" or not self.inPlayback:
            return

        self.process.write("pause\n")
        self.playing = not self.playing

    def prev(self):
        if len(self.filelist)<=0:
            return

        self.current_index = self.current_index - 1
        if self.current_index < 0:
            self.current_index = 0
        filename=self.filelist[self.current_index]
        self.loadFile(filename)

    def next(self):
        if len(self.filelist)<=0:
            return

        self.current_index = self.current_index + 1
        if self.current_index>=len(self.filelist):
            self.current_index= len(self.filelist)-1
        filename=self.filelist[self.current_index]
        self.loadFile(filename)

    def loadFile(self, filename):
        self.clear()
        if filename != "":
            self.ensureRunning()
            self.filename = filename
            self.title = os.path.basename(filename)
            self.pending += 1
         
            escapedFilename = filename.replace("\"", "\\\"")
            escapedFilename = escapedFilename.replace("\\", "\\\\")
            self.process.write("loadfile \"" + escapedFilename + "\"\n")

        else:
            self.end()
            self.playing = False

    def ensureRunning(self):
        wid=self.render_wid

        fullCommand = "mplayer -slave -idle -identify -quiet -input nodefault-bindings:conf=" + os.devnull + " -wid " + wid + " " + self.extraOptions
        if self.process.state() == QtCore.QProcess.NotRunning:
            if self.logWidget:
                self.logWidget.append("MPlayer Command: " + fullCommand)
            self.process.start(fullCommand)


    def end(self):
        self.process.terminate()
        time.sleep(1)
        self.process.kill()
        time.sleep(.1)


    def seek(self, position):
        adjustedPosition = int(float(position) / self.seekScale)
        self.process.write("pausing_keep_force seek " + str(adjustedPosition) + " 2\n")


    def readStdout(self):
        lines = self.process.readAllStandardOutput().data().splitlines()
        for line in lines:
            # Don't spam the console with ANS_volume lines (we query it frequently)
            if line.find("ANS_volume=") != -1:
                self.lastVolume = time.time()
                self.signals.foundVolume.emit(int(float(line[11:])))
                continue
         
            # Don't really want to see these messages either
            if line.find("ANS_ERROR=PROPERTY_UNAVAILABLE") != -1 and self.inPlayback:
                self.eof()
                continue
            
            print "MPlayer:", line
            if self.logWidget:
                self.logWidget.append("MPlayer: " + line)
            
            if line.find("Starting playback...") != -1:
                #self.timer.start() # Do this before setting inPlayback to eliminate any chance of a race condition
                self.lastVolume = time.time() # Ditto
                self.inPlayback = True
                #self.signals.playbackStarted.emit()

            foundTitle=''

            if line.find("Title: ") != -1:
                foundTitle = line[8:]
            if foundTitle != "":
                self.title = foundTitle
            print "Found title:", self.title

            foundName=''
            if line.find("Name: ") != -1:
                foundName = line[7:]
            if foundName != "":
                self.title = foundName
            print "Found name:", self.title

            foundArtist=''
            if line.find("Artist:") != -1:
                foundArtist = line[9:]
            if foundArtist != "":
                self.artist = foundArtist
            print "Found artist:", self.artist

            foundAlbum=''
            if line.find("Album:") != -1:
                foundAlbum = line[8:]
            if foundAlbum != "":
                self.album = foundAlbum
            print "Found album:", self.album

            if line.find("ID_LENGTH=") != -1:
                self.length = int(float(line[10:]))
                print "Found length:", self.formattedTime()

            if line.find("ID_VIDEO_WIDTH") != -1:
                self.width = int(line[15:])

            if line.find("ID_VIDEO_HEIGHT") != -1:
                self.height = int(line[16:])
                #self.signals.foundVideo.emit()

            if line.find("ID_VIDEO_ASPECT") != -1:
                print line[16:]
                self.aspect = float(line[16:])
                self.signals.foundAspect.emit()

            sys.stdout.flush()


    def formattedTime(self, time = None):
        if time == None:
            time = self.length
        return ZMPlayer.formatTime(time)


    def finished(self):
        self.clear()
        self.playing = False


    def fullscreen(self):
        self.in_fullscreen=not self.in_fullscreen

        if self.in_fullscreen:
            self.process.write("pausing_keep_force vo_fullscreen 1\n")
        else:
            self.process.write("pausing_keep_force vo_fullscreen 0\n")

        self.signals.fullscreenChanged.emit()

    def restart(self):
        self.end()
        self.clear()
        # This call doesn't seem to work right in QT 4.6.2 - the process state is never updated
        # Fortunately, MPlayer will be restarted the next time a file is played anyway
        self.ensureRunning()


    def setVolume(self, vol):
        self.process.write("pausing_keep_force volume " + str(vol) + " 1\n")
      
      
    def getVolume(self):
        # This only works when we're playing
        if self.inPlayback:
            self.process.write("pausing_keep_force get_property volume\n")
         
         
    def checkEOF(self):
        # Check if we got a volume value recently.  Once the file ends we stop getting them.
        # This is for older versions of MPlayer where we don't get an error message back when we query
        # the volume after the file has ended.
        if time.time() - self.lastVolume > 3 and self.inPlayback:
            self.eof()
         
    def eof(self):
        print "End of file"
        self.inPlayback = False
        self.pending -= 1
        if self.pending < 1:
            self.filename = ""
            self.fileFinished.emit()

