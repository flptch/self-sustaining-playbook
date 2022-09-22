class RoleHandler:
    """The class, which represents the handler defined in the role/handlers folder
    """
    def __init__(self, body: dict):
        """The constructor

        Args:
            body (YAML): YAML representation of the the handler body
        """
        self.body = body
        self.name = body['name']
        self.rebootModule = self.initiateReboot()

    def initiateReboot(self):
        """Finds out if the handler initiates reboot via reboot module

        Returns:
            bool: True - if the handler initiates the reboot via reboot module, False - otherwise
        """
        for i in self.body:
            if i == "reboot":
                return True
        return False

    def __str__(self):
        """The string representation of the RoleHandler object

        Returns:
            string: representation of the RoleHandler object
        """
        return self.body