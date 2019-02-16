#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Starts the GUI controller
"""

import _thread
import sys
import subprocess
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
                             QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QMenu, QPushButton, QSpinBox, QStyle, QSystemTrayIcon,
                             QTextEdit, QVBoxLayout)
from PyQt5.QtGui import QIcon, QFont

import nltk
import psutil

from settings import Settings
from dialogue import Dialogue
from command_center import CommandCenter

import systray_rc


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()

        self.leapd = None
        self.leapRunner = None

        self.settings = Settings()
        microphone_device_index = self.settings.microphone["device_index"]
        self.dialogue = Dialogue(microphone_device_index=microphone_device_index)
        self.command_center = CommandCenter(dialogue=self.dialogue)

        self.name = "ZTSC"

        self.initUi()

        if self.settings.leap["enabled"]:
            self.initLeap()


    def initLeap(self):
        if self.isLeapDaemonRunning():
            self.showMessage(message="Leap daemon running.")
            # leapd independently ran
            # TODO periodically check if it's running and run it if it dies
        else:
            self.showMessage(message="Leap daemon is not running. Attempting to start it!")
            _thread.start_new_thread(self.keep_leapd_alive, ())

        _thread.start_new_thread(self.keep_leap_runner_alive, ())


    def keep_leapd_alive(self):
        run_leapd_cmd = [
            "gksudo", "-m",
            "Your password is needed to (re)start 'leapd' and enable you to wave your hands to control your computer",
            "leapd"
        ]
        if not self.leapd:
            self.leapd = subprocess.Popen(run_leapd_cmd)

        while 1:
            self.leapd.wait()
            self.leapd = subprocess.Popen(run_leapd_cmd)


    def keep_leap_runner_alive(self):
        run_leap_runner_cmd = [
            "python2", "daemon.py"
        ]
        if not self.leapRunner:
            self.leapRunner = subprocess.Popen(run_leap_runner_cmd)

        while 1:
            self.leapRunner.wait()
            self.leapRunner = subprocess.Popen(run_leap_runner_cmd)


    def a_thread(self, name):
        words = self.dialogue.listen()
        self.command_center.run(words)


    def isLeapDaemonRunning(self):
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "leapd":
                return True
        return False


    def initUi(self):
        self.createIconGroupBox()

        self.createActions()
        self.createTrayIcon()

        self.showIconCheckBox.toggled.connect(self.trayIcon.setVisible)
        self.trayIcon.activated.connect(self.iconActivated)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.iconGroupBox)
        self.setLayout(mainLayout)

        self.setIcon(QIcon(':/images/icon.png'), "Touchless System Controller")

        self.trayIcon.show()

        self.setWindowTitle("ZTSC - Touchless System Controller")
        self.resize(400, 300)


    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super(Window, self).setVisible(visible)


    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QMessageBox.information(self, "ZTSC",
                    "The program will keep running in the system tray. To "
                    "terminate the program, choose <b>Quit</b> in the "
                    "context menu of the system tray entry.")
            self.hide()
            event.ignore()


    def setIcon(self, icon, tooltip):
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

        self.trayIcon.setToolTip(tooltip)


    def iconActivated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.trayIcon.showMessage("I'm listening...", "", QIcon(), 1500)
            _thread.start_new_thread(self.a_thread, ("thread",))
        elif reason == QSystemTrayIcon.MiddleClick:
            print("middle click")
        else:
            print("other clicks")


    def showMessage(self, title = None, message = None, icon = QSystemTrayIcon.Information, duration = 6000):
        # prepend app name to message title
        title = self.name + ((" - " + title) if title else "")

        self.trayIcon.showMessage(title, message, icon, duration)


    def createIconGroupBox(self):
        self.iconGroupBox = QGroupBox("Tray Icon")

        self.iconLabel = QLabel("Icon:")

        self.showIconCheckBox = QCheckBox("Show icon")
        self.showIconCheckBox.setChecked(True)

        iconLayout = QHBoxLayout()
        iconLayout.addWidget(self.iconLabel)
        iconLayout.addStretch()
        iconLayout.addWidget(self.showIconCheckBox)
        self.iconGroupBox.setLayout(iconLayout)


    def createActions(self):
        self.minimizeAction = QAction("Mi&nimize", self, triggered=self.hide)
        self.maximizeAction = QAction("Ma&ximize", self, triggered=self.showMaximized)
        self.restoreAction = QAction("&Restore", self, triggered=self.showNormal)
        self.quitAction = QAction("&Quit", self, triggered=self.quitApp)


    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)


    def quitApp(self):
        # TODO close leapd if started it?
        if self.leapd:
            self.leapd.kill()
            self.leapd.wait()

        if self.leapRunner:
            self.leapRunner.kill()
            self.leapRunner.wait()

        QApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    try:
        print("Checking for nltk")
        nltk.sent_tokenize("What a sentence? What a sentence.")
        print("Got nltk!")
    except LookupError:
        print("Downloading nltk")
        nltk.download("punkt")
        print("Downloaded nltk!")

    sys.exit(app.exec_())
