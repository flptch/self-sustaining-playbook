#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Handler import Handler
from playbook_classes.Header import Header
from playbook_classes.Host import Host
from playbook_classes.Role import Role
from playbook_classes.Task import Task
from playbook_classes.PreTask import PreTask

class Playbook():
    headers = []
    def __init__(self, name, headers):
        self.name = name
        self.createHeaderObjects(headers)

    def createHeaderObjects(self, headers):
        for i in range(len(headers)):
            tmpHeader = Header(self.createHostObjects(headers[i]['hosts']), [], [], [], [])
            try:
                tmpHeader.setTasks(Task(headers[i]['tasks']))
            except:
                tmpHeader.setTasks([])
            try:
                tmpHeader.setPreTasks(self.createPreTaskObjects(headers[i]['pre_tasks']))
            except:
                tmpHeader.setPreTasks([])
            try:
                tmpHeader.setHandlers(self.createHandlerObjects(headers[i]['handlers']))
            except:
                tmpHeader.setHandlers([])
            #try:
            tmpHeader.setRoles(self.createRoleObjects(headers[i]['roles']))
            #except:
            #    tmpHeader.setRoles([])
            
            self.headers.append(tmpHeader)

    def createHostObjects(self, hosts):
        listOfHosts = []
        hosts = hosts.split(",")
        for i in range(len(hosts)):
            listOfHosts.append(Host(hosts[i]))

        return listOfHosts

    def createPreTaskObjects(self, preTasks):
        listOfPreTasks = []
        for i in range(len(preTasks)):
            listOfPreTasks.append(PreTask(preTasks[i]['name'], preTasks[i]['meta'], preTasks[i]['when']))

        return listOfPreTasks

    def createHandlerObjects(self, handlers):
        listOfHandlers = []
        for i in range(len(handlers)):
            listOfHandlers.append(Handler(handlers[i]['name']))

        return listOfHandlers

    def createRoleObjects(self, roles):
        listOfRoles = []
        for i in range(len(roles)):
            listOfRoles.append(Role(roles[i]['role']))

        return listOfRoles

    def getName(self):
        return self.name

    def getHeaders(self):
        return self.headers