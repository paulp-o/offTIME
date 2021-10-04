# GUI 모듈들 불러오기
import MakeUI
from modules import *


# 시작프로그램에 등록될 "invisible 메인" 프로그램
# 하는 일: 30초에 한 번씩 설정값 파일을 읽어서 세팅값을 가져온다.
# 이 프로그램의 구동은 보이지 않게 진행된다 (이는 py2exe 과정에서 설정). 인위적으로 켜거나 끄는 기능은 '보조' 프로그램에서 담당한다.


def open_window():
    make_ui = MakeUI
    make_ui.open.mainapp()


def start():
    # create_file() # debugging
    if check_file() is False: create_file()
    restart_bg()
    make_ui = MakeUI
    make_ui.open.mainapp()


start()
