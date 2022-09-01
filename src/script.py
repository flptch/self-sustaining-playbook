#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook

def rebootInPlaybookPreTasks():
    for header in Playbook.getHeaders():
        for preTask in header.getPreTasks():
            if preTask.rebootCommand and VMHostInHosts(header.getHosts()):
                x = 0
                # TODO uprava playbooku pro reboot control host
            elif preTask.rebootModule and VMHostInHosts(header.getHosts()):
                x = 1
                # TODO uprava playbooku pro reboot control host
            elif preTask.notifyHandler:
                handler = findTheHandler(preTask.notifiedHandler, listOfRoles=header.getRoles())
                if handler.rebootModule and VMHostInHosts(header.getHosts()):
                    x = 2
                    # TODO uprava playbooku pro reboot control host

def rebootInRole():
    """Finds out which role initiates the reboot
    """
    for header in Playbook.getHeaders():
        for role in header.getRoles():
            for roleTask in role.getRoleTasks():
                # role task reboots the control host via command
                if roleTask.rebootCommand and VMHostInHosts(header.getHosts()):
                    x = 0
                    # TODO uprava playbooku pro reboot control host
                # role task reboots the control host via reboot module
                elif roleTask.rebootModule and VMHostInHosts(header.getHosts()):
                    x = 1
                    #TODO uprava playbooku pro reboot control host
                elif roleTask.notifyHandler:
                    handler = findTheHandler(roleTask.notifiedHandler, role=role)
                    # role task notifies handler, which reboots the control host via reboot module
                    if handler.rebootModule and VMHostInHosts(header.getHosts()):
                        # TODO uprava playbooku pro reboot control host
                        x = 2

def findTheHandler(notifiedHandlers, listOfRoles=None, role=None):
    """Finds the handler by name and returns it

    Args:
        handlerNames (string): names of handlers 

    Returns:
        Handler: the desired handler
    """
    # looking for the handler in all of the roles
    if not listOfRoles is None:
        for role in listOfRoles:
            for handler in role.getRoleHandlers():
                for name in notifiedHandlers:
                    if name == handler.name:
                        return handler
        

    # looking for the handler in the playbook
    for header in Playbook.getHeaders():
        for handler in header.getHandlers():
            for name in notifiedHandlers:
                if handler.name == name:
                    return handler
    # looking for the handler in the role/handlers folder
    for handler in role.getRoleHandlers():
        for name in notifiedHandlers:
            if name == handler:
                return handler
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

rebootInPlaybookPreTasks()