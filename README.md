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

- LeapMotion controller
- LeapMotion drivers
- LeapMotion python SDK
- PyUserInput

(`sudo pip2 install pyuserinput`)

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
