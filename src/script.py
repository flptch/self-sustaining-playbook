#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook

def rebootInRole():
    for header in Playbook.getHeaders():
        for role in header.getRoles():
            for roleTask in role.getRoleTasks():
                if roleTask.rebootModule:
                    x = 1
                    #TODO
                elif roleTask.notifyHandler:
                    handler = findTheHandler(roleTask.notifiedHandler)
                    if handler.rebootModule and VMHostInHosts(header.getHosts()):
                        print('reboot here')

def findTheHandler(notifiedHandlers):
    """Finds the handler by name and returns it

    Args:
        handlerNames (string): names of handlers 

    Returns:
        Handler: the desired handler
    """
    # looking for the handler in the playbook
    for header in Playbook.getHeaders():
        for handler in header.getHandlers():
            for name in notifiedHandlers:
                if handler.name == name:
                    return handler
    # looking for the handler in the role/handlers folder
    # TODO
    # looking for the handler in the role/tasks/main.yml file
    # TODO

def VMHostInHosts(hosts):
    """Finds out if the list of hosts contains the vm_host (locahost?)

    Args:
        hosts (List): List of hosts in the header

    Returns:
        bool: True - if vm_host is in the list hosts, False - otherwise
    """
    for host in hosts:
        if host.name == 'vm_host':
            return True
    return False

with open('../playbooks/infra/full_nfv.yml') as file:
    data = yaml.load(file, Loader = SafeLoader)
    Playbook = Playbook('full_nfv.yml', data)

rebootInRole()