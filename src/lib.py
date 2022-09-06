counterOfReboots = 0

incrementCounterTask = {
    "name" : "increment the reboot counter",
    "lineinfile": {
        "dest": "inventory",
        "regexp:": "rebootCounter",
        "line": "rebootCounter = {}".format(counterOfReboots + 1)
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


