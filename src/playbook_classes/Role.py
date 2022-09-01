import yaml
from yaml.loader import SafeLoader

from role_classes.RoleTask import RoleTask
from role_classes.RoleHandler import RoleHandler

class Role:
    """The class, which represents the Role
    """
    def __init__(self, name):
        """The constructor

        Args:
            name (string): name of the role
        """
        self.name = name
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

    def __str__(self):
        """The string representation of the Role objects

        Returns:
            string: the name of the role
        """
        return self.name