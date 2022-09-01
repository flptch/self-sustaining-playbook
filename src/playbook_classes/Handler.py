class Handler():
    """The class, which represents the handler defined in the playbook
    """
    def __init__(self, body):
        """The constructor

        Args:
            body (YAML): the YAML representation of the body of the handler
        """
        self.body = body
        self.name = body['name']
        self.rebootModule = self.initiateReboot()

    def initiateReboot(self):
        """Finds out if the handler initiates reboot via reboot module

        Returns:
            bool: True - if the handler initiates reboot via reboot module, False - otherwise
        """
        for i in self.body:
            if i == "reboot":
                return True
        return False

    def __str__(self):
        """returns the string representation of the Handler object
        """
        return(self.body)