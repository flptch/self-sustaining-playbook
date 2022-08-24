
class Header():
    def __init__(self, hosts, tasks, pre_tasks, handlers, roles):
        self.hosts = hosts
        self.tasks = tasks
        self.pre_tasks = pre_tasks
        self.handlers = handlers
        self.roles = roles

    def __str__(self):
        return ("hosts: " + str(self.hosts) + "\n"
        + "tasks: " + str(self.tasks) + "\n"
        + "pre_tasks:" + str(self.pre_tasks) + "\n"
        + "handlers: " + str(self.handlers) + "\n"
        + "roles: " + str(self.roles)   )

    def getHosts(self):
        return self.hosts
    def setHosts(self, newHosts):
        self.hosts = newHosts

    def getTasks(self):
        return self.tasks
    def setTasks(self, newTasks):
        self.tasks = newTasks

    def getPreTasks(self):
        return self.pre_tasks
    def setPreTasks(self, newPre_tasks):
        self.pre_tasks = newPre_tasks

    def getHandlers(self):
        return self.handlers
    def setHandlers(self, newHandlers):
        self.handlers = newHandlers

    def getRoles(self):
        return self.roles
    def setRoles(self, newRoles):
        self.roles = newRoles        