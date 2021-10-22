import MakeUI
import sys
from ctypes import windll
from elevate import elevate

# user-defined libraries
from modules import *

# due to bug in PyInstaller, some modules must be imported in main.py
import requests
import win32com.client

try:
    elevate(show_console=True)
except OSError:
    title = '권한 오류'
    text = '오프타임 제어판을 열기 위해 관리자 권한이 필요합니다.'
    windll.user32.MessageBoxW(0, text, title, 0x00010010)
    sys.exit()

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

def start():
    if check_file() is False: create_file()
    restart_bg()
    make_ui = MakeUI
    make_ui.open()


start()
