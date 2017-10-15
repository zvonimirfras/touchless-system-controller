#!/usr/bin/python2

import sys

from pymouse import PyMouse
from pykeyboard import PyKeyboard

import Leap
from Leap import CircleGesture, SwipeGesture

from settings import Settings

from pointer import Pointer
from printer import Printer

## TODO add features:
## limit swipe to directions (don't swipe unless the direction is correct in all directions, i.e. not diagonal)
## press mouse button by moving the finger towards the screen (Leap.Gesture.TYPE_SCREEN_TAP?)
## scroll with grabbing the screen with a fist and dragging


class MainListener(Leap.Listener):
    """Leap listener that handles all the user interactions"""
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_STOP']

    def __init__(self, settings):
        Leap.Listener.__init__(self);
        self.settings = settings

    def on_init(self, controller):
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.pointer = Pointer(self.mouse, self.settings)
        self.printer = Printer(self.settings)

        print("Initialized")


    def on_connect(self, controller):
        print("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);


    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")


    def on_exit(self, controller):
        print("Exited")


    def on_frame(self, controller):
        self.printer.echo(controller)
        self.pointer.move(controller)
        self.pointer.click(controller)
        self.pointer.scroll(controller)

        frame = controller.frame()

        for hand in frame.hands:
            normal = hand.palm_normal

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle = (circle.progress - previous_update.progress) * 2 * Leap.PI

                if circle.state == Leap.Gesture.STATE_STOP and circle.radius > 15 and circle.radius < 25:
                    # go to right or left tab by ctrl+pgdwn or ctrl+pgup
                    if clockwiseness == "clockwise":
                        self.keyboard.press_key(self.keyboard.control_key)
                        self.keyboard.tap_key(self.keyboard.page_down_key)
                        self.keyboard.release_key(self.keyboard.control_key)
                    elif clockwiseness == "counterclockwise":
                        self.keyboard.press_key(self.keyboard.control_key)
                        self.keyboard.tap_key(self.keyboard.page_up_key)
                        self.keyboard.release_key(self.keyboard.control_key)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)

                for hand in frame.hands:
                    normal = hand.palm_normal

                # go back on swipe right; forward on swipe left
                mouse_pos = self.mouse.position()
                palm_roll = normal.roll * Leap.RAD_TO_DEG
                if gesture.state == Leap.Gesture.STATE_START:
                    if swipe.direction.x > 0.33 \
                        and palm_roll > 90 - self.settings.tolerance["hand_roll"] \
                        and palm_roll < 90 + self.settings.tolerance["hand_roll"]:  # prevent false positives
                        self.mouse.click(mouse_pos[0], mouse_pos[1], 8)
                    elif swipe.direction.x < -0.33 \
                        and palm_roll > -90 - self.settings.tolerance["hand_roll"] \
                        and palm_roll < -90 + self.settings.tolerance["hand_roll"]:  # prevent false positives
                        self.mouse.click(mouse_pos[0], mouse_pos[1], 9)


def main():
    # Create a main listener and controller
    settings = Settings()
    listener = MainListener(settings)
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
