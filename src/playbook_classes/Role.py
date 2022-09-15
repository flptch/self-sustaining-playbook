import yaml
from yaml.loader import SafeLoader
from role_classes.RoleTask import RoleTask
from role_classes.RoleHandler import RoleHandler
import lib
from copy import deepcopy

from yamlable import *

@yaml_info(yaml_tag_ns='')
class Role(YamlAble):
    """The class, which represents the Role
    """
    def __init__(self, name, when=None, tags=None):
        """The constructor

        Args:
            name (string): name of the role
        """
        self.name = name
        self.when = when
        self.tags = tags
        self.roleTasks = self.createRoleTaskObjects()
        self.roleHandlers = self.createRoleHandlerObjects()

    def createRoleHandlerObjects(self):
        """ Creates the role handler objects

        Returns:
            List: the list of the handler Objects defined in the role
        """
        roleHandlers = []
        try:
            with open('../roles/{}/handlers/main.yml'.format(self.name)) as file:
                roleHandlersMainFile = yaml.load(file, Loader=SafeLoader)
                for i in roleHandlersMainFile:
                    roleHandlers.append(RoleHandler(i))
        except:
            pass

        return roleHandlers
    def createRoleTaskObjects(self):
        """Creates RoleTask objects

        Returns:
            List: the list of task Objects defined the role
        """
        roleTasks = []
        with open('../roles/{}/tasks/main.yml'.format(self.name)) as f:
            roleMainFile = yaml.load(f, Loader=SafeLoader)
        try:
            for i in roleMainFile:
                roleTasks.append(RoleTask(i))            
        except:
            pass

        return roleTasks
    def getRoleTasks(self):
        """Returns the list of the tasks defined in the role

        Returns:
            List: the tasks
        """
        return self.roleTasks
    
    def getRoleHandlers(self):
        """Returns the list of the handlers defined in the role

        Returns:
            List: the handlers
        """
        return self.roleHandlers

    '''def wrapRoleTaskToBlock(self, name,counterOfReboots):
        """Creates the block of commands, which increment the global counter and reboot the control host

        Args:
            name (string): name of the task
            counterOfReboots (int): the numner of the reboot
        """
        for i in self.roleTasks:
            if i.name == name:
                i.body = {'block': [lib.incrementCounterTask, lib.rebootTask],
                          'when': 'rebootCounter == {}'.format(counterOfReboots)}
'''
    def addBlock(self, index, condition=None):
        """Insert the block of tasks at, which increment the global counter and initiate the reboot, a certain place

        Args:
            index (int): The position of block in roleTasks list
            condition (string, optional): When condition. Defaults to None.
        """
        # deepcopy creation because of YAML bs
        tmpRebootTask = deepcopy(lib.rebootTask)
        if not condition == None:
            self.roleTasks.insert(index, RoleTask({'block': [self.returnIncrementCounterTask(lib.counterOfReboots + 1), tmpRebootTask],
                                          'when': condition + ' ' + 'and' + ' ' + 'rebootCounter == {}'.format(lib.counterOfReboots)}))
        else:
            self.roleTasks.insert(index, RoleTask({'block': [self.returnIncrementCounterTask(lib.counterOfReboots + 1), tmpRebootTask],
                                                   'when': 'rebootCounter == {}'.format(lib.counterOfReboots)}))

    def returnIncrementCounterTask(self, counterOfReboots):
        """Method which returns the task, which increments the global counter

        Args:
            counterOfReboots (int): the number of the reboot

        Returns:
            YAML task: the task, which increments the counter
        """
        return {
                "name" : "increment the reboot counter",
                "lineinfile": {
                    "dest": "inventory",
                    "regexp:": "rebootCounter",
                    "line": "rebootCounter = {}".format(counterOfReboots)
    }
}

    def __to_yaml_dict__(self):
        """Method which controls what to dump

        Returns:
            YAML: dumped yaml
        """
        if self.when is None and self.tags is None:
            return {'role': self.name}
        elif self.tags is None:
            return {'role': self.name,
                    'when': self.when}
        elif self.when is None:
            return {'role': self.name,
                    'tags': self.tags}
        else:
            return {'role': self.name,
                    'tags': self.tags,
                    'when': self.when}

    def __str__(self):
        """The string representation of the Role objects

        Returns:
            string: the name of the role
        """
        return self.name