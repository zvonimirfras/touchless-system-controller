#!/usr/bin/python2

import sys

import Leap

from daemon.main_leap_listener import MainLeapListener
from settings import Settings

## TODO add features:
## limit swipe to directions (don't swipe unless the direction is correct in all directions, i.e. not diagonal)
## press mouse button by moving the finger towards the screen (Leap.Gesture.TYPE_SCREEN_TAP?)
## scroll with grabbing the screen with a fist and dragging



def main():
    # Create a main listener and controller
    settings = Settings()
    listener = MainLeapListener(settings)
    controller = Leap.Controller()

    # Have the main listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
