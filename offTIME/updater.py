import requests
import random
from os.path import dirname, abspath
from bs4 import BeautifulSoup
from PyQt5 import uic, QtTest
from PyQt5.QtWidgets import *

path = dirname(dirname(abspath(__file__)))
version = '2110c'
url = 'https://raw.githubusercontent.com/flickout/offTIME/master/version.txt'
updaterUI = uic.loadUiType("ui/updater.ui")[0]


class Updater(QDialog, updaterUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def updateStart(self):
        self.progressBar.setFormat("Initializing...")
        # start
        self.progressBar.setProperty("maximum", 100)
        QtTest.QTest.qWait(random.randint(50,150))
        self.progressBar.setValue(random.randint(10,20))
        self.progressBar.setFormat("Loading URL...")
        # ???
        text = '...'
        QtTest.QTest.qWait(random.randint(50,200))
        self.progressBar.setValue(random.randint(40,50))
        self.progressBar.setFormat("Downloading Data from the internet...")
        try:
            # request data from url
            response = requests.get(url)
            QtTest.QTest.qWait(random.randint(300,700))
            self.progressBar.setValue(random.randint(60,70))
            self.progressBar.setFormat("Receiving Response...")
            # receive code
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                QtTest.QTest.qWait(random.randint(100,250))
                self.progressBar.setValue(random.randint(90,95))
                self.progressBar.setFormat("Done!")
                if version < str(soup):
                    print(version==soup)
                    print(soup)
                    self.progressBar.hide()
                    text = '현재버전: {0}, 최신버전: {1} \n' \
                           '최신버전이 아님, 정보 메뉴에서 업데이트하세요.'.format(version, soup)
                else:
                    self.progressBar.setValue(100)
                    text = '현재 최신버전인 {0}입니다.'.format(version)
            else:
                self.progressBar.setProperty("maximum", 0)
                text = '업데이트 확인 서버 오류!'
        except Exception as e:
            self.progressBar.hide()
            text = '오류입니다. 인터넷 연결을 확인하세요. code: {0}'.format(e)
        finally:
            self.label.setText(text)


