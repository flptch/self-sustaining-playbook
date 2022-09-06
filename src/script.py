#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook
from playbook_classes.PreTask import PreTask
from playbook_classes.Task import Task
import os
import lib

def rebootInPlaybookPreTasks():
    for header in Playbook.getHeaders():
        for preTask in header.getPreTasks():
            print(type(preTask))
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

def createSystemdUnit():
    """Creates the systemd unit file, which takes care of executing the playbook on boot
    """
    #TODO cesta (user)
    try:
        os.mkdir('files')
    except FileExistsError:
        pass

    with open('files/{}.service'.format(os.getlogin()), 'w') as systemdUnit:
        systemdUnit.write('''[Unit]
Description=Run ansible playbook on boot
After=default.target
DefaultDependecies=no
Before=shutdown.target

[Service]
Type=oneshot
DISPLAY=:0
User={}
ExecStart=/bin/bash -c 'DISPLAY=:0 xterm -geometry 120x50+500 -hold -e sudo ansible-playbook -i /home/filip/work/self-sustaining-playbook/inventory.ini /home/filip/self-sustaining-playbook/playbooks/infra/full_nfv.yml'
User={}

[Install]
WantedBy=default.target

'''.format(os.getlogin(), os.getlogin()))


def addSystemdTasks():
    """Adds all necessary tasks, which take care of creating, enabling and removing the systemd unit
    """
    Playbook.getHeaders()[0].getPreTasks().append(PreTask(lib.createSystemdUnitTask))
    Playbook.getHeaders()[0].getPreTasks().append(PreTask(lib.enableSystemdUnitTask))
    Playbook.getHeaders()[0].getPreTasks().append(PreTask(lib.daemonReloadTask))
    Playbook.getHeaders()[len(Playbook.getHeaders()) - 1].getTasks().append(Task(lib.removeSystemdUnitTask))
    Playbook.getHeaders()[len(Playbook.getHeaders()) - 1].getTasks().append(Task(lib.daemonReloadTask))

def createCounterVariable():
    #TODO pripravit to na vice use cases
    """Creates the global variable Counter used by reboots conditions,
    """
    with open('../inventory.ini', 'r+') as inventoryFile:
        lastLine = inventoryFile.readlines()[-1]
        if not lastLine == "rebootCounter=0" + "\n":
            inventoryFile.write("rebootCounter=0" + "\n")


with open('../playbooks/infra/full_nfv.yml') as file:
    data = yaml.load(file, Loader = SafeLoader)
    Playbook = Playbook(data)

createCounterVariable()
createSystemdUnit()
addSystemdTasks()

with open('../created_playbook.yml', 'w') as createdFile:
    documents = yaml.dump(Playbook.getHeaders(), createdFile)

Playbook.getHeaders()[0].getRoles()[0].wrapRoleTaskToBlock('Set defaults', lib.counterOfReboots)
print(yaml.dump(Playbook.getHeaders()[0].getRoles()[0].getRoleTasks(), sort_keys=False))

#rebootInPlaybookPreTasks()