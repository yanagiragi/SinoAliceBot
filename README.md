# KurtzPelBot

## Dev Environments

Win10 (64bit)

Python 3.7.2 (64 bit)

## Prerequisites

```pip install -r requirements.txt```

* if failed, you may need to download source code of [pyHook](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook) and install manually.

## Run

Create scrspy instance: ```.\scrcpy.exe --window-height 720 --window-borderless -w```

Run: ```python main.py [--debug]``` or ```./main.exe [--debug]``` (for built executable)

## Build

```pyinstaller -F ./main.py && cp -rfv Resources dist/Resources```
