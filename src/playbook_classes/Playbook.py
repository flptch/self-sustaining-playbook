#!/usr/bin/env python3
from yaml.loader import SafeLoader
from playbook_classes.Handler import Handler
from playbook_classes.Header import Header
from playbook_classes.Host import Host
from playbook_classes.Role import Role
from playbook_classes.Task import Task
from playbook_classes.PreTask import PreTask
import yaml
from yamlable import *

@yaml_info(yaml_tag_ns='')
class Playbook(YamlAble):
    counterOfReboots = 0
    """The class, which represents the whole playbook
    """
    def __init__(self, headers):
        """The constructor

        Args:
            name (string): the name of the playbook
            headers (YAML): YAML representation of the playbook
        """
        self.headers = self.createHeaderObjects(headers)

    def createHeaderObjects(self, headers):
        """Creates the header objects

        Args:
            headers (YAML): YAML representation of the playbook
        """
        tmpHeaders = []
        for i in range(len(headers)):
            tmpHeader = Header(self.createHostObjects(headers[i]['hosts']), [], [], [], [], [], [])
            try:
                # TODO kinda sus
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
            try:
                tmpHeader.setRoles(self.createRoleObjects(headers[i]['roles']))
            except:
                tmpHeader.setRoles([])
            try:
                tmpHeader.setEnvironment(headers[i]['environment'])
            except:
                #TODO
                tmpHeader.setEnvironment('')
            try:
                tmpHeader.setAnyErrorsFatal(headers[i]['any_errors_fatal'])
            except:
                #TODO
                tmpHeader.setAnyErrorsFatal('')

            tmpHeaders.append(tmpHeader)

        return tmpHeaders

    def createHostObjects(self, hosts):
        """Creates the header hosts objects

        Args:
            hosts (List): the list of the hosts of the particular header

        Returns:
            List: the list of Hosts objects
        """
        listOfHosts = []
        #hosts = hosts.split(",")
        #for i in range(len(hosts)):
        hosts = hosts.split(',')
        for host in hosts:
            listOfHosts.append((host))

        return listOfHosts

    def createPreTaskObjects(self, preTasks):
        """Creates the pretasks objects

        Args:
            preTasks (List): the list of tasks of the particular header

        Returns:
            List: the list of PreTask objects 
        """
        listOfPreTasks = []
        for i in range(len(preTasks)):
            listOfPreTasks.append(PreTask(preTasks[i]))

        return listOfPreTasks

    def createHandlerObjects(self, handlers):
        """Creates the handler objects

        Args:
            handlers (List): the list of handlers of the particular header

        Returns:
            List: the list of the Handler objects
        """
        listOfHandlers = []
        for i in range(len(handlers)):
            listOfHandlers.append(Handler(handlers[i]))

        return listOfHandlers

    def createRoleObjects(self, roles):
        """Creates the Role objects

        Args:
            roles (List): _

        Returns:
            _type_: _description_
        """
        listOfRoles = []
        for i in range(len(roles)):
            try:
                listOfRoles.append(Role(roles[i]['role'], roles[i]['when']))
            except:
                listOfRoles.append(Role(roles[i]['role']))

        return listOfRoles

    def getName(self):
        """Returns the name of the playbook

        Returns:
            string: the name of the playbook
        """
        return self.name

    def getHeaders(self):
        """Returns the list of playbook headers

        Returns:
            List: the list of playbook headers
        """
        return self.headers
    