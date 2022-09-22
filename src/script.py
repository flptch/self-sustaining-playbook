#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook
from playbook_classes.PreTask import PreTask
from playbook_classes.Task import Task
import os
import lib
import argparse

def rebootInPlaybookPreTasks(controlHost: str):
    """Searches for reboot in the playbook pretasks and replaces it with the block of commands

    Returns:
        bool: True - if thereplacement is needed, False - otherwise
    """
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        counterOfPreTasks = 0
        for preTask in header.getPreTasks():
            # the pretask reboots the localhost via reboot module or reboot command
            if (preTask.rebootModule or preTask.rebootCommand) and controlHostInHosts(header.getHosts(), controlHost):
                changeNeeded = True
                # deletes the pretask which reboots the localhost
                header.getPreTasks().pop(counterOfPreTasks)
                # replaces the pretask with block of commands
                try:
                    header.addBlockToPreTasks(counterOfPreTasks, preTask.body['when'])
                except KeyError:
                    header.addBlockToPreTasks(counterOfPreTasks)
                lib.counterOfReboots += 1
            # the pretask notifies handler
            elif preTask.notifyHandler:
                handler = findTheHandler(preTask.notifiedHandler, listOfRoles=header.getRoles())
                # the handler reboots the localhost
                if handler.rebootModule and controlHostInHosts(header.getHosts(), controlHost):
                    changeNeeded = True
                    # deletes the notify section
                    preTask.body.pop('notify')
                    # adds the the block to pretasks, which increments the counter and reboots the localhost
                    try:
                        header.addBlockToPreTasks(counterOfPreTasks + 1, preTask.body['when'])
                    except KeyError:
                        header.addBlockToPreTasks(counterOfPreTasks + 1)
                lib.counterOfReboots += 1
        counterOfPreTasks += 1
    return changeNeeded

def rebootInPlaybookTasks(controlHost: str):
    """Searches for reboot in playbook tasks and replaces it with block of commands

    Returns:
        bool: True - if the replacement is needed, False - otherwise 
    """
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        counterOfTasks = 0
        for task in header.getTasks():
            # the tasks reboots the localhost via reboot command or reboot module
            if(task.rebootModule or task.rebootCommand) and controlHostInHosts(header.getHosts(), controlHost):
                changeNeeded = True
                # deletes the reboot task
                header.getTasks().pop(counterOfTasks)
                # replaces it with the block of command, which increments the counter and reboots the localhost
                try:
                    header.addBlockToTasks(counterOfTasks, task.body['when'])
                except KeyError:
                    header.addBlockToTasks(counterOfTasks)
                lib.counterOfReboots += 1
            # the tasks notifies the handler
            elif task.notifyHandler:
                handler = findTheHandler(task.notifiedHandler, listOfRoles=header.getRoles())
                # the notified handler reboots the localhost
                if handler.rebootModule and controlHostInHosts(header.getHosts(), controlHost):
                    changeNeeded = True
                    # deletes the notify section
                    task.body.pop('notify')
                    # adds the block of commands to tasks, which increments the counter and reboots the localhost
                    try:
                        header.addBlockToTasks(counterOfTasks + 1, task.body['when'])
                    except KeyError:
                        header.addBlockToTasks(counterOfTasks + 1)
                lib.counterOfReboots += 1
            counterOfTasks += 1
    return changeNeeded

def rebootInRole(controlHost: str):
    """Searches for reboot task in role tasks and replaces it with the block of commands

    Returns:
        bool: True - if the replacement is needed, False - otherwise
    """
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        for role in header.getRoles():
            counterOfRoleTasks = 0
            for roleTask in role.getRoleTasks():
                # role task reboots the control host via command or via reboot module
                if (roleTask.rebootModule or roleTask.rebootCommand) and controlHostInHosts(header.getHosts(), controlHost):
                    changeNeeded = True
                    role.getRoleTasks().pop(counterOfRoleTasks)
                    try:
                        role.addBlock(counterOfRoleTasks, roleTask.body['when'])
                    except KeyError:
                        role.addBlock(counterOfRoleTasks)
                    lib.counterOfReboots += 1
                elif roleTask.notifyHandler:
                    handler = findTheHandler(roleTask.notifiedHandler, role=role)
                    # role task notifies handler, which reboots the control host via reboot module
                    if handler.rebootModule and controlHostInHosts(header.getHosts(), controlHost):
                        changeNeeded = True
                        roleTask.body.pop('notify')
                        try:
                            role.addBlock(counterOfRoleTasks + 1, roleTask.body['when'])
                        except KeyError:
                            role.addBlock(counterOfRoleTasks + 1)
                        lib.counterOfReboots += 1
                counterOfRoleTasks += 1
    return changeNeeded

