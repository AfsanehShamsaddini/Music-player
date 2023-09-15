import time
from PyQt5.QtCore import QTimer
from mutagen.mp3 import MP3
from pygame import mixer
from  PyQt5.QtWidgets import  QMainWindow, QApplication,QLabel,QPushButton,QMenu,QMenuBar,QFileDialog,QListWidget,QSlider
from PyQt5 import uic,QtGui
import sys
mixer.init()
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('player.ui',self)
        self.list_of_music= self.findChild(QListWidget,"list_music")
        self.music_position = self.findChild(QSlider,"music_position")
        self.volume = self.findChild(QSlider, "volume")
        self.forward = self.findChild(QPushButton, "forward")
        self.back = self.findChild(QPushButton, "back")
        self.play = self.findChild(QPushButton,"play")
        self.stop = self.findChild(QPushButton, "stop")
        self.pause = self.findChild(QPushButton, "pause")
        self.pushButton_6 = self.findChild(QPushButton, "pushButton_6")

        self.img = self.findChild(QPushButton, "img")
        self.end_time = self.findChild(QLabel, "end_time")
        self.start_time = self.findChild(QLabel, "start_time")

        self.show()
        self.stopped = False
        self.musiclist = []
        self.paused = False
        self.song_length = 0
        self.actionOpen.triggered.connect(self.open_file)
        self.actionDelete_music.triggered.connect(self. delete_song)
        self.actionClear_all.triggered.connect(self. delete_all_song)

        self.play.clicked.connect(self.play_music)
        self.stop.clicked.connect(self.stop_music)
        self.pause.clicked.connect(self.pause_music)
        self.forward.clicked.connect(self.forward_music)
        self.back.clicked.connect(self.back_music)
        self.count = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateslider)
        self.volume.setMinimum(0)
        self.volume.setMaximum(100)
        self.volume.setValue(70)
        mixer.music.set_volume(0.5)
        self.volume.valueChanged.connect(self.setvolume)
        #self.music_position.valueChanged.connect(self.get_position)


    def open_file(self):
        songs, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", "Audio Files *.mp3 *.m4a *.ogg *.wav *.m3u")
        for song in  songs:
            self.musiclist.append(song)
            song = song.split('/')[-1]
            self.list_of_music.addItem(song)

    def updateslider(self):
        self.count += 1
        self.music_position.setValue(int(self.count))
        self.start_time.setText(time.strftime("%M:%S", time.gmtime(self.count)))
        if self.count == self.song_length:
            self.music_position.setValue(0)
            self.count = 0
            self.timer.stop()
            self.stop_music()

    def play_music(self):
        self.music_position.setValue(0)
        self.count = 0
        self.stopped = False
        index = self.list_of_music.currentRow()
        mixer.music.load(str(self.musiclist[index]))
        mixer.music.play()
        self.timer.start()
        song = str(self.musiclist[index])
        song_mute = MP3(song)
        self.song_length = song_mute.info.length
        self.song_length = round(self.song_length)
        converted_song_length = time.strftime("%M:%S", time.gmtime(self.song_length))
        self.end_time.setText(converted_song_length)
        self.music_position.setMaximum(self.song_length)

    def stop_music(self):
        mixer.music.stop()
        self.timer.stop()
        self.count = 0
        self.music_position.setValue(self.count)
    def pause_music(self):
        if self.paused:
            mixer.music.unpause()
            self.paused = False
            self.timer.start()
            self.count = self.music_position.value()
            self.music_position.setValue(self.count)
        else:
            mixer.music.pause()
            self.paused = True
            self.timer.stop()
            self.count = self.music_position.value()
            self.music_position.setValue(self.count)

    def forward_music(self):
        index = self.list_of_music.currentRow()
        if index == len(self.list_of_music) - 1:
            index = 0
        else:
            index += 1
        self.list_of_music.setCurrentRow(index)
        mixer.music.load(str(self.musiclist[index]))
        mixer.music.play()

    def back_music(self):
        index = self.list_of_music.currentRow()
        if index == 0:
            index = len(self.list_of_music) - 1
        else:
            index -= 1
        self.list_of_music.setCurrentRow(index)
        mixer.music.load(str(self.musiclist[index]))
        mixer.music.play()
    def setvolume(self):
        volume1 = self.volume.value()
        mixer.music.set_volume(volume1 / 100)
        current_volume = self.volume.value()
        print(current_volume)

        if int(current_volume) < 1:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("icon/volume1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_6.setIcon(icon2)
        elif int(current_volume) >= 1 and int(current_volume) <= 25:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("icon/volume3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_6.setIcon(icon2)
        elif int(current_volume) >= 25 and int(current_volume) <= 75:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("icon/volume3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_6.setIcon(icon2)
        elif int(current_volume) >= 75 and int(current_volume) <= 100:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("icon/volume4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_6.setIcon(icon2)

    def delete_song(self):
        self.stop_music()
        # Delete currently select song
        clicked = self.list_of_music.currentRow()
        self.list_of_music.takeItem(clicked)
        self.musiclist.pop(clicked)
        print(self.musiclist)
        mixer.music.stop()

    # Delete All song
    def delete_all_song(self):
        self.stop_music()
        # Delete all select song
        self.list_of_music.clear()
        self.musiclist = []
        self.paused = False
        mixer.music.stop()
    def get_position(self):
        index = self.list_of_music.currentRow()
        song = mixer.music.load(str(self.musiclist[index]))
        mixer.music.load(song)
        mixer.music.play(loops=0, start=int(  self.music_position.value()))
if __name__ == '__main__':

    app=QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

