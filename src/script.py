#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook
import os

counter = 0

incrementCounterTask = {
    "name" : "increment the reboot counter",
    "lineinfile": {
        "dest": "inventory",
        "regexp:": "rebootCounter",
        "line": "rebootCounter = {}".format(counter)
    }
}

rebootTask = {
    "name" : "reboot the local host",
    "command" : "sudo reboot"
}

createSystemdUnitTask = {
    "name": "create the systemd unit to start the second playbook after reboot",
    "tags": "always",
    "copy": {
        "src": "files/filip.service",
        "dest": "/etc/systemd/system"
    }
}

enableSystemdUnitTask = {
    "name": "enable the unit to execute at reboot",
    "tags": "always",
    "command": "sudo systemctl enable filip.service"
}

daemonReloadTask = {
    "name": "reload the units",
    "tags": "always",
    "command": "sudo systemctl daemon-reload"
}

removeSystemdUnitTask = {
    "name": "delete the systemd unit",
    "tags": "always",
    "file" : {
        "state": "absent",
        "path": "/etc/systemd/system/filip.service"
    }
}

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
    Playbook.getHeaders()[0].getPreTasks().append(createSystemdUnitTask)
    Playbook.getHeaders()[0].getPreTasks().append(enableSystemdUnitTask)
    Playbook.getHeaders()[0].getPreTasks().append(daemonReloadTask)


with open('../playbooks/infra/full_nfv.yml') as file:
    data = yaml.load(file, Loader = SafeLoader)
    Playbook = Playbook('full_nfv.yml', data)

createSystemdUnit()
addSystemdTasks()
#rebootInPlaybookPreTasks()