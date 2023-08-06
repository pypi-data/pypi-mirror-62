#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a class that can log you into work"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


import os
from pynput.keyboard import Key, Controller
import time


class Work_Login:
    """Class that performs functions for login"""

    def __init__(self, conf_path="/etc/work_loging.conf"):
        """Saves config file location"""

        self.conf_path = conf_path
        self.keyboard = Controller()

    def login(self):
        """Logs user in through terminal"""

        # Configures config file if not done so already
        self.configure()
        # Opens a terminal
        os.system("gnome-terminal")
        with open(self.conf_path, "r") as f:
            for cmd in f:
                self._run_cmd(cmd)

    def configure(self):
        """Configures file that will contain commands to run"""

        # I know I could be using proper logging
        # But this is supposed to be a quick package
        if not os.path.exists(self.conf_path):
            print("It appears that you have not configured your work login")
            print("Note that this is only for logging in through a terminal")
            print("Please enter the commands, separated by the enter key")
            cmds = [input("Next command, or hit enter:\n")]
            # Ugh neesd 3.6 compatibility, but with 3.8 could use walrus here
            while cmds[-1] != "":
                cmds.append(input("Next command, or hit enter:\n"))
            with open(self.conf_path, "w") as f:
                f.write("\n".join(cmds))

    def _run_cmd(self, cmd, keyboard):
        """Runs a command slowly so as not to error"""

        for c in cmd:
            self.keyboard.press(c)
            time.sleep(.1)
            self.keyboard.release(c)
            time.sleep(.1)
        self.keboard.press(Key.enter)
        time.sleep(2)
