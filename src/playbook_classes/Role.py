import yaml
from yaml.loader import SafeLoader

from role_classes.RoleTask import RoleTask

class Role:
    def __init__(self, name):
        self.name = name
        self.roleTasks = self.createRoleTaskObjects()

    def createRoleTaskObjects(self):
        roleTasks = []
        with open('../roles/{}/tasks/main.yml'.format(self.name)) as f:
            roleMainFile = yaml.load(f, Loader=SafeLoader)
        try:
            for i in roleMainFile:
                roleTasks.append(RoleTask(i['name']))
        except:
            pass

        return roleTasks
    def getRoleTasks(self):
        return self.roleTasks
    def __str__(self):
        return self.name