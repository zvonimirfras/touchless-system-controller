import math
import datetime

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from settings import Settings


class Pointer():
    def __init__(self, mouse, settings):
        self.mouse = mouse
        self.settings = settings

        self.previous_palm_pos = None
        self.relative_pointer_starting_point = None
        self.relative_palm_starting_point = None
        self.grab_palm_starting_point = None
        self.previous_scroll_step_y = 0
        self.previous_scroll_step_x = 0
        self.pointer_time = datetime.datetime.now()


    ## move pointer according to hand position if index finger is pointing
    def move(self, controller):
        frame = controller.frame()

        for hand in frame.hands:
            extended_fingers = frame.fingers.extended()

            if len(extended_fingers) == 1 and extended_fingers[0].type == 1:
                if not self.relative_palm_starting_point:
                    self.relative_palm_starting_point = hand.palm_position
                if not self.relative_pointer_starting_point:
                    self.relative_pointer_starting_point = self.mouse.position()

                # absolute and relative mouse movement
                if self.settings.pointer["movement"] == "absolute":
                    self.mouse.move(5 * (400 + hand.palm_position.x), 4 * (400 - hand.palm_position.y))
                else:
                    multiplier = self.settings.pointer["relative_multiplier"]
                    if self.previous_palm_pos:
                        self.mouse.move(
                            self.relative_pointer_starting_point[0] + multiplier * (hand.palm_position.x - self.relative_palm_starting_point.x),
                            self.relative_pointer_starting_point[1] + multiplier * (-hand.palm_position.y + self.relative_palm_starting_point.y))

                    self.previous_palm_pos = hand.palm_position
            else:
                # reset relative pointer starting point
                self.relative_pointer_starting_point = None
                self.relative_palm_starting_point = None


    def click(self, controller):
        frame = controller.frame()

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP and self.settings.pointer["key_tap_click"]:
                mouse_pos = self.mouse.position()
                self.mouse.click(mouse_pos[0], mouse_pos[1], 1)

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP and self.settings.pointer["screen_tap_click"]:
                mouse_pos = self.mouse.position()
                self.mouse.click(mouse_pos[0], mouse_pos[1], 1)


    def scroll(self, controller):
        frame = controller.frame()

        if self.settings.pointer["swipe_scroll"]:
            mouse_pos = self.mouse.position()
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)

                    for hand in frame.hands:
                        normal = hand.palm_normal

                    # go back on swipe right; forward on swipe left
                    palm_roll = normal.roll * Leap.RAD_TO_DEG
                    # scroll up on swipe down; down on swipe up (natural swipe)
                    if gesture.state == Leap.Gesture.STATE_START \
                        and palm_roll > -self.settings.tolerance["hand_roll"] \
                        and palm_roll < self.settings.tolerance["hand_roll"]:  # prevent false positives
                        if swipe.direction.y < -0.24:
                            if self.settings.pointer["reverse_swipe_direction"]:
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 5)
                            else:
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 4)
                        elif swipe.direction.y > 0.24:
                            if self.settings.pointer["reverse_swipe_direction"]:
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 4)
                            else:
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 5)

        if self.settings.pointer["grab_scroll"]:
            mouse_pos = self.mouse.position()
            for hand in frame.hands:
                if hand.grab_strength > 0.96 and len(frame.fingers.extended()) == 0:
                    # grab
                    if not self.grab_palm_starting_point:
                        self.grab_palm_starting_point = hand.palm_position
                        self.previous_scroll_step_y = 0
                        self.previous_scroll_step_x = 0

                    # vertical scroll
                    scroll_step_y = int((hand.palm_position.y - self.grab_palm_starting_point.y) /
                                      self.settings.pointer["grab_scroll_step"])
                    relative_scroll_step_y = self.previous_scroll_step_y - scroll_step_y
                    self.previous_scroll_step_y = scroll_step_y
                    if relative_scroll_step_y > 0:
                        if self.settings.pointer["reverse_grab_scroll_direction_y"]:
                            for i in range(relative_scroll_step_y):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 5)
                        else:
                            for i in range(relative_scroll_step_y):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 4)
                    elif relative_scroll_step_y < 0:
                        if self.settings.pointer["reverse_grab_scroll_direction_y"]:
                            for i in range(-relative_scroll_step_y):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 4)
                        else:
                            for i in range(-relative_scroll_step_y):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 5)

                    # horizontal scroll
                    scroll_step_x = int((hand.palm_position.x - self.grab_palm_starting_point.x) /
                                      self.settings.pointer["grab_scroll_step"])
                    relative_scroll_step_x = self.previous_scroll_step_x - scroll_step_x
                    self.previous_scroll_step_x = scroll_step_x
                    if relative_scroll_step_x > 0:
                        if self.settings.pointer["reverse_grab_scroll_direction_x"]:
                            for i in range(relative_scroll_step_x):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 6)
                        else:
                            for i in range(relative_scroll_step_x):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 7)
                    elif relative_scroll_step_x < 0:
                        if self.settings.pointer["reverse_grab_scroll_direction_x"]:
                            for i in range(-relative_scroll_step_x):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 7)
                        else:
                            for i in range(-relative_scroll_step_x):
                                self.mouse.click(mouse_pos[0], mouse_pos[1], 6)

                else:
                    # release
                    self.grab_palm_starting_point = None
                    self.previous_scroll_step_y = None
                    self.previous_scroll_step_x = None
