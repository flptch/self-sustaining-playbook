import yaml
import os
from yamlable import *
from copy import deepcopy
import lib
from playbook_classes.PreTask import PreTask
from playbook_classes.Task import Task

@yaml_info(yaml_tag_ns='')

class Header(YamlAble):
    """The class, which represents the header in the playbook
    """
    def __init__(self, hosts: list):
        """The constructor

        Args:
            hosts (List): the list of hosts
        """
        self.hosts = hosts
      
    
    def __to_yaml_dict__(self):
        return {'hosts': ','.join(self.hosts),
                **({'become': self.become} if not self.become == "" else {}),
                **({'become_user': self.becomeUser} if not self.becomeUser == "" else {}),
                'tasks': self.tasks,
                'pre_tasks': self.pre_tasks,
                **({'handlers': self.handlers} if not self.handlers == [] else {}),
                **({'roles': self.roles} if not self.roles == [] else {}),
                **({'environment': self.environment} if not self.environment == "" else {}),
                **({'any_errors_fatal': self.any_errors_fatal} if not self.any_errors_fatal == "" else {})}

    def addBlockToPreTasks(self, index: int, condition: str):
        """Insert the block of tasks into the pretask section, which increment the global counter and initiate the reboot, a certain place

        Args:
            index (int): The position of block in roleTasks list
            condition (string, optional): When condition. Default is None.
        """
        # deepcopy creation because of YAML bs
        tmpRebootTask = deepcopy(lib.rebootTask)
        if not condition == None:
            self.pre_tasks.insert(index, PreTask({'block': [self.returnIncrementCounterTask(lib.counterOfReboots + 1), tmpRebootTask],
                                          'when': condition + ' ' + 'and' + ' ' + f'rebootCounter == {lib.counterOfReboots}'}))
        else:
            self.pre_tasks.insert(index, PreTask({'block': [self.returnIncrementCounterTask(lib.counterOfReboots + 1), tmpRebootTask],
                                                   'when': f'rebootCounter == {lib.counterOfReboots}'}))

    def addBlockToTasks(self, index: int, condition: str=None):
        """Insert the block of tasks into tasks section, which increment the global counter and initiate the reboot, a certain place

        Args:
            index (int): The position of block in roleTasks list
            condition (string, optional): When condition. Defaults to None.
        """
        # deepcopy creation because of YAML bs
        tmpRebootTask = deepcopy(lib.rebootTask)
        if not condition == None:
            self.tasks.insert(index, Task({'block': [self.returnIncrementCounterTask(lib.counterOfReboots + 1), tmpRebootTask],
                                          'when': condition + ' ' + 'and' + ' ' + f'rebootCounter == {lib.counterOfReboots}'}))
        else:
            self.tasks.insert(index, Task({'block': [self.returnIncrementCounterTask(lib.counterOfReboots + 1), tmpRebootTask],
                                                   'when': f'rebootCounter == {lib.counterOfReboots}'}))

    def returnIncrementCounterTask(self, counterOfReboots: int):
        """Method which returns the task, which increments the global counter

        Args:
            counterOfReboots (int): the number of the reboot

        Returns:
            _type_: _description_
        """
        return {
                "name" : "increment the reboot counter",
                "lineinfile": {
                    "dest": os.path.join(os.getcwd(), lib.inventoryFile),
                    "regexp": "rebootCounter",
                    "line": f"rebootCounter={counterOfReboots}"
    }
}

    def __str__(self):
        """Returns the string representation of the header object

        Returns:
            string: the representation of the object
        """
        return ("hosts: " + str(self.hosts) + "\n"
        + "tasks: " + str(self.tasks) + "\n"
        + "pre_tasks:" + str(self.pre_tasks) + "\n"
        + "handlers: " + str(self.handlers) + "\n"
        + "roles: " + str(self.roles)   )

    def getHosts(self):
        """returns the list of hosts

        Returns:
            List: hosts
        """
        return self.hosts
    def setHosts(self, newHosts: list):
        """Sets the hosts of the header

        Args:
            newHosts (List): the list of new hosts
        """
        self.hosts = newHosts

    def getTasks(self):
        """returns the list of tasks of the header

        Returns:
            List: tasks
        """
        return self.tasks
    def setTasks(self, newTasks: list):
        """Sets the tasks of the header

        Args:
            newTasks (List): the list of new tasks
        """
        self.tasks = newTasks

    def getPreTasks(self):
        """Returns the list of pretasks

        Returns:
            List: pretasks
        """
        return self.pre_tasks
    def setPreTasks(self, newPre_tasks: list):
        """Sets the pretasks of the header

        Args:
            newPre_tasks (List): the list of new pretasks
        """
        self.pre_tasks = newPre_tasks

    def getHandlers(self):
        """Returns the list of the handlers defined in the header

        Returns:
            List: handlers
        """
        return self.handlers
    def setHandlers(self, newHandlers: list):
        """Sests the list of handlers

        Args:
            newHandlers (List): The list of new handlers
        """
        self.handlers = newHandlers

    def getRoles(self):
        """Returns the list of the roles of the header

        Returns:
            List: roles
        """
        return self.roles

    def setRoles(self, newRoles: list):
        """Sets the roles in the header

        Args:
            newRoles (List): List of new roles
        """
        self.roles = newRoles 
    
    def setEnvironment(self, newEnvironment: str):
        """Sets the environment in the header

        Args:
            newEnvironment (string): new environment
        """
        self.environment = newEnvironment

    def setAnyErrorsFatal(self, newAnyErrorsFatal: str):
        """Sets the any_errors_fatal variable in the header

        Args:
            newAnyErrorsFatal (bool): the value of the variable
        """
        self.any_errors_fatal = newAnyErrorsFatal

    def setBecome(self, value: str):
        """Sets the become variable in the header

        Args:
            value (bool): the bool value of the variable
        """
        self.become = value

    def setBecomeUser(self, user: list):
        """Sets the user

        Args:
            user (string): the user
        """
        self.becomeUser = user