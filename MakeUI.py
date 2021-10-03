from datetime import datetime
import os, sys, configparser, subprocess
from collections import OrderedDict

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic

import resources_rc, random
from modules import *

password = "1234"


# UI 파일 불러오기


mainAppUI = uic.loadUiType("mainapp.ui")[0]
advancedSettingsUI = uic.loadUiType("advanced_settings.ui")[0]
helpUI = uic.loadUiType("help.ui")[0]
infoUI = uic.loadUiType("info.ui")[0]
openSourceInfoUI = uic.loadUiType("openSourceLicense.ui")[0]


class MainApp(QMainWindow, mainAppUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # UI 초기화
        self.setStyleSheet('QMainWindow { background-color: rgb(182,182,182) }')
        self.setTimeLCD.setDigitCount(8)
        hour, minute, switch, _enablecancel, second, _notifytime = read_file()
        self.setTimeEdit.setTime(QtCore.QTime(int(hour), int(minute), int(second)))
        self.onoffCheckBox.setChecked(int(switch))
        if self.onoffCheckBox.isChecked():
            self.statusInfo.setText("현재 예약종료 활성화됨. ")
        else:
            self.statusInfo.setText("현재 예약종료 비활성화됨. ")
        self.help.setShortcut('Ctrl+?')


        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.updateTimes)
        self.timer.start()


        self.setTime = self.setTimeEdit.time()


        ## 기능부 연결
        self.closeButton.clicked.connect(self.closeButtonClicked)  # 닫기 버튼
        self.updateTimeLCD()  # LCD 업데이트
        self.onoffCheckBox.stateChanged.connect(self.switchCheckBoxChanged)  # 활성화/비활성화 체크박스
        self.timeApplyButton.clicked.connect(self.timeApplyButtonClicked)  # 시간 적용 버튼
        #self.setTimeEdit.timeChanged.connect(self.timeApplyButtonClicked)
        # <메뉴>
        self.advanced_settings.triggered.connect(self.advancedSettingsMenuClicked)  # 고급 설정 열기
        self.help.triggered.connect(self.helpClicked)  # 도움말 열기
        self.infoOfProgram.triggered.connect(self.infoClicked)  # 프로그램 정보 열기
        self.infoOpenSource.triggered.connect(self.openSourceInfoClicked)  # 오픈소스 정보 열기
        self.logoButton.clicked.connect(self.logoButtonClicked)

    # 기능부 구현
        self.switch = 1
    def logoButtonClicked(self):
        if self.switch:
            self.setStyleSheet('QMainWindow {}')
            self.switch = 0
        else:
            self.setStyleSheet('QMainWindow { background-color: rgb(182,182,182) }')
            self.switch = 1

    def closeButtonClicked(self):
        print("ui: closeButton clicked")
        self.close()

    def updateTimeLCD(self):
        self.hour, self.minute, self.switch, self.enablecancel, self.second, self.notifytime = read_file()
        self.setTimeLCD.display("{0}:{1}:{2}".format(self.hour, self.minute, self.second))

    def switchCheckBoxChanged(self, state):
        if state == QtCore.Qt.Checked:
            #print("switch checkbox on")
            edit_config('switch', '1')
            self.statusInfo.setText("현재 예약종료 활성화됨. ")
        else:
            #print("switch checkbox off")
            edit_config('switch', '0')
            self.statusInfo.setText("현재 예약종료 비활성화됨. ")
        restart_bg()

    def timeApplyButtonClicked(self):
        self.setTime = self.setTimeEdit.time()
        hour = self.setTime.hour() if (self.setTime.hour()>=10) else ('0'+str(self.setTime.hour()))
        minute = self.setTime.minute() if (self.setTime.minute()>=10) else ('0'+str(self.setTime.minute()))
        second = self.setTime.second() if (self.setTime.second()>=10) else ('0'+str(self.setTime.second()))
        print("changed hour: %s, minute: %s, second: %s" % (hour, minute, second))
        edit_config('hour', hour)
        edit_config('minute', minute)
        edit_config('second', second)
        self.updateTimeLCD()
        restart_bg()

    def closeEvent(self, QCloseEvent):
        #self.destroy()  # 다른 거에서 닫을 때 렉 이슈가 존재하여 일단 메인윈도우를 비활성화시킴.
        #if self.advanced_settings_dialog.isVisible() == True: self.advanced_settings_dialog.close()
        #if self.help_dialog.isVisible() == True: self.help_dialog.close()
        exit()
        pass

    def updateTimes(self):
        currentT = QtCore.QTime.currentTime()
        currentT_msec = QtCore.QTime.msecsSinceStartOfDay(currentT)
        if self.setTime <= currentT:  # 예약시간이 현재시간보다 이전일때 다음날 날짜로 계산함
            leftT_msec = (24 * 60 * 60 * 1000) - (currentT_msec - QtCore.QTime.msecsSinceStartOfDay(self.setTime)) + 1000
        else:  # 예약시간이 오늘기준일때
            leftT_msec = QtCore.QTime.msecsSinceStartOfDay(self.setTime) - currentT_msec + 1000
        leftT = QtCore.QTime.fromMSecsSinceStartOfDay(leftT_msec)
        self.currentTime.setText(currentT.toString("hh:mm:ss"))
        self.leftTime.setText(str(leftT.toString("hh:mm:ss")))


    def advancedSettingsMenuClicked(self):
        self.advanced_settings_dialog = AdvancedSettings()
        self.advanced_settings_dialog.show()
        pass

    def helpClicked(self):
        self.help_dialog = Help()
        self.help_dialog.show()

    def infoClicked(self):
        self.info_dialog = Info()
        self.info_dialog.show()

    def openSourceInfoClicked(self):
        self.open_source_info_dialog = OpenSourceInfo()
        self.open_source_info_dialog.show()


