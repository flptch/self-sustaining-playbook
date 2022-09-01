class RoleHandler:
    def __init__(self, body):
        self.body = body
        self.name = body['name']
        print(self.name)
        self.rebootModule = self.initiateReboot()

    def initiateReboot(self):
        for i in self.body:
            if i == "reboot":
                return True
        return False

    def __str__(self):
        return self.body