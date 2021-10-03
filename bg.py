### bg.py 파일 - 단독 작동하는 백그라운드 실행 파일을 위한 코드이다. ###
#### 이는 offtime-bg-b2ZmdGltZS1iZw.exe 라는 파일로 컴파일한다. ####
### 현재 코드 버전: 0a ###

# 이 코드는 타 모듈 없이 완전히 스스로 동작해야 함.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, Qt

import configparser, os

import datetime, time


########## UI 부분 자동생성 코드 시작 ##########
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
        Dialog.setWindowTitle(_translate("Dialog", "offTime"))
        self.scheduledInfo.setText(_translate("Dialog", "이 PC는 hh시 mm분에 종료되도록 예약되었습니다."))
        self.questionLabel.setText(_translate("Dialog", "종료 예약을 취소하시겠습니까?"))
        self.cancelButton.setText(_translate("Dialog", "예약 취소"))
        self.leftTimeProgressBar.setFormat(_translate("Dialog", "%p초 후 자동 종료"))

    # def closeEvent(self, event):
    # pass


############################################
########### UI 부분 자동생성 코드 끝 ##########
############################################


config = configparser.ConfigParser()


def open_ui(setTime):
    import sys

    # UI 세부 설정
    # 예약 시간 표시
    setTime = setTime + datetime.timedelta(seconds=int(config['ACTIVITY']['notifytime_sec']))
    QsetT = QDateTime.fromString(str(setTime), "yyyy-MM-dd hh:mm:ss")


    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    ui.scheduledInfo.setText(
        "이 PC는 {0}시 {1}분 {2}초에 종료되도록 예약되었습니다.".format(config['TIME']['hour'], config['TIME']['minute'],
                                                      config['TIME']['second']))

    # 남은시간 실시간 업데이트
    def updateProgressBar():
        QnowT = QtCore.QDateTime.currentDateTime()
        Qdiff_msec = QnowT.msecsTo(QsetT)
        # print(QsetT, QnowT, Qdiff_msec)
        Qdiff_sec = Qdiff_msec / 1000
        # timer_init = QtCore.QTimer()
        # timer_init.setInterval(5)
        # timer_init.start()
        ui.leftTimeProgressBar.setFormat("{0}초 후 자동으로 종료됨. ".format(round(Qdiff_sec)))
        if Qdiff_sec > int(config['ACTIVITY']['notifytime_sec']):
            pass
        else:
            ui.leftTimeProgressBar.setProperty("maximum", 10000)
            value = int(Qdiff_msec) / ((int(config['ACTIVITY']['notifytime_sec']) * 1000)) * 10000
            #print(value)
            ui.leftTimeProgressBar.setProperty("value", value)
        #print(Qdiff_sec)
        if 0 <= Qdiff_sec <= 1:
            print("<종료커맨드 발동>")
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

    # 예약취소 버튼 클릭.
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

    # 창 종료 방지
    Dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | QtCore.Qt.Tool)

    Dialog.show()
    sys.exit(app.exec_())


def shutdown_start(setTime):
    # print("종료 {0}초전 창 열림...".format(int(config['ACTIVITY']['notifytime_sec'])))
    open_ui(setTime)


##### 디버그 #####
# setTime = datetime.datetime.now().replace(hour=int(config['TIME']['hour']), minute=int(config['TIME']['minute']), second=0, microsecond=0)
# open_ui(setTime)
#################


def main():
    config.read("offTimeConfig.ini")
    notify_time_sec = int(config['ACTIVITY']['notifytime_sec'])
    now = datetime.datetime.now()
    setTimeOriginal = datetime.datetime.now().replace(hour=int(config['TIME']['hour']),
                                                      minute=int(config['TIME']['minute']),
                                                      second=int(config['TIME']['second']),
                                                      microsecond=0)
    setTime = setTimeOriginal - datetime.timedelta(seconds=notify_time_sec)

    if setTime <= now.replace(microsecond=0) + datetime.timedelta(seconds=1) <= setTime + datetime.timedelta(seconds=notify_time_sec):
        # 예정대로 동작
        if config['ACTIVITY']['Switch'] == '1':
            shutdown_start(setTime)

    while 1:
        config.read("offTimeConfig.ini")
        # setTime은 30초 앞으로 설정한다. (어차피 확인창에서 30초 더 끌 거임. )
        notify_time_sec = int(config['ACTIVITY']['notifytime_sec'])
        setTimeOriginal = datetime.datetime.now().replace(hour=int(config['TIME']['hour']),
                                                          minute=int(config['TIME']['minute']),
                                                          second=int(config['TIME']['second']),
                                                          microsecond=0)
        setTime = setTimeOriginal - datetime.timedelta(seconds=notify_time_sec)

        # 또 예약시간이 이미 지난시간일 경우 다음날 기준으로 바꾼다.
        now = datetime.datetime.now()
        if setTime < now:
            setTime = setTime + datetime.timedelta(days=1)

        # 23:55에서 다음날 0시 사이일 경우 예약시간을 다음날 기준으로 바꾼다.
        if setTime.replace(hour=23, minute=55, second=0, microsecond=0) <= setTime <= setTime.replace(
                hour=setTime.max.hour,
                minute=setTime.max.minute,
                second=setTime.max.second,
                microsecond=setTime.max.microsecond):
            print('ACTIVATED!')
            setTime = setTime + datetime.timedelta(days=1)

        # 지금 시간이 설정된 시간 전이라면

        # <DEBUG>
        print("setTime:", setTime, "now: ", now.replace(microsecond=0))

        if str(now.replace(microsecond=0) + datetime.timedelta(seconds=1)) == str(setTime):
            # 예정대로 동작
            if config['ACTIVITY']['Switch'] == '1':
                shutdown_start(setTime)
                break
        # 아니면
        else:
            pass
        time.sleep(0.5)


main()
