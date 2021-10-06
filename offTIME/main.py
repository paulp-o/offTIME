import MakeUI
import sys

# user-defined libraries
from modules import *

# due to bug in PyInstaller, some modules must be imported in main.py
import requests
import win32com.client

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
