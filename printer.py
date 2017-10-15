import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class Printer():
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_STOP']

    def __init__(self, settings):
        self.settings = settings

    def echo(self, controller):
        frame = controller.frame()

        if self.settings.printer["frame_info"]:
            print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
                frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:
            if self.settings.printer["hand_info"]:
                handType = "Left hand" if hand.is_left else "Right hand"
                print "  %s, id %d, position: %s" % (
                    handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            if self.settings.printer["hand_angles"]:
                print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                    direction.pitch * Leap.RAD_TO_DEG,
                    normal.roll * Leap.RAD_TO_DEG,
                    direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            if self.settings.printer["arm_info"]:
                arm = hand.arm
                print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                    arm.direction,
                    arm.wrist_position,
                    arm.elbow_position)


            # Get fingers
            for finger in hand.fingers:
                if self.settings.printer["finger_info"]:
                    print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                        self.finger_names[finger.type],
                        finger.id,
                        finger.length,
                        finger.width)

                # Get bones
                if self.settings.printer["finger_bone_info"]:
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                            self.bone_names[bone.type],
                            bone.prev_joint,
                            bone.next_joint,
                            bone.direction)

        # Get tools
        for tool in frame.tools:
            if self.settings.printer["tools_info"]:
                print "  Tool id: %d, position: %s, direction: %s" % (
                    tool.id, tool.tip_position, tool.direction)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE and self.settings.printer["gesture_circle"]:
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
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)


            if gesture.type == Leap.Gesture.TYPE_SWIPE and self.settings.printer["gesture_swipe"]:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                        gesture.id, self.state_names[gesture.state],
                        swipe.position, swipe.direction, swipe.speed)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP and self.settings.printer["gesture_key_tap"]:
                keytap = KeyTapGesture(gesture)
                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction )

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP and self.settings.printer["gesture_screen_tap"]:
                screentap = ScreenTapGesture(gesture)
                print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        screentap.position, screentap.direction )
