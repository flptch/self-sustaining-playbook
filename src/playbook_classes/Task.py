class Task():
    """The class, which represents the Task defined in the playbook
    """
    def __init__(self, body):
        """The constructor

        Args:
            body (YAML): the YAML representation of the body of the pretask
        """
        self.body = body
        self.name = body['name']
        self.rebootModule = self.initiateReboot()
        self.notifyHandler = self.usesHandler()
        self.rebootCommand = self.commandReboot()

    def commandReboot(self):
        for i in self.body:
            if i == "command":
                if self.body['command'] == "sudo reboot":
                    return True
        return False

    def initiateReboot(self):
        """Finds out if the pretask initiates reboot via reboot module

        Returns:
            bool: True - if the pretask initiates reboot via reboot module, False - otherwise
        """
        for i in self.body:
            if i == "reboot":
                return True
        return False
    
    def usesHandler(self):
        """Finds out if the pretask notifies the handler

        Returns:
            bool: True - if the pretask notifies some handler, False - otherwise
        """
        for i in self.body:
            if i == "notify":
                self.notifiedHandler = self.body['notify']
                return True
        return False

    def __str__(self):
        """returns the string representation of the Task object
        """
        return ("name: " + self.body)