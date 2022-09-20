#!/usr/bin/env python3
from cmath import sin
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook
from playbook_classes.PreTask import PreTask
from playbook_classes.Task import Task
import os
import lib
import argparse

def rebootInPlaybookPreTasks(controlHost):
    """Searches for reboot in the playbook pretasks and replaces it with the block of commands

    Returns:
        bool: True - if thereplacement is needed, False - otherwise
    """
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        counterOfPreTasks = 0
        for preTask in header.getPreTasks():
            # the pretask reboots the localhost via reboot module or reboot command
            if (preTask.rebootModule or preTask.rebootCommand) and VMHostInHosts(header.getHosts(), controlHost):
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
                if handler.rebootModule and VMHostInHosts(header.getHosts(), controlHost):
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

def rebootInPlaybookTasks(controlHost):
    """Searches for reboot in playbook tasks and replaces it with block of commands

    Returns:
        bool: True - if the replacement is needed, False - otherwise 
    """
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        counterOfTasks = 0
        for task in header.getTasks():
            # the tasks reboots the localhost via reboot command or reboot module
            if(task.rebootModule or task.rebootCommand) and VMHostInHosts(header.getHosts(), controlHost):
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
                if handler.rebootModule and VMHostInHosts(header.getHosts(), controlHost):
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

def rebootInRole(controlHost):
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
                if (roleTask.rebootModule or roleTask.rebootCommand) and VMHostInHosts(header.getHosts(), controlHost):
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
                    if handler.rebootModule and VMHostInHosts(header.getHosts(), controlHost):
                        changeNeeded = True
                        roleTask.body.pop('notify')
                        try:
                            role.addBlock(counterOfRoleTasks + 1, roleTask.body['when'])
                        except KeyError:
                            role.addBlock(counterOfRoleTasks + 1)
                        lib.counterOfReboots += 1
                counterOfRoleTasks += 1
    return changeNeeded

def findTheHandler(notifiedHandlers, listOfRoles=None, role=None):
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
                for name in notifiedHandlers:
                    if name == handler.name:
                        return handler
        

    # looking for the handler in the playbook
    for header in PlaybookObject.getHeaders():
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
    #TODO

def VMHostInHosts(hosts, controlHost):
    """Finds out if the list of hosts contains the control host

    Args:
        hosts (List): List of hosts in the header

    Returns:
        bool: True - if vm_host is in the list hosts, False - otherwise
    """
    for host in hosts:
        if host == controlHost:
            return True
    return False

def createSystemdUnit(playbookName, systemdUnitLocation, inventoryFile):
    """Creates the systemd unit file, which takes care of executing the playbook on boot
    """

    try:
        os.mkdir('files')
    except FileExistsError:
        pass

    with open(systemdUnitLocation, 'w') as systemdUnit:
        systemdUnit.write('''[Unit]
Description=Run ansible playbook on boot
After=default.target
DefaultDependecies=no
Before=shutdown.target

[Service]
Type=oneshot
DISPLAY=:0
User={}
ExecStart=/bin/bash -c 'DISPLAY=:0 xterm -geometry 120x50+500 -hold -e sudo ansible-playbook -i {} {}'
User={}

[Install]
WantedBy=default.target

'''.format(os.getlogin(), os.path.abspath(inventoryFile),os.path.abspath(playbookName),os.getlogin()))


def addSystemdTasks():
    """Adds all necessary tasks, which take care of creating, enabling and removing the systemd unit
    """
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.createSystemdUnitTask))
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.enableSystemdUnitTask))
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.daemonReloadTask))
    PlaybookObject.getHeaders()[len(PlaybookObject.getHeaders()) - 1].getTasks().append(Task(lib.removeSystemdUnitTask))
    PlaybookObject.getHeaders()[len(PlaybookObject.getHeaders()) - 1].getTasks().append(Task(lib.daemonReloadTask))

def createCounterVariable(inventoryFile):
    """Creates the global variable Counter used by reboots conditions,
    """
    with open(inventoryFile, 'r') as file:
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

def dumpTheMainPlaybook(playbookName):
    """Dumps the main playbook
    """
    # dumping the main playbook
    # TODO change to playbook name and error catch
    with open('../created_playbook.yml', 'w') as createdFile:
        yaml.dump(PlaybookObject.getHeaders(), createdFile, sort_keys=False)

def dumpTheRoleTasks( ):
    """Dumps role tasks
    """
    for header in PlaybookObject.getHeaders():
        for role in header.getRoles():
            with open('{}/{}/tasks/main.yml'.format(lib.rolesFolder, role.name), 'w') as dumpedRoleTasks:
                yaml.dump(role.getRoleTasks(), dumpedRoleTasks, sort_keys=False)

ap = argparse.ArgumentParser()
ap.add_argument('--single-playbook',action='store_true',help=' if the single playbook will be checked')
ap.add_argument('--inventory-file', metavar='',default="../inventory.ini",help='the location of the inventory file (default: ../inventory.ini)')
ap.add_argument('--roles-folder', metavar='', default='../roles', help='the location of the roles folder (default: ../roles)')
ap.add_argument('--playbooks-folder', metavar='', default='../playbooks', help='the location of the playbooks folder (default: ../playbooks)')
ap.add_argument('--systemd-unit', metavar='', default='files/{}.service'.format(os.getlogin()), help='the location where the systemd unit will be created (default: files)')
ap.add_argument('file', metavar='file',type=str, help='the name of the playbook')
ap.add_argument('controlHost', metavar='control_host', type=str, help='the name of the controlHost')
args = ap.parse_args()
singlePlaybookSwitch = args.single_playbook
inventoryFile = args.inventory_file
lib.rolesFolder = args.roles_folder
lib.playbooksFolder = args.playbooks_folder
systemdUnitLocation = args.systemd_unit
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
        if os.stat('{}/{}'.format(lib.playbooksFolder, playbookName)).st_size == 0:
            continue
        else:
            with open('{}/{}'.format(lib.playbooksFolder, playbookName)) as file:
                data = yaml.load(file, Loader = SafeLoader)
                # creating the playbook object
                PlaybookObject = Playbook(data)

    # checking all of possible reboots 
    if not rebootInPlaybookPreTasks(controlHost) and not rebootInPlaybookTasks(controlHost) and not rebootInRole(controlHost):
        # print('No change needed in playbook {}'.format(playbookName))
        continue
    # creating the global counter variable 
    createCounterVariable(inventoryFile)
    # creating the systemd unit, which starts the playbook on boot
    createSystemdUnit(playbookName, systemdUnitLocation, inventoryFile)
    # adds systemd tasks to the playbook pretasks/tasks
    addSystemdTasks()
    # saving the main playbook
    dumpTheMainPlaybook(playbookName)
    # saving playbook roles and their tasks
    #dumpTheRoleTasks()
    changedPlaybooks += 1


#print(yaml.dump(Playbook.getHeaders()[0], sort_keys=False))
if changedPlaybooks == 0:
    print('No change was made...')
    exit(0)

print(lib.counterOfReboots)