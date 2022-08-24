class Task():
    def __init__(self, name, module):
        self.name = name
        self.module = module

    def __str__(self):
        return ("name: " + self.name + "\n"
        + self.module)