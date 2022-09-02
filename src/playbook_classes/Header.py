import yaml
from yamlable import *

@yaml_info(yaml_tag_ns='')

class Header(YamlAble):
    """The class, which represents the header in the playbook
    """
    def __init__(self, hosts, tasks, pre_tasks, handlers, roles, environment, any_errors_fatal):
        """The constructor

        Args:
            hosts (List): the list of hosts
            tasks (List): the list of tasks
            pre_tasks (List): the list of pretasks
            handlers (List): the list of handlers
            roles (List): the list of roles
            environment(string): describes the environment
            any_errors_fatal(bool): the value of the variable
        """
        self.hosts = hosts
        self.tasks = tasks
        self.pre_tasks = pre_tasks
        self.handlers = handlers
        self.roles = roles
        self.environment = environment
        self.any_errors_fatal = any_errors_fatal
    
    def __to_yaml_dict__(self):
        return {'hosts': self.hosts[0],
                'tasks': self.tasks,
                'pre_tasks': self.pre_tasks,
                'handlers': self.handlers,
                'roles': self.roles,
                'environment': self.environment,
                'any_errors_fatal': self.any_errors_fatal}


    def __str__(self):
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
    def setHosts(self, newHosts):
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
    def setTasks(self, newTasks):
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
    def setPreTasks(self, newPre_tasks):
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
    def setHandlers(self, newHandlers):
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

    def setRoles(self, newRoles):
        """Sets the roles in the header

        Args:
            newRoles (List): List of new roles
        """
        self.roles = newRoles 
    
    def setEnvironment(self, newEnvironment):
        """Sets the environment in the header

        Args:
            newEnvironment (string): new environment
        """
        self.environment = newEnvironment

    def setAnyErrorsFatal(self, newAnyErrorsFatal):
        """Sets the any_errors_fatal variable in the header

        Args:
            newAnyErrorsFatal (bool): the value of the variable
        """
        self.any_errors_fatal = newAnyErrorsFatal