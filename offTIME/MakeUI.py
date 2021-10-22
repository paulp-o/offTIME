import random
import sys
import win32com.client

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import *

# user-defined libraries
from modules import *
import updater

password = "1234"

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

# load UI files
mainAppUI = uic.loadUiType("ui/mainapp.ui")[0]
advancedSettingsUI = uic.loadUiType("ui/advanced_settings.ui")[0]
helpUI = uic.loadUiType("ui/help.ui")[0]
infoUI = uic.loadUiType("ui/info.ui")[0]
openSourceInfoUI = uic.loadUiType("ui/openSourceLicense.ui")[0]


class MainApp(QMainWindow, mainAppUI):
    def __init__(self):
        super().__init__()
        self.open_source_info_dialog = OpenSourceInfo()
        self.info_dialog = Info()
        self.help_dialog = Help()
        self.advanced_settings_dialog = AdvancedSettings()
        self.hour, self.minute, self.switch, self.enablecancel, self.second, self.notifytime = read_file()
        self.setupUi(self)
        # Initialize UI
        self.verLabel_2.setText(updater.version)
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

        # Connect functions with UI elements
        self.closeButton.clicked.connect(self.closeButtonClicked)  # close button
        self.updateTimeLCD()  # update lcd with digital time
        self.onoffCheckBox.stateChanged.connect(self.switchCheckBoxChanged)  # checkbox: switch
        self.timeApplyButton.clicked.connect(self.timeApplyButtonClicked)  # time apply button
        self.createShortcutButton.clicked.connect(self.createShortcutClicked)  # create shortcut button
        # self.setTimeEdit.timeChanged.connect(self.timeApplyButtonClicked)
        # <menus>
        self.advanced_settings.triggered.connect(self.advancedSettingsMenuClicked)  # menu: open advanced settings panel
        self.help.triggered.connect(self.helpClicked)  # menu: open help dialog
        self.infoOfProgram.triggered.connect(self.infoClicked)  # menu: open program information dialog
        self.infoOpenSource.triggered.connect(self.openSourceInfoClicked)  # menu: open OSS info dialog
        self.check_update.triggered.connect(self.updateMenuClicked)  # menu: open updater dialog
        # when logo clicked (for easteregg)
        self.logoButton.clicked.connect(self.logoButtonClicked)

        # this is for switching between gray/white background color mode.
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
        self.setTimeLCD.display("{0}:{1}:{2}".format(self.hour, self.minute, self.second))
        print(self.hour, self.minute, self.second)

    def switchCheckBoxChanged(self, state):
        if state == QtCore.Qt.Checked:
            # print("switch checkbox on")
            edit_config('switch', '1')
            self.statusInfo.setText("현재 예약종료 활성화됨. ")
        else:
            # print("switch checkbox off")
            edit_config('switch', '0')
            self.statusInfo.setText("현재 예약종료 비활성화됨. ")
        restart_bg()

    def timeApplyButtonClicked(self):
        self.setTime = self.setTimeEdit.time()
        self.hour = self.setTime.hour() if (self.setTime.hour() >= 10) else ('0' + str(self.setTime.hour()))
        self.minute = self.setTime.minute() if (self.setTime.minute() >= 10) else ('0' + str(self.setTime.minute()))
        self.second = self.setTime.second() if (self.setTime.second() >= 10) else ('0' + str(self.setTime.second()))
        print("changed hour: %s, minute: %s, second: %s" % (self.hour, self.minute, self.second))
        edit_config('hour', self.hour)
        edit_config('minute', self.minute)
        edit_config('second', self.second)
        self.updateTimeLCD()
        restart_bg()

    def closeEvent(self, QCloseEvent):
        self.hide()
        super().hide()
        sys.exit()

    def updateTimes(self):
        currentT = QtCore.QTime.currentTime()
        currentT_msec = QtCore.QTime.msecsSinceStartOfDay(currentT)
        if self.setTime <= currentT:  # if set time is passed already, consider it to be tomorrow
            leftT_msec = (24 * 60 * 60 * 1000) - \
                         (currentT_msec - QtCore.QTime.msecsSinceStartOfDay(self.setTime)) + 1000
        else:  # when set time is today
            leftT_msec = QtCore.QTime.msecsSinceStartOfDay(self.setTime) - currentT_msec + 1000
        leftT = QtCore.QTime.fromMSecsSinceStartOfDay(leftT_msec)
        self.currentTime.setText(currentT.toString("hh:mm:ss"))
        self.leftTime.setText(str(leftT.toString("hh:mm:ss")))

    def advancedSettingsMenuClicked(self):
        self.advanced_settings_dialog.show()
        pass

    def helpClicked(self):
        self.help_dialog.show()

    def infoClicked(self):
        self.info_dialog.show()

    def openSourceInfoClicked(self):
        self.open_source_info_dialog.show()

    def updateMenuClicked(self):
        import updater
        self.updater_dialog = updater.Updater()
        self.updater_dialog.show()
        self.updater_dialog.updateStart()

    def createShortcutClicked(self):
        try:
            import win32com.client
            appdata = os.path.join(os.getenv('USERPROFILE'), r"Desktop")
            print(':::', appdata)
            path = os.path.join(appdata, r'오프타임 제어판.lnk')
            dirname = os.path.dirname(__file__)
            target = os.path.join(dirname, r'offTIME.exe')
            icon = os.path.join(dirname, r'offTIME.exe')
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.IconLocation = icon
            shortcut.save()
        except:
            self.createShortcutButton.setText("실패(오류)!")
        else:
            self.createShortcutButton.setText("완료!")