def findTheHandler(notifiedHandlers: list, listOfRoles: list=None, role: str=None):
    """Finds the handler by name and returns it

    Args:
        handlerNames (string): names of handlers 

    Returns:
        Handler: the handler
    """
    # looking for the handler in all of the roles
    if not listOfRoles is None:
        for role in listOfRoles:
            for handler in role.getRoleHandlers():
                if handler.name in notifiedHandlers:
                    return handler

    # looking for the handler in the playbook
    for header in PlaybookObject.getHeaders():
        for handler in header.getHandlers():
            if handler.name in notifiedHandlers:
                return handler

    # looking for the handler in the role/handlers folder
    for handler in role.getRoleHandlers():
        if handler.name in notifiedHandlers:
            return handler

def controlHostInHosts(hosts: list, controlHost: str):
    """Finds out if the list of hosts contains the control host

    Args:
        hosts (List): List of hosts in the header
        controlHost (string): the name of the control host

    Returns:
        bool: True - if vm_host is in the list hosts, False - otherwise
    """
    for host in hosts:
        if host == controlHost:
            return True
    return False

def createSystemdUnit(playbookName: str, systemdUnitLocation: str, inventoryFile: str):
    """Creates the systemd unit to the given location

    Args:
        playbookName (string): the name of the playbook
        systemdUnitLocation (string): the location where the systemd unit will be created
        inventoryFile (string): the location of the inventory file
    """

    try:
        os.mkdir('files')
    except FileExistsError:
        pass

    with open(systemdUnitLocation, 'w') as systemdUnit:
        systemdUnit.write(f'''[Unit]
Description=Run ansible playbook on boot
After=default.target
DefaultDependecies=no
Before=shutdown.target

[Service]
Type=oneshot
DISPLAY=:0
User={os.getlogin()}
ExecStart=/bin/bash -c 'DISPLAY=:0 xterm -geometry 120x50+500 -hold -e sudo ansible-playbook -i {os.path.abspath(inventoryFile)} {os.path.abspath("../created_playbook.yml")}'
User={os.getlogin()}

[Install]
WantedBy=default.target

''')


def addSystemdTasks():
    """Adds all necessary tasks, which take care of creating, enabling and removing the systemd unit
    """
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.createSystemdUnitTask))
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.enableSystemdUnitTask))
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.daemonReloadTask))
    PlaybookObject.getHeaders()[len(PlaybookObject.getHeaders()) - 1].getTasks().append(Task(lib.removeSystemdUnitTask))
    PlaybookObject.getHeaders()[len(PlaybookObject.getHeaders()) - 1].getTasks().append(Task(lib.daemonReloadTask))

def createCounterVariable(inventoryFile: str):
    """Creates the global variable Counter used by reboots conditions

    Args:
        inventoryFile (string): the location of the inventory file
    """
    with open(os.path.join(os.path.dirname("src"), lib.inventoryFile), 'r') as file:
        lines = file.readlines()

    counter = 0
    varsFound = False
    for line in lines:
        if '[all:vars]' in line:
            varsFound = True
            line.replace(line,line + "\n")
            if not lines[counter + 1] == "rebootCounter=0" + "\n":
                lines.insert(counter + 1, "rebootCounter=0" + "\n")
        counter += 1

    if not varsFound:
        lines.append("[all:vars]" + "\n")
        lines.append("rebootCounter=0" + "\n")

    with open(inventoryFile, 'w') as file:
        file.writelines(lines)

