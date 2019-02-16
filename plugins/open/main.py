import subprocess

from command import Command

class OpenCommand(Command):
    def __init__(self):
        self.name = "open"
        self.triggers = ["open", "run", "start"]
        self.programs = [
            ["firefox", "firefox --new-tab about:home"]
        ]


    def run(self, words):
        # search for program
        for program in self.programs:
            if words.split()[1].lower() == program[0].lower():
                self.run_subprocess(program[1])
                return

        self.run_subprocess("".join(words.split()[1:]).lower())



    def triggered(self, words):
        for trigger in self.triggers:
            if words.startswith(trigger):
                return True

        return False


    def run_subprocess(self, cmd):
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
