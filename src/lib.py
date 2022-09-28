import os
import pwd

counterOfReboots = 0
rolesFolder = "../roles"
playbooksFolder = "../playbooks"
inventoryFile = "inventory.ini"
systemdUnitLocation = os.path.abspath(f'files/{pwd.getpwuid(os.geteuid())[0]}.service')

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
    "command": f"sudo systemctl enable {pwd.getpwuid(os.geteuid())[0]}.service"
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
        "path": f"/etc/systemd/system/{pwd.getpwuid(os.geteuid())[0]}.service"
    }
}

setCounterToZero = {
    "name": "set the global counter to zero",
    "tags": "always",
    "dest": os.path.join(os.getcwd(), inventoryFile),
                    "regexp": "rebootCounter",
                    "line": "rebootCounter=0"
}


