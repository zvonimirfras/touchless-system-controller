# Touchless System Controller

ZTSC allows you to control your desktop system without touching it.

Except the obvious cool factor, useful usecases include:

- Casual web browsing
- Following cooking recipes without smudging your screen or keyboard

## Features

- Move pointer with your index finger
- Relative and absolute movement
- Key tap or screen tap to click
- Grab and drag screen to scroll
- Swipe vertically to scroll
- Swipe horizontally to navigate browser history
- Circle to switch browser tabs
- Reverse swipe and scroll directions

## Requirements

### Daemon

- LeapMotion controller
- LeapMotion drivers
- LeapMotion python SDK
- PyUserInput (`sudo pip2 install pyuserinput`)

### Graphical User Interface a.k.a. GUI Controller

- PyQt5 (`pip3 install pyqt5` or `sudo pip3 install pyqt5`)
- psutil (`pip3 install psutil` or `sudo pip3 install psutil`; needed to check if `leapd` is running)

### Audio commands

PyAudio (`pip3 install PyAudio`)
SpeechRecognition (`pip3 install SpeechRecognition`)
pyttsx3 (`pip3 install pyttsx3`)
gTTS (`pip3 install gTTS`)
playsound (`pip3 install playsound`)
nltk (`pip3 install nltk`)

## Install and run

I found `leapd` to be somewhat unstable on my machine so ZTSC contains a convenient script to keep it running.

Run on one terminal:

```bash
sudo ./keep_leapd_resurected.sh
```

In a second one run the main application by typing:

```bash
python2 daemon.py
```

## Settings

- Open [`settings.json`](settings.json).
- Change.
- Save.
- Rerun the app.

## Tested on

- Linux Manjaro (Arch based)
