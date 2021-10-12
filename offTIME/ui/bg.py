# compile this to exe as offtime-bg-b2ZmdGltZS1iZw.exe
# ver: 0a

# this is an independently-compiled and running code.

import configparser
import datetime
import os
import time
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, Qt


########## UI auto generated code ##########
############################################

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(360, 100))
        Dialog.setMaximumSize(QtCore.QSize(360, 100))
        Dialog.setBaseSize(QtCore.QSize(360, 100))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        Dialog.setFont(font)
        Dialog.setAutoFillBackground(False)
        self.scheduledInfo = QtWidgets.QLabel(Dialog)
        self.scheduledInfo.setGeometry(QtCore.QRect(10, 10, 321, 16))
        self.scheduledInfo.setWordWrap(True)
        self.scheduledInfo.setObjectName("scheduledInfo")
        self.questionLabel = QtWidgets.QLabel(Dialog)
        self.questionLabel.setGeometry(QtCore.QRect(10, 30, 271, 16))
        self.questionLabel.setWordWrap(True)
        self.questionLabel.setObjectName("questionLabel")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(280, 70, 71, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.leftTimeProgressBar = QtWidgets.QProgressBar(Dialog)
        self.leftTimeProgressBar.setGeometry(QtCore.QRect(10, 49, 341, 16))
        self.leftTimeProgressBar.setProperty("value", 5)
        self.leftTimeProgressBar.setProperty("maximum", 00)
        self.leftTimeProgressBar.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.leftTimeProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.leftTimeProgressBar.setInvertedAppearance(False)
        self.leftTimeProgressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.leftTimeProgressBar.setObjectName("leftTimeProgressBar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "offTIME 예약 종료 안내창"))
        self.scheduledInfo.setText(_translate("Dialog", "이 PC는 hh시 mm분에 종료되도록 예약되었습니다."))
        self.questionLabel.setText(_translate("Dialog", "종료 예약을 취소하시겠습니까?"))
        self.cancelButton.setText(_translate("Dialog", "예약 취소"))
        self.leftTimeProgressBar.setFormat(_translate("Dialog", "%p초 후 자동 종료"))

    # def closeEvent(self, event):
    # pass


############################################
######### UI autogenerated code end ########
############################################


config = configparser.ConfigParser()
config.read("offTimeConfig.ini", encoding='utf-8')


def open_ui(setTime):
    import sys

    # UI Details
    # set time display
    setTime = setTime + datetime.timedelta(seconds=int(config['ACTIVITY']['notifytime_sec']))
    QsetT = QDateTime.fromString(str(setTime), "yyyy-MM-dd hh:mm:ss")

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    ui.scheduledInfo.setText(
        "이 PC는 {0}시 {1}분 {2}초에 종료되도록 예약되었습니다.".format(config['TIME']['hour'], config['TIME']['minute'],
                                                      config['TIME']['second']))

    # live update of left time
    def updateProgressBar():
        QnowT = QtCore.QDateTime.currentDateTime()
        Qdiff_msec = QnowT.msecsTo(QsetT)
        Qdiff_sec = Qdiff_msec / 1000
        ui.leftTimeProgressBar.setFormat("{0}초 후 자동으로 종료됨. ".format(round(Qdiff_sec)))
        if Qdiff_sec > int(config['ACTIVITY']['notifytime_sec']):
            pass
        else:
            ui.leftTimeProgressBar.setProperty("maximum", 10000)
            value = 10000 - (int(Qdiff_msec) / ((int(config['ACTIVITY']['notifytime_sec']) * 1000)) * 10000)
            ui.leftTimeProgressBar.setProperty("value", value)
        if 0 <= Qdiff_sec <= 1:
            try:
                if config['ACTIVITY']['killswitch'] == '1':
                    print('<Killswitch Acitvated>')
                else:
                    raise KeyError()
            except:
                print('shutdown')
                os.system('shutdown -s -f -t 0')
            exit()

    timer = QtCore.QTimer()
    timer.setInterval(500)
    timer.timeout.connect(updateProgressBar)
    timer.start()

    # when cancel button clicked
    def cancelled():
        exit()

    if config['ACTIVITY']['enablecancel'] == '1':
        ui.cancelButton.setEnabled(True)
        ui.cancelButton.clicked.connect(cancelled)
    elif config['ACTIVITY']['enablecancel'] == '0':
        ui.cancelButton.setDisabled(True)
        ui.questionLabel.setText("이는 취소할 수 없으므로, 작업을 저장하세요.")
        ui.questionLabel.setStyleSheet("Color : red")
    else:
        raise ValueError()

    # Prevent window close
    Dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | QtCore.Qt.Tool | Qt.WindowTitleHint)
    Dialog.setWindowOpacity(70)

    Dialog.show()
    sys.exit(app.exec_())


def shutdown_start(setTime):
    open_ui(setTime)


def main():
    try:
        os.chdir(sys._MEIPASS)
        print(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())

    config.read("offTimeConfig.ini", encoding='utf-8')
    notify_time_sec = int(config['ACTIVITY']['notifytime_sec'])
    print(notify_time_sec)
    now = datetime.datetime.now()
    setTimeOriginal = datetime.datetime.now().replace(hour=int(config['TIME']['hour']),
                                                      minute=int(config['TIME']['minute']),
                                                      second=int(config['TIME']['second']),
                                                      microsecond=0)
    setTime = setTimeOriginal - datetime.timedelta(seconds=notify_time_sec)

    if setTime <= now.replace(microsecond=0) + datetime.timedelta(seconds=1) <= setTime + datetime.timedelta(
            seconds=notify_time_sec):
        # shutdown process activates
        if config['ACTIVITY']['Switch'] == '1':
            shutdown_start(setTime)

    while 1:
        config.read("offTimeConfig.ini", encoding='utf-8')
        # the 'activating' set time should be 'real' set time minus the notify_time
        notify_time_sec = int(config['ACTIVITY']['notifytime_sec'])
        setTimeOriginal = datetime.datetime.now().replace(hour=int(config['TIME']['hour']),
                                                          minute=int(config['TIME']['minute']),
                                                          second=int(config['TIME']['second']),
                                                          microsecond=0)
        setTime = setTimeOriginal - datetime.timedelta(seconds=notify_time_sec)

        # when set time is already passed, consider it to be tomorrow's time
        now = datetime.datetime.now()
        if setTime < now:
            setTime = setTime + datetime.timedelta(days=1)

        # when 'activating' set time is between 23:55 and 00:00, the 'real' set time should be considered as tomorrow
        if setTime.replace(hour=23, minute=55, second=0, microsecond=0) <= setTime <= setTime.replace(
                hour=setTime.max.hour,
                minute=setTime.max.minute,
                second=setTime.max.second,
                microsecond=setTime.max.microsecond):
            print('ACTIVATED!')
            setTime = setTime + datetime.timedelta(days=1)

        if str(now.replace(microsecond=0) + datetime.timedelta(seconds=1)) == str(setTime):
            # when time has reached
            if config['ACTIVITY']['Switch'] == '1':
                shutdown_start(setTime)
                break
        # else just wait
        else:
            pass
        time.sleep(0.5)


main()