# advanced settings dialog #

class AdvancedSettings(QDialog, advancedSettingsUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.eastereggstack = 1

        # Initializing UI
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.advancedGroupBox.setEnabled(False)
        self.pwTextBox.setFocus()
        self.pwTextBox.installEventFilter(self)

        # connect functions with UI elements
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

    # override eventFilter function in QDialog.py for key event feature
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

            # initialize disabled UI elements
            # 1. init enablecancel settings
            if enablecancel == '0':
                self.disableCancelRadioButton.setChecked(1)
            elif enablecancel == '1':
                self.enableCancelRadioButton.setChecked(1)
            else:
                raise ValueError('enablecancel value key error')
            # 2. init notify_time settings
            self.notifyTimeSpinBox.setValue(int(notifytime))

        else:
            self.advancedGroupBox.setEnabled(False)
            self.statusDisplay.setText("로그인 실패! (%d) :l" % self.eastereggstack)
            self.pwTextBox.setText("")
            self.eastereggstack += 1
            if 100 <= self.eastereggstack <= 499:
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
            if os.path.isfile('C:\offTimeConfig.ini'): raise FileExistsError
            createConfigFile()
        except FileExistsError:
            self.statusDisplay.setText("설정파일이 이미 존재합니다! 설정파일을 리셋하기 위해서는 설정파일을 삭제하고 다시 생성하세요.")
        except Exception as e:
            self.statusDisplay.setText("오류가 발생했습니다! 실행 권한 또는 백신 프로그램을 체크해주세요.")
            print(e)
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
            appdata = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
            print(':::', appdata)
            path = os.path.join(appdata, r'offtimeSvc.exe.lnk')
            dirname = os.path.dirname(__file__)
            target = os.path.join(dirname, r'offtimeSvc.exe')
            icon = os.path.join(dirname, r'offtimeSvc.exe')
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.IconLocation = icon
            shortcut.save()
        except Exception as e:
            self.statusDisplay.setText("오류가 발생했습니다! 실행 권한 또는 백신 프로그램을 체크해주세요. ")
            print(e)
        else:
            self.statusDisplay.setText("시작프로그램에 등록되었습니다. ")

    def startupDisableButtonClicked(self):
        try:
            os.remove(os.path.join(os.getenv('APPDATA'),
                                   r"Microsoft\Windows\Start Menu\Programs\Startup\offtimeSvc.exe.lnk"))
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


# Help Dialog #
class Help(QDialog, helpUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        # connect functions with UI elements
        self.closeButton.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self):
        self.close()


# Program Info Dialog #
class Info(QDialog, infoUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.logoClickTimes = 0

        # connect functions with UI elements
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
            if random.randint(1, 100) <= 30:
                self.setStyleSheet('QDialog { background-color: rgb(%d,%d,%d) }'
                                   % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            else:
                self.setStyleSheet('QDialog { background-color: rgb(182,182,182) }')
            pass


# OSS Info Dialog#
class OpenSourceInfo(QDialog, openSourceInfoUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        # connect functions with UI elements
        self.closeButton.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self):
        self.close()


class open:
    def __init__(self):
        self.mainapp()

    @staticmethod
    def mainapp():
        # run ! ! !
        app = QApplication(sys.argv)
        MainWindow = MainApp()
        MainWindow.show()
        app.exec_()
