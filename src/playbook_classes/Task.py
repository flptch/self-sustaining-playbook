class Task():
    def __init__(self, body):
        self.body = body
        self.name = body['name']
        self.rebootModule = self.initiateReboot()
        self.notifyHandler = self.usesHandler()

    def initiateReboot(self):
        for i in self.body:
            if i == "reboot":
                return True
        return False
    
    def usesHandler(self):
        for i in self.body:
            if i == "notify":
                self.notifiedHandler = self.body['notify']
                return True
        return False

    def __str__(self):
        return ("name: " + self.body)