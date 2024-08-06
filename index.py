# NOTE AT the end of app try this from PyQt5 import QtGui,QtCore see if there's a difference in launch time
# importing important modules
from PyQt5.QtWidgets import *
'''contains widgets that we'll use like QPushButton, QApplication'''
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from main import Ui_MainWindow
from os import getcwd,mkdir,chdir,path
import sys
import urllib.request
from pytube import Playlist, YouTube
import humanize

# initializing a class that inherits its parameters and fncs from QMainWindow class
    # takes the variable containing the design as a 2nd parameter
class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.Handel_UI()
        self.Handel_Button()

# International methods
    def Handel_UI(self):
        self.setWindowTitle('MiDO Downloader')
        self.setFixedSize(576,369)

    def Handel_Button(self):
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_5.clicked.connect(self.Handel_browse_video)
        self.pushButton_9.clicked.connect(self.Get_Youtube_Video)
        self.pushButton_6.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_7.clicked.connect(self.Handel_Browse_Playlist)
        self.pushButton_10.clicked.connect(self.Get_playlist)
        self.pushButton_8.clicked.connect(self.Playlist_download)

# NOTE when connecting a funcion with another don't use brackets in the 2nd fn.. just 
# its name inside the 1st fn brackets, otherwise it will raise None Error.

                    # MAIN APP FUNCTIONS
########################### FIRST TAB ##########################
    def Handel_Browse(self):
        save = QFileDialog.getSaveFileName(self, caption='Save as',directory='', filter='All Files (*.*)')
        string = str(save) # because the method above returns a TUPLE! not string
        save_place = string.split("'")[1]
        self.lineEdit_2.setText(save_place)

    def Handel_pregress(self, blocknum, blocksize, totlasize):
        read = blocknum * blocksize
        if totlasize > 0 :
            percent = round(read * 100 / totlasize)
            self.progressBar.setValue(percent)
            QApplication.processEvents()

    def Download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url, save_location, self.Handel_pregress)    
            QMessageBox.information(self, 'Successful !','File Downloaded completed')
        except:
            QMessageBox.warning(self, 'Error :(', 'Download Failed !')

        self.progressBar.setValue(0)
        # self.lineEdit.setText('')
        # self.lineEdit_2.setText('')


####################### YouTube video tab ######################

    def Handel_browse_video(self):
        save = QFileDialog.getExistingDirectory(self, 'Save Video as')
        self.lineEdit_5.setText(save)
        # the difference between this method and the one above in browse getSaveFileName 
        # is that this takes just a path from user and returns a directory, while in the
        # other we could name the file and choose extension.          

    def Get_Youtube_Video(self):
        self.comboBox.clear()
        url = self.lineEdit_6.text()
        v = YouTube(url)
        stream_list = v.streams.desc().filter(subtype='mp4', progressive=True)
        for s in stream_list:
            final = str((s.type, s.subtype,s.resolution, humanize.naturalsize(s.filesize))).replace("'",'')
            self.comboBox.addItem(final)

    def Video_progress(self, chunk, file_handler, bytes_remaining):
        size = chunk.filesize
        downloaded = size - bytes_remaining
        percent = round(downloaded / size *100)
        self.progressBar_2.setValue(percent)
        QApplication.processEvents()

    def Download_Youtube_Video(self):
        url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()
        try:
            v = YouTube(url, on_progress_callback=self.Video_progress)
            stream_list = v.streams.desc().filter(subtype='mp4', progressive=True)
            quality = self.comboBox.currentIndex()
            download = stream_list[quality].download(save_location)

            QMessageBox.information(self, 'Success!','Video Downloaded completed :)')
        except:
            QMessageBox.warning(self, 'Error!', 'Download Failed  :(')
        self.progressBar_2.setValue(0)


############################ Playlist Download #########################

    def Get_playlist(self):
        self.comboBox_2.clear()
        url = self.lineEdit_8.text()
        playlist = Playlist(url)
        video = YouTube(playlist[0])
        stream_list = video.streams.desc().filter(subtype='mp4', progressive=True)
        for s in stream_list:
            final = str((s.type, s.subtype,s.resolution, humanize.naturalsize(s.filesize))).replace("'",'')
            self.comboBox_2.addItem(final)

    def Playlist_download(self):
        url = self.lineEdit_8.text()
        save_location = self.lineEdit_7.text()
        playlist = (Playlist(url))
        quality = self.comboBox_2.currentIndex()
        current_vid_num = 0
        chdir(save_location)
        if path.exists(playlist.title):
            chdir(playlist.title)     
        else:
            mkdir(playlist.title)
            chdir(playlist.title)
        try:
            for video in range(playlist.length):
                v = YouTube(playlist[video])
                stream_list = v.streams.desc().filter(subtype='mp4', progressive=True)
                download = stream_list[quality].download(getcwd())
                current_vid_num += 1
                self.lcdNumber.display(current_vid_num)
                QApplication.processEvents()
            QMessageBox.information(self, 'Success!','Video Downloaded completed :)')
        except:
            QMessageBox.warning(self, 'Error!', 'Download Failed  :(')
    
        self.progressBar_2.setValue(0)
        self.lcdNumber.display(0)

    def Handel_Browse_Playlist(self):
        save = QFileDialog.getExistingDirectory(self, 'Save Playlist as')
        self.lineEdit_7.setText(save)

# creating the main app function 
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()
    '''creating an object (instance) of MainApp class
        To show the app window
        the app stays open (making an infinite loop)'''

# App will start from here (main()fundtion)
if __name__ == '__main__':
    main()