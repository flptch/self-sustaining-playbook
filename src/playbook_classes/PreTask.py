import yaml
from yamlable import *

@yaml_info(yaml_tag_ns='')
class PreTask(YamlAble):
    yaml_tag = u'!pretask'
    """The class, which represents the pretask defined in the playbook
    """
    def __init__(self, body: dict):
        yaml.emitter.Emitter.prepare_tag = lambda self, tag: ''
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
        """Finds out if the pretask initiates reboot via command

        Returns:
            bool: True - if the pretask initiates the reboot via command, False - otherwise
        """
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

    def __to_yaml_dict__(self):
        """Method which controls what to dump

        Returns:
            YAML: dumped yaml
        """
        return self.body

    def __repr__(self):    
        return f"{type(self).__name__} - {dict(a=self.name, b=self.body)}"