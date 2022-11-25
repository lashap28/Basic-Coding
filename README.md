# Basic-Coding

import os
import random
import numpy as np
import torchaudio
import torch.nn as nn
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import datetime
from datetime import date

global_root = r'Z:/data_science/VoiceDataLabeling'
username = os.getlogin().lower()

dd = {'achakhnashvili': 'ავთო',
      'aksovreli': 'აჩი',
      'dkatsobashvili': 'კაცობ',
      'ggorgadze': 'გაბრიელ',
      'gmekhrishvili': 'გიგა',
      'gjavakhidze': 'გიზო',
      'ibareladze': 'ევროპალიგა',
      'ilatauri': 'ილია',
      'ljavelidze': 'ლიზა',
      'lpantskhava': 'ფაშა',
      'mnazgaidze': 'მიშო',
      'nabazadze': 'ვამეხი',
      'sgogichaishvili': 'საბლო',
      'vochigava': 'ვასო',
      'tkipshidze': 'თინი',
      'djokhadze': 'დათიკო',
      'gigotsiridze': 'გიიიგა',
      'tamazlezhava': 'თაზო 3-1',
      }


class Ui_MainWindow(object):
    def __init__(self):
        self.voicename = None
        self.f_path = os.path.join(global_root, 'AudioChunksMapped')
        self.ll = None
        self.player = QMediaPlayer()
        self.ind = 0
        self.num_lim = 180
        self.td_result = 0
        self.cur_date = date.today()
        self.upath = os.path.join(global_root, 'labeled_files', username).replace("\\", "/")
        self._translate = QtCore.QCoreApplication.translate
        for i in os.listdir(self.upath):
            if date.fromtimestamp(os.path.getmtime(self.upath + '/' + i)) == date.today():
                self.td_result += 1

    def setupUi(self, MainWindow):
        with open(os.path.join(global_root, 'AudioMapped.txt'), 'r') as f:
            all_audio = f.readlines()
        self.all_audio = set(all_audio[0].split('/&/'))

        if os.path.exists(os.path.join(global_root, 'doneVoicesMapped.txt')):
            with open(os.path.join(global_root, "doneVoicesMapped.txt"), 'r') as f:
                lines = f.readlines()
            lines = lines[0].split('/&/')[:-1]

            self.ll = list(self.all_audio - set(lines))
            random.shuffle(self.ll)
        else:
            self.ll = os.listdir(self.f_path)
            random.shuffle(self.ll)

        MainWindow.setObjectName("VoiceLabler")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditPressEvent = self.lineEdit.keyPressEvent
        self.lineEdit.keyPressEvent = self.keyPressEvent
        self.lineEdit.setGeometry(QtCore.QRect(30, 310, 750, 90))
        f = self.lineEdit.font()
        f.setPointSize(12)
        self.lineEdit.setFont(f)
        self.lineEdit.setObjectName("lineEdit")




        self.SaveNextButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveNextButton.keyPressEvent = self.enterPressSaveNext
        self.SaveNextButton.setGeometry(QtCore.QRect(170, 420, 451, 71))
        self.SaveNextButton.clicked.connect(self.label_and_next)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.SaveNextButton.setFont(font)
        self.SaveNextButton.setObjectName("SaveNextButton")




        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(0,0,0,0))
        # self.SaveButton.clicked.connect(self.LabelAudio)
        # font = QtGui.QFont()
        # font.setPointSize(18)
        # font.setBold(True)
        # font.setWeight(75)
        # self.SaveButton.setFont(font)
        self.SaveButton.setObjectName("SaveButton")





        self.Next = QtWidgets.QPushButton(self.centralwidget)
        self.Next.setGeometry(QtCore.QRect(0, 0, 0, 0))
        # self.Next.clicked.connect(self.NextAudio)
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # font.setBold(True)
        # font.setWeight(75)
        # self.Next.setFont(font)
        self.Next.setObjectName("Next")

        self.AudioCount = QtWidgets.QLabel(self.centralwidget)
        self.AudioCount.setGeometry(QtCore.QRect(230, 60, 300, 40))
        self.AudioCount.setAlignment(Qt.AlignCenter)
        self.AudioCount.setStyleSheet("background-color: lightblue")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AudioCount.setFont(font)
        self.AudioCount.setObjectName("label")
        _translate = QtCore.QCoreApplication.translate
        self.AudioCount.setText(_translate("MainWindow", f"გამარჯობა {dd[username]}"))

        self.AudioCount = QtWidgets.QLabel(self.centralwidget)
        self.AudioCount.setGeometry(QtCore.QRect(160, 120, 450, 40))
        self.AudioCount.setAlignment(Qt.AlignCenter)
        self.AudioCount.setStyleSheet("background-color: lightblue")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AudioCount.setFont(font)
        self.AudioCount.setObjectName("label")
        _translate = QtCore.QCoreApplication.translate
        self.AudioCount.setText(_translate("MainWindow", f"{self.ll[0]} "))

        self.AudioCount1 = QtWidgets.QLabel(self.centralwidget)
        self.AudioCount1.setGeometry(QtCore.QRect(250, 260, 250, 40))
        self.AudioCount1.setAlignment(Qt.AlignCenter)
        # self.AudioCount1.setStyleSheet("background-color: lightblue")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(45)
        self.AudioCount1.setFont(font)
        self.AudioCount1.setObjectName("label")
        _translate = QtCore.QCoreApplication.translate
        self.AudioCount1.setText(_translate("MainWindow", f"Today's Progress: {self.td_result} / {self.num_lim}"))

        self.Play = QtWidgets.QPushButton(self.centralwidget)
        self.Play.setGeometry(QtCore.QRect(120, 260, 120, 40))
        self.Play.clicked.connect(self.playAudioFile)
        self.Play.keyPressEvent = self.enterPressPlay
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Play.setFont(font)
        self.Play.setObjectName("Play")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        if not os.path.exists(os.path.join(global_root, 'labeled_files', username)):
            os.mkdir(os.path.join(global_root, 'labeled_files', username))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VoiceLabler"))
        self.SaveButton.setText(_translate("MainWindow", "Save"))
        self.SaveNextButton.setText(_translate("MainWindow", "Save and Next"))
        self.Next.setText(_translate("MainWindow", "Next"))
        self.Play.setText(_translate("MainWindow", "Play"))

    def playAudioFile(self):
        full_file_path = os.path.join(self.f_path, self.ll[0])
        self.voicename = self.ll[0]
        print(self.ll[0])
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.Next.setDisabled(True)
        self.player.setMedia(content)
        self.player.play()
        self.lineEdit.setFocus()

    def NextAudio(self):

        with open(os.path.join(global_root, "doneVoicesMapped.txt"), 'r') as f:
            lines = f.readlines()
        lines = lines[0].split('/&/')[:-1]

        self.ll = list(self.all_audio - set(lines))
        random.shuffle(self.ll)

        if len(self.ll) is None:
            print("All is Labeled")

        self.AudioCount.setText(self._translate("MainWindow", f"{self.ll[0]} "))
        self.lineEdit.clear()
        self.SaveButton.setEnabled(True)
        self.SaveNextButton.setEnabled(True)
        self.Play.setEnabled(True)
        self.playAudioFile()


    def LabelAudio(self):
        if len(self.lineEdit.text()) > 0:
            wave, samplerate = torchaudio.load(os.path.join(self.f_path, self.ll[0]))
            self.Next.setEnabled(True)
            lbl = self.lineEdit.text()
            llist = list([wave[0].tolist(), samplerate, lbl, self.ll[0].replace('.wav', '')])
            print(os.path.join(self.f_path, self.ll[0]))
            np.save(os.path.join(global_root, 'labeled_files', username, self.ll[0].replace('wav', 'npy')),
                    llist,
                    allow_pickle=True)

            self.AudioCount.setText("შენახულია, მადლობა!!!")
            self.SaveButton.setEnabled(False)
            self.Play.setEnabled(False)
            self.SaveNextButton.setEnabled(False)

            with open(os.path.join(global_root, "doneVoicesMapped.txt"), 'a') as f:
                f.writelines(self.voicename + "/&/")

            if self.cur_date != date.today():
                self.cur_date = date.today()
                self.td_result = 0
            self.td_result += 1
            self.AudioCount1.setText(self._translate("MainWindow", f"Today's limit: {self.td_result}/{self.num_lim}"))

        else:
            self.AudioCount.setText("დაამატე ტექსტი!!!")


    def label_and_next(self):
        if len(self.lineEdit.text()) > 0:
	        self.LabelAudio()
	        self.NextAudio()
        else:
            self.AudioCount.setText("დაამატე ტექსტი!!!")



    def enterPressSaveNext(self, e):
        if e.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.label_and_next()
        print (self.lineEdit.keyPressEvent)

    def enterPressPlay(self, e):
        if e.modifiers() & Qt.ControlModifier:
            self.keyPressEvent(e)
        elif e.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.playAudioFile()


    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            if e.key() == Qt.Key_P:
                self.playAudioFile()
            elif e.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter, QtCore.Qt.Key_S):
                self.label_and_next()
            else:
                self.lineEditPressEvent(e)
        else:
            self.lineEditPressEvent(e)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.playAudioFile()
    sys.exit(app.exec_())

