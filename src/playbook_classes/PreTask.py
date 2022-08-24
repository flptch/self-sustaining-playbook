class PreTask():
    def __init__(self, name, meta, condition):
        self.name = name
        self.meta = meta
        self.condition = condition

    def __str__(self):
        return("name: " + self.name + "\n"
        + "meta: " + self.meta + "\n"
        + "when: " + str(self.condition))