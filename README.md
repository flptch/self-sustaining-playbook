# Self - sustaining Ansible playbook

## Description
The python script, which splits the Ansible playbook, which initiates the local host reboot.

## How to run the script
The script has two positional arguments: file - the name of the playbook, control_host - the name of the control host
To show all of the optional arguments, run "python3 script --help"

## Examples
python3 script.py ../playbooks/full_nfv.yml vm_host \
python3 script.py ../playbooks/infra/full_nfv.yml vm_host --single-playbook \
python3 script.py --help
