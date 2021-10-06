<p align="left">
  <img src="offTIME/icon/iconLong.png" width="50%"/>
  <br>
</p>

### :sparkles: 관공서에 최적화된 PC 예약종료 프로그램 :sparkles:
###### 광고, 업데이트, 라이센스 등의 문제가 전혀 없는, 관공서 사용에 특화된 오픈 소스 PC 예약 종료 프로그램입니다. 


| 다운로드 / 소스 코드 | [:octocat: GitHub](https://github.com/flickout/offTIME/releases) |
| :--: | -- |
#

#### :zap: 주요 기능 / 특징
- :alarm_clock: 매일 특정 시간에 반복하여 PC를 예약 종료합니다.
- :clock3: 종료하기 몇 분 전부터 종료 예약 알림창을 띄울지 설정 가능합니다.
- :negative_squared_cross_mark:	관공서의 민원인용PC 등 특정 PC에선 사용자가 종료 예약을 취소시키지 못하게끔 설정할 수 있습니다.
- :arrows_counterclockwise: 프로그램을 시작프로그램에 등록할 수 있어 별도의 실행 없이 동작하게 할 수 있습니다.
- :blush: 광고나 업데이트 등의 알림을 일체 띄우지 않으며 업데이트를 강제하지 않습니다.

#
#### :page_with_curl: 사용 원칙 (라이센스)
- 이 프로그램은 [GPLv3 라이센스](https://www.gnu.org/licenses/gpl-3.0.en.html)로 배포됩니다.
- 개인, 기업, 관공서 등 모든 사용자가 자유롭게 이용할 수 있습니다.
- 이 프로그램을 재배포할 시 원작자를 표시해야 합니다.

#
#### ℹ️ 제 3자 소프트웨어 정보 및 오픈 소스 라이센스
- [Qt 5](https://code.qt.io/cgit/) - [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
- [BeautifulSoup](https://github.com/waylan/beautifulsoup) - [MIT License](https://www.mit.edu/~amini/LICENSE.md)

#
#### :cd: 빌드 방법
소스 코드를 이용하여 프로그램을 빌드할 때 이러한 과정을 거칩니다.
- 먼저 _bg.py_ 의 디렉터리에서 pyInstaller을 통해 다음 명령어로 빌드합니다.

```Shell
pyinstaller --onefile --noconsole --clean --name offtime-bg-b2ZmdGltZS1iZw.exe --distpath ./ui --icon=./icon/iconSmall.ico bg.py
```
or
```Shell
pyinstaller -F -w --clean -n offtime-bg-b2ZmdGltZS1iZw.exe --distpath ./ui -i=./icon/iconSmall.ico bg.py
```

- _offtime-bg-b2ZmdGltZS1iZw.exe_ 이 _ui_ 폴더 안에 빌드되었을 때, _main.py_ 의 디렉터리에서 pyInstaller을 통해 빌드하면 됩니다.

> ##### PyInstaller 빌드 참고 사항 (_.spec_):
> #####
> in **Analysis**:
> #####
> datas=[('./icon/icon.png', './icon'),('./icon/iconLong.png', './icon'),('./icon/iconSmall.png', './icon'),('./icon/iconSmall.ico', './icon'),('./ui/*', './ui'),('./ui/offtime-bg-b2ZmdGltZS1iZw.exe', './ui')]
> #####
> hiddenimports=['MakeUI','modules.*','updater','resources_rc','bs4.BeautifulSoup','requests','win32com.client']
> #####
> in **exe**:
> #####
> icon='./icon/iconSmall.ico'
> #####











