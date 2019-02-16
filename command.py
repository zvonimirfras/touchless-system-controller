class Command:
    def __init__(self):
        self.name = "base command"
        self.triggers = []


    def run(self, words):
        print("You should implement this function")


    def triggered(self, words):
        print("You should implement this function to return boolean")
        return False
