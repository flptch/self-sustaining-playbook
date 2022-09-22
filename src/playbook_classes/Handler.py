import yaml
from yamlable import *

@yaml_info(yaml_tag_ns='')
class Handler(YamlAble):
    """The class, which represents the handler defined in the playbook
    """
    def __init__(self, body: dict):
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

    def __to_yaml_dict__(self):
        """Method which controls what to dump

        Returns:
            YAML: dumped yaml
        """
        return self.body

    def __str__(self):
        """returns the string representation of the Handler object
        """
        return(self.body)