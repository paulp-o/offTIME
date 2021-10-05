# GUI 모듈들 불러오기
import MakeUI
from modules import *

def start():
    if check_file() is False: create_file()
    restart_bg()
    make_ui = MakeUI
    make_ui.open()


start()
