class RoleTask():
    """The class, which represents the task defined in the role
    """
    def __init__(self, body):
        """The constructor

        Args:
            body (YAML): the YAML representation of the task
        """
        self.body = body
        self.name = self.body['name']
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
        """Finds out if the task initiates reboot via reboot module

        Returns:
            bool: True - if the task initiates reboot via reboot module, False - otherwise
        """
        for i in self.body:
            if i == "reboot":
                return True
        return False
    
    def usesHandler(self):
        """Finds out if the task notifies the handler

        Returns:
            bool: True - if the task notifies some handler, False - otherwise
        """
        for i in self.body:
            if i == "notify":
                self.notifiedHandler = self.body['notify']
                return True
        return False

    def __str__(self):
        """The string representation of the RoleTask object

        Returns:
            string: the string representation of the RoleTask object
        """
        return self.body