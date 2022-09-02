import yaml
from yamlable import *

@yaml_info(yaml_tag_ns='')
class Host(YamlAble):
    """The class, which represents the host in the header
    """
    def __init__(self, name):
        """The constructor

        Args:
            name (string): name of the host
        """
        self.name = name

    def __str__(self):
        """Returns the string representation of the Host object

        Returns:
            string: Returns the string representation of the Host object
        """
        return self.name

    def __to_yaml_dict__(self):
        """Method which controls what to dump

        Returns:
            YAML: dumped yaml
        """
        return self.name