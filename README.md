# KurtzPelBot

## Dev Environments

Win10 (64bit)

Python 3.6 (32 bit)

## Prerequisites

```pip install -r requirements.txt```

* if failed, you may need to download source code of [pyHook](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook) and install manually.

## Run

```python main.py [--debug]```

or

```./main.exe [--debug]```

## Build

```pyinstaller -F ./main.py && cp -rfv Resources dist/Resources```
