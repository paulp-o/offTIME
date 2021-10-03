import configparser, subprocess, os

config = configparser.ConfigParser()

# config 파일의 존재여부 검사
def check_file():
    try:
        with open("offTimeConfig.ini", "r", encoding="utf-8"): read_file()
    except: return False
    else:
        return True

# 파일 읽기
def read_file():
    config.read("offTimeConfig.ini")
    #print(config.sections())
    setHour = config['TIME']['hour']
    setMinute = config['TIME']['minute']
    setSecond = config['TIME']['second']
    switch = config['ACTIVITY']['switch']
    enableCancel = config['ACTIVITY']['EnableCancel']
    notifyTime = config['ACTIVITY']['NotifyTime_sec']

    # print("read configfile:", setHour, setMinute, switch, enableCancel, setSecond, notifyTime)
    return setHour, setMinute, switch, enableCancel, setSecond, notifyTime

# 파일 생성하기 (없을 경우)
def create_file():
    with open("offTimeConfig.ini", "w", encoding="utf-8") as configfile:
        config['TIME'] = {'Hour' : '17',
                          'Minute' : '59',
                          'Second' : '00'}
        config['ACTIVITY'] = {'Switch' : '0',
                              'EnableCancel' : '1',
                              'NotifyTime_sec' : '300'}
        config.write(configfile)

# 파일 수정하는 기능
def edit_config(config_code, value):
    with open("offTimeConfig.ini", "w", encoding="utf-8") as configfile:
        if config_code == 'hour': config['TIME']['Hour'] = str(value)
        elif config_code == 'minute': config['TIME']['Minute'] = str(value)
        elif config_code == 'second': config['TIME']['Second'] = str(value)
        elif config_code == 'switch': config['ACTIVITY']['Switch'] = str(value)
        elif config_code == 'enablecancel': config['ACTIVITY']['EnableCancel'] = str(value)
        elif config_code == 'notifytime': config['ACTIVITY']['NotifyTime_sec'] = str(value)
        else: raise ValueError("Wrong config code")
        config.write(configfile)

# 고급 설정 메뉴의 버튼들
def bgProgramStart():
    restart_bg()

def bgProgramClose():
    close_bg()

def createConfigFile():
    create_file()

def deleteConfigFile():
    os.remove('offTimeConfig.ini')

def open_bg():
    if os.path.isfile('offtime-bg-b2ZmdGltZS1iZw.exe'):
        print('exe exist')
        subprocess.Popen('offtime-bg-b2ZmdGltZS1iZw.exe')
    else:
        print('no background program to open !!!!!!')


def close_bg():
    os.system("TASKKILL /F /IM offtime-bg-b2ZmdGltZS1iZw.exe")
    pass

def restart_bg():
    print('restarting bgprogram')
    close_bg()
    open_bg()
