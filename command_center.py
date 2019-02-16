import os
import json
import importlib

from dialogue import Dialogue
from ask_duck import ask_duck


class CommandCenter:
    def __init__(self, dialogue=None):
        self.commands = []
        self.plugins_path = "plugins"
        self.load_commands()

        self.dialogue = dialogue
        if not dialogue:
            self.dialogue = Dialogue()


    def load_commands(self):
        self.commands = []

        # list plugins folder contents
        plugins_folders = filter(lambda x: os.path.isdir(self.plugins_path + "/" + x), os.listdir(self.plugins_path))

        for folder in plugins_folders:
            if folder.startswith("__"):
                continue

            module = importlib.import_module("plugins." + folder + ".main")

            for potential_command in module.__dir__():
                # find all plugin-added commands
                if not potential_command.endswith("Command") or potential_command == "Command":
                    continue

                command = getattr(module, potential_command)  # get the class out of the module
                self.commands.append(command())  # append the instance of the class


    def run(self, words):
        if not words:
            # nothing to do
            return

        print('Running words: "' + words + '"')

        command = self.find_command(words)
        if not command:
            self.default_command(words)
            return

        command.run(words)


    def default_command(self, words):
        print("default_command for", words)
        reply = ask_duck(words)

        if "Abstract" in reply and reply["Abstract"]:
            self.dialogue.say(reply["Abstract"])
        else:
            self.dialogue.say("No abstract for " + words)


    def find_command(self, words):
        # find the command based on trigger
        for command in self.commands:
            if command.triggered(words):
                return command


if __name__ == "__main__":
    cc = CommandCenter()
    cc.run("run firefox")

