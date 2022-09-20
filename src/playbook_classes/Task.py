import yaml
from yamlable import *

@yaml_info(yaml_tag_ns='')
class Task(YamlAble):
    """The class, which represents the Task defined in the playbook
    """
    def __init__(self, body):
        """The constructor

        Args:
            body (YAML): the YAML representation of the body of the pretask
        """
        self.body = body
        if not 'block' in body:
            self.name = self.body['name']
        self.rebootModule = self.initiateReboot()
        self.notifyHandler = self.usesHandler()
        self.rebootCommand = self.commandReboot()

    def commandReboot(self):
        """Finds out if the task initiates reboot via command 

        Returns:
            bool: True - if the task initiates the reboot via command, False - otherwise
        """
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

    def __to_yaml_dict__(self):
        return self.body

    def __str__(self):
        """returns the string representation of the Task object
        """
        return self.name