def dumpTheMainPlaybook(playbookName: str):
    """Dumps the main playbook

    Args:
        playbookName (string): the name of the playbook
    """
    # TODO right now it creates a new file for testing purposes, change "createdFile" to "playbookName" later
    with open('../created_playbook.yml', 'w') as createdFile:
        yaml.dump(PlaybookObject.getHeaders(), createdFile, sort_keys=False)

def dumpTheRoleTasks():
    """Dumps role tasks
    """
    for header in PlaybookObject.getHeaders():
        for role in header.getRoles():
            with open(f'{lib.rolesFolder}/{role.name}/tasks/main.yml', 'w') as dumpedRoleTasks:
                yaml.dump(role.getRoleTasks(), dumpedRoleTasks, sort_keys=False)

# parsing arguments
ap = argparse.ArgumentParser()
ap.add_argument('--single-playbook',action='store_true',help=' if the single playbook will be checked')
ap.add_argument('--inventory-file', metavar='',default="../inventory.ini",help='the location of the inventory file (default: ../inventory.ini)')
ap.add_argument('--roles-folder', metavar='', default='../roles', help='the location of the roles folder (default: ../roles)')
ap.add_argument('--playbooks-folder', metavar='', default='../playbooks', help='the location of the playbooks folder (default: ../playbooks)')
ap.add_argument('--systemd-unit', metavar='', default=f'files/{os.getlogin()}.service', help='the location where the systemd unit will be created (default: files)')
ap.add_argument('file', metavar='file',type=str, help='the name of the playbook')
ap.add_argument('controlHost', metavar='control_host', type=str, help='the name of the controlHost')
args = ap.parse_args()
singlePlaybookSwitch = args.single_playbook
lib.inventoryFile = args.inventory_file
lib.rolesFolder = args.roles_folder
lib.playbooksFolder = args.playbooks_folder
lib.systemdUnitLocation = args.systemd_unit
playbookName = args.file
controlHost = args.controlHost

listOfPlaybooks = []
if not singlePlaybookSwitch:
    # opening the main playbook, which includes playbooks, which will be checked
    with open(playbookName) as theMainPlaybook:
        theMainData = yaml.load(theMainPlaybook, Loader=SafeLoader)
        for header in theMainData:
            listOfPlaybooks.append(header['import_playbook'])
else:
    listOfPlaybooks.append(playbookName)
# looping through the imported playbooks
changedPlaybooks = 0
for playbookName in listOfPlaybooks:
    # checking if the playbook is empty (idk why it generated empty playbooks)
    if singlePlaybookSwitch:
        if os.stat(playbookName).st_size == 0:
            continue
        else:
            with open(playbookName) as file:
                data = yaml.load(file, Loader=SafeLoader)
                PlaybookObject = Playbook(data)
    else:
        if os.stat(f'{lib.playbooksFolder}/{playbookName}').st_size == 0:
            continue
        else:
            with open(f'{lib.playbooksFolder}/{playbookName}') as file:
                data = yaml.load(file, Loader = SafeLoader)
                # creating the playbook object
                PlaybookObject = Playbook(data)

    # checking for all possible reboots of the control host 
    if not rebootInPlaybookPreTasks(controlHost) and not rebootInPlaybookTasks(controlHost) and not rebootInRole(controlHost):
        # print('No change needed in playbook {}'.format(playbookName))
        continue

    # creating the global counter variable 
    createCounterVariable(lib.inventoryFile)
    # creating the systemd unit, which starts the playbook on boot
    createSystemdUnit(playbookName, lib.systemdUnitLocation, lib.inventoryFile)
    # adds systemd tasks to the playbook pretasks/tasks
    addSystemdTasks()
    # saving the main playbook
    dumpTheMainPlaybook(playbookName)
    # saving playbook roles and their tasks
    #dumpTheRoleTasks()
    changedPlaybooks += 1


if changedPlaybooks == 0:
    print('No change was made...')
    exit(0)