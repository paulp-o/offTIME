import configparser
import os
import subprocess

config = configparser.ConfigParser()
os.chdir(os.getcwd())

# check if configfile exists
def check_file():
    try:
        read_file()
    except:
        return False
    else:
        return True


def read_file():
    config.read(r"C:\offTimeConfig.ini", encoding="utf-8")
    # print(config.sections())
    setHour = config['TIME']['hour']
    setMinute = config['TIME']['minute']
    setSecond = config['TIME']['second']
    switch = config['ACTIVITY']['switch']
    enableCancel = config['ACTIVITY']['EnableCancel']
    notifyTime = config['ACTIVITY']['NotifyTime_sec']
    return setHour, setMinute, switch, enableCancel, setSecond, notifyTime


def create_file():
    with open(r"C:\offTimeConfig.ini", "w", encoding="utf-8") as configfile:
        config['TIME'] = {'Hour': '17',
                          'Minute': '59',
                          'Second': '00'}
        config['ACTIVITY'] = {'Switch': '0',
                              'EnableCancel': '1',
                              'NotifyTime_sec': '300'}
        config.write(configfile)


def edit_config(config_code, value):
    if config_code == 'hour':
        config['TIME']['Hour'] = str(value)
    elif config_code == 'minute':
        config['TIME']['Minute'] = str(value)
    elif config_code == 'second':
        config['TIME']['Second'] = str(value)
    elif config_code == 'switch':
        config['ACTIVITY']['Switch'] = str(value)
    elif config_code == 'enablecancel':
        config['ACTIVITY']['EnableCancel'] = str(value)
    elif config_code == 'notifytime':
        config['ACTIVITY']['NotifyTime_sec'] = str(value)
    else:
        raise ValueError("Wrong config code")
    with open(r"C:\offTimeConfig.ini", "w", encoding="utf-8") as configfile:
        config.write(configfile)


def bgProgramStart():
    restart_bg()


def bgProgramClose():
    close_bg()


def createConfigFile():
    create_file()


def deleteConfigFile():
    os.remove(r'C:\offTimeConfig.ini')


def open_bg():
    if os.path.isfile(r'offtimeSvc.exe'):
        print('exe exist')
        dirname = os.path.dirname(__file__)
        subprocess.Popen(os.path.join(dirname, r'offtimeSvc.exe'))
    else:
        print('no background program to open !!!!!!')


def close_bg():
    subprocess.call('TASKKILL /F /IM offtimeSvc.exe', creationflags=0x08000000)
    pass


def restart_bg():
    print('restarting bgprogram')
    close_bg()
    open_bg()
