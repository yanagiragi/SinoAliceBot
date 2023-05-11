# Sinoalice Bot

A Bot designed originally for looping level in SinoAlice based on phone remote controls, template matching and hand-crafted mouse macros.

Now support different games via phone remote controls.

![](https://i.imgur.com/QdDbedk.png)

## Dev Environments

* Win10 (64bit)

* Python 3.7.2 (64 bit)

## Prerequisites

* ```pip install -r requirements.txt```

* if failed, you may need to download source code of [pyHook](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook) and install manually.

* And also get [Scrspy](https://github.com/Genymobile/scrcpy) relesae files

## Run

* Check scripts for details
  * for `daily_scheduler.sh`, might need to setup `.env.sh` first. `cp scripts/.env.sample.sh scripts/.env.sh` & setup credentials

## Build

* ```pyinstaller -F ./main.py && cp -rfv Resources dist/Resources```
