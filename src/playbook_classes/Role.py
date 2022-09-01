import yaml
from yaml.loader import SafeLoader

from role_classes.RoleTask import RoleTask
from role_classes.RoleHandler import RoleHandler

class Role:
    def __init__(self, name):
        self.name = name
        self.roleTasks = self.createRoleTaskObjects()
        self.roleHandlers = self.createRoleHandlerObjects()

    def createRoleHandlerObjects(self):
        roleHandlers = []
        print(self.name)
        try:
            with open('../roles/{}/handlers/main.yml'.format(self.name)) as file:
                roleHandlersMainFile = yaml.load(file, Loader=SafeLoader)
                for i in roleHandlersMainFile:
                    roleHandlers.append(RoleHandler(i))
        except:
            pass

        return roleHandlers
    def createRoleTaskObjects(self):
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
        return self.roleTasks
    def __str__(self):
        return self.name