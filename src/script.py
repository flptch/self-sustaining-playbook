#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook
from playbook_classes.PreTask import PreTask
from playbook_classes.Task import Task
import os
import lib
import argparse

def rebootInPlaybookPreTasks():
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        counterOfPreTasks = 0
        for preTask in header.getPreTasks():
            if (preTask.rebootModule or preTask.rebootCommand) and VMHostInHosts(header.getHosts()):
                changeNeeded = True
                header.getPreTasks().pop(counterOfPreTasks)
                try:
                    header.addBlockToPreTasks(counterOfPreTasks, preTask.body['when'])
                except KeyError:
                    header.addBlockToPreTasks(counterOfPreTasks)
                lib.counterOfReboots += 1
            elif preTask.notifyHandler:
                handler = findTheHandler(preTask.notifiedHandler, listOfRoles=header.getRoles())
                if handler.rebootModule and VMHostInHosts(header.getHosts()):
                    changeNeeded = True
                    preTask.body.pop('notify')
                    try:
                        header.addBlockToPreTasks(counterOfPreTasks + 1, preTask.body['when'])
                    except KeyError:
                        header.addBlockToPreTasks(counterOfPreTasks + 1)
                lib.counterOfReboots += 1
        counterOfPreTasks += 1
    return changeNeeded

def rebootInPlaybookTasks():
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        counterOfTasks = 0
        for task in header.getTasks():
            if(task.rebootModule or task.rebootCommand) and VMHostInHosts(header.getHosts()):
                changeNeeded = True
                header.getTasks().pop(counterOfTasks)
                try:
                    header.addBlockToTasks(counterOfTasks, task.body['when'])
                except KeyError:
                    header.addBlockToTasks(counterOfTasks)
                lib.counterOfReboots += 1
            elif task.notifyHandler:
                handler = findTheHandler(task.notifiedHandler, listOfRoles=header.getRoles())
                if handler.rebootModule and VMHostInHosts(header.getHosts()):
                    changeNeeded = True
                    task.body.pop('notify')
                    try:
                        header.addBlockToTasks(counterOfTasks + 1, task.body['when'])
                    except KeyError:
                        header.addBlockToTasks(counterOfTasks + 1)
                lib.counterOfReboots += 1
            counterOfTasks += 1
    return changeNeeded

def rebootInRole():
    """Finds out which role initiates the reboot
    """
    changeNeeded = False
    for header in PlaybookObject.getHeaders():
        for role in header.getRoles():
            counterOfRoleTasks = 0
            for roleTask in role.getRoleTasks():
                # role task reboots the control host via command or via reboot module
                if (roleTask.rebootModule or roleTask.rebootCommand) and VMHostInHosts(header.getHosts()):
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
                    if handler.rebootModule and VMHostInHosts(header.getHosts()):
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
    #TODO dodelat

def VMHostInHosts(hosts):
    # TODO localhost == vmhost???
    """Finds out if the list of hosts contains the vm_host (localhost?)

    Args:
        hosts (List): List of hosts in the header

    Returns:
        bool: True - if vm_host is in the list hosts, False - otherwise
    """
    for host in hosts:
        if host == 'vm_host':
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
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.createSystemdUnitTask))
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.enableSystemdUnitTask))
    PlaybookObject.getHeaders()[0].getPreTasks().append(PreTask(lib.daemonReloadTask))
    PlaybookObject.getHeaders()[len(PlaybookObject.getHeaders()) - 1].getTasks().append(Task(lib.removeSystemdUnitTask))
    PlaybookObject.getHeaders()[len(PlaybookObject.getHeaders()) - 1].getTasks().append(Task(lib.daemonReloadTask))

def createCounterVariable():
    #TODO pripravit to na vice use cases
    """Creates the global variable Counter used by reboots conditions,
    """
    with open('../inventory.ini', 'r+') as inventoryFile:
        lastLine = inventoryFile.readlines()[-1]
        if not lastLine == "rebootCounter=0" + "\n":
            inventoryFile.write("rebootCounter=0" + "\n")

def dumpTheMainPlaybook(playbookName):
    """Dumps the main playbook
    """
    # dumping the main playbook
    # TODO change to playbook name and error catch
    with open('../created_playbook.yml', 'w') as createdFile:
        yaml.dump(PlaybookObject.getHeaders(), createdFile, sort_keys=False)

def dumpTheRoleTasks():
    for header in PlaybookObject.getHeaders():
        for role in header.getRoles():
            with open('../roles/{}/tasks/main.yml'.format(role.name), 'w') as dumpedRoleTasks:
                yaml.dump(role.getRoleTasks(), dumpedRoleTasks, sort_keys=False)

ap = argparse.ArgumentParser()
ap.add_argument('file', metavar='file',type=str, help='the name of the playbook')
args = ap.parse_args()
playbookName = args.file


listOfPlaybooks = []
with open(playbookName) as theMainPlaybook:
    theMainData = yaml.load(theMainPlaybook, Loader=SafeLoader)
    for header in theMainData:
        listOfPlaybooks.append(header['import_playbook'])

for playbookName in listOfPlaybooks:
    if os.stat('../playbooks/{}'.format(playbookName)).st_size == 0:
        continue
    else:
        with open('../playbooks/{}'.format(playbookName)) as file:
            data = yaml.load(file, Loader = SafeLoader)
            PlaybookObject = Playbook(data)

        if not rebootInPlaybookPreTasks() and not rebootInPlaybookTasks() and not rebootInRole():
            # print('No change needed in playbook {}'.format(playbookName))
            continue

        createCounterVariable()
        createSystemdUnit()
        addSystemdTasks()

        dumpTheMainPlaybook(playbookName)
        #dumpTheRoleTasks()


#print(yaml.dump(Playbook.getHeaders()[0], sort_keys=False))
print(lib.counterOfReboots)