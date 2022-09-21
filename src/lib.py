import os

counterOfReboots = 0
rolesFolder = "../roles"
playbooksFolder = "../playbooks"
inventoryFile = "inventory.ini"
systemdUnitLocation = os.path.abspath('files/{}.service').format(os.getlogin())

rebootTask = {
    "name" : "reboot the local host",
    "command" : "sudo reboot"
}

createSystemdUnitTask = {
    "name": "create the systemd unit to start the second playbook after reboot",
    "tags": "always",
    "copy": {
        "src": systemdUnitLocation,
        "dest": "/etc/systemd/system"
    }
}

enableSystemdUnitTask = {
    "name": "enable the unit to execute at reboot",
    "tags": "always",
    "command": "sudo systemctl enable {}.service".format(os.getlogin())
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
        "path": "/etc/systemd/system/{}.service".format(os.getlogin())
    }
}