## 고급 설정 ##

class AdvancedSettings(QDialog, advancedSettingsUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.eastereggstack = 1


        # UI 초기화
        self.advancedGroupBox.setEnabled(False)
        self.pwTextBox.setFocus()
        self.pwTextBox.installEventFilter(self)


        # 기능부 연결
        self.loginButton.clicked.connect(self.loginButtonClicked)
        self.bgProgramStartButton.clicked.connect(self.bgProgramStartButtonClicked)
        self.bgProgramCloseButton.clicked.connect(self.bgProgramCloseButtonClicked)
        self.settingsFileCreateButton.clicked.connect(self.configFileCreateButtonClicked)
        self.settingsFileDeleteButton.clicked.connect(self.configFileDeleteButtonClicked)
        self.startupEnableButton.clicked.connect(self.startupEnableButtonClicked)
        self.startupDisableButton.clicked.connect(self.startupDisableButtonClicked)
        self.disableCancelRadioButton.clicked.connect(self.disableCancelRadioButtonClicked)
        self.enableCancelRadioButton.clicked.connect(self.enableCancelRadioButtonClicked)
        self.notifyTimeApplyButton.clicked.connect(self.notifyTimeApplyButtonClicked)


    # eventFilter을 override하여 키입력을 확인
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.pwTextBox:
            if event.key() == QtCore.Qt.Key_Return and self.pwTextBox.hasFocus():
                self.loginButtonClicked()
        return super().eventFilter(obj, event)



    def loginButtonClicked(self):
        _hour, _minute, _switch, enablecancel, _second, notifytime = read_file()
        if self.pwTextBox.text() == password:
            self.advancedGroupBox.setEnabled(True)
            self.statusDisplay.setText("로그인 성공! :)")
            self.loginButton.setFocus()

            # 숨겼던 UI 요소들을 초기화함
            # 1. 중도취소 버튼 사용 여부
            if enablecancel == '0':
                self.disableCancelRadioButton.setChecked(1)
            elif enablecancel == '1':
                self.enableCancelRadioButton.setChecked(1)
            else:
                raise ValueError('enablecancel value key error')
            # 2. 종료예약 창 n초 미리 뜨게 하기
            self.notifyTimeSpinBox.setValue(int(notifytime))

        else:
            self.advancedGroupBox.setEnabled(False)
            self.statusDisplay.setText("로그인 실패! (%d) :l" % self.eastereggstack)
            self.pwTextBox.setText("")
            self.eastereggstack+=1
            if 100<=self.eastereggstack<=499:
                self.statusDisplay.setStyleSheet('QLabel { color: rgb(%d,%d,%d) }' % (
                    random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                self.statusDisplay.setText("( ͡° ͜ʖ ͡°) [ %d ] щ（ﾟДﾟщ）" % self.eastereggstack)
            if self.eastereggstack >= 500:

                self.statusDisplay.setStyleSheet('QLabel { background-color: rgb(%d,%d,%d); color: rgb(%d,%d,%d); }' % (
                                                 random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                                 random.randint(0, 255), random.randint(0, 255),
                                                 random.randint(0, 255)))
                self.statusDisplay.setText("ㅋㅋㅋ x %d" % self.eastereggstack)


    def bgProgramStartButtonClicked(self):
        bgProgramStart()
        self.statusDisplay.setText("백그라운드 프로그램을 실행했습니다. ")

    def bgProgramCloseButtonClicked(self):
        bgProgramClose()
        self.statusDisplay.setText("백그라운드 프로그램을 종료했습니다. ")

    def configFileCreateButtonClicked(self):
        try:
            if os.path.isfile('offTimeConfig.ini'): raise FileExistsError
            createConfigFile()
        except FileExistsError:
            self.statusDisplay.setText("설정파일이 이미 존재합니다! 설정파일을 리셋하기 위해서는 설정파일을 삭제하고 다시 생성하세요.")
        except:
            self.statusDisplay.setText("오류가 발생했습니다! 실행 권한 또는 백신 프로그램을 체크해주세요.")
        else:
            self.statusDisplay.setText("설정파일을 생성하였습니다.")

    def configFileDeleteButtonClicked(self):
        try:
            deleteConfigFile()
        except:
            self.statusDisplay.setText("설정 파일이 이미 존재하지 않습니다.")
        else:
            self.statusDisplay.setText("설정 파일을 삭제했습니다. ")

    def startupEnableButtonClicked(self):
        try:
            import win32com.client
            appdata = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
            print(':::', appdata)
            path = os.path.join(appdata, r'offtime-bg-b2ZmdGltZS1iZw.exe.lnk')
            dirname = os.path.dirname(__file__)
            target = os.path.join(dirname, r'\offtime-bg-b2ZmdGltZS1iZw.exe')
            icon = os.path.join(dirname, r'\offtime-bg-b2ZmdGltZS1iZw.exe')
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.IconLocation = icon
            shortcut.save()
        except:
            self.statusDisplay.setText("오류가 발생했습니다! 실행 권한 또는 백신 프로그램을 체크해주세요. ")
        else:
            self.statusDisplay.setText("시작프로그램에 등록되었습니다. ")

    def startupDisableButtonClicked(self):
        try:
            os.remove(os.path.join(os.getenv('APPDATA'),
                                   r"Microsoft\Windows\Start Menu\Programs\Startup\offtime-bg-b2ZmdGltZS1iZw.exe.lnk"))
        except:
            self.statusDisplay.setText("시작프로그램에 등록되지 않은 상태입니다.")
        else:
            self.statusDisplay.setText("시작프로그램에서 삭제되었습니다.")

    def disableCancelRadioButtonClicked(self):
        edit_config('enablecancel', '0')
        self.statusDisplay.setText("예약 취소 버튼을 비활성화했습니다. 이제 종료 예정 안내창에서 종료를 취소할 수 없습니다.")
        restart_bg()


    def enableCancelRadioButtonClicked(self):
        edit_config('enablecancel', '1')
        self.statusDisplay.setText("예약 취소 버튼을 활성화했습니다. 종료 예정 안내창에서 종료 취소가 가능합니다.")
        restart_bg()

    def notifyTimeApplyButtonClicked(self):
        edit_config('notifytime', str(self.notifyTimeSpinBox.value()))
        self.statusDisplay.setText("예약 시간 {0}초 전에 종료 예정 안내창을 띄우도록 설정되었습니다.".format(self.notifyTimeSpinBox.value()))
        restart_bg()






## 도움말 창 ##
class Help(QDialog, helpUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 기능부 연결
        self.closeButton.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self):
        self.close()

## 프로그램 정보 창 ##
class Info(QDialog, infoUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logoClickTimes = 0

        # 기능부 연결
        self.closeButton.clicked.connect(self.closeButtonClicked)
        self.logoButton.clicked.connect(self.logoButtonClicked)

    def closeButtonClicked(self):
        self.close()

    # easter egg
    def logoButtonClicked(self):
        self.logoClickTimes += 1
        if self.logoClickTimes % 2:  # 홀수
            self.logo.hide()
        else:
            self.logo.show()
        if self.logoClickTimes > 10:
            self.titleLabel.setText("Secret Found! %d times of useless clicks" % self.logoClickTimes)
            if random.randint(1,100) <= 30:
                self.setStyleSheet('QDialog { background-color: rgb(%d,%d,%d) }'
                                   % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            else:
                self.setStyleSheet('QDialog { background-color: rgb(182,182,182) }')
            pass




## 오픈소스 정보 창 ##
class OpenSourceInfo(QDialog, openSourceInfoUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 기능부 연결
        self.closeButton.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self):
        self.close()


class open:
    def __init__(self):
        self.mainapp()

    @staticmethod
    def mainapp():
        # 구동부
        app = QApplication(sys.argv)
        MainWindow = MainApp()
        MainWindow.show()
        app.exec_()

#open_advanced_settings()