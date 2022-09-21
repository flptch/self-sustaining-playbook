# Self - sustaining Ansible playbook

## Description
The python script, which edits the ansible playbook, which reboots the control host. \
The script is still being implemented, the right functionality is not guaranteed.

## How to run the script
The script has two positional arguments: file - the name of the playbook, control_host - the name of the control host. \
To show all the optional arguments, run "python3 script --help"

## Examples
The playbook example:
- name: preflight checks \
  import_playbook: preflight.yml \
  when: preflight_enabled | default(true) | bool
- name: configure target hosts OS layer \
  import_playbook: infra/full_nfv.yml \
  . \
  . \
  . \

Run: python3 script.py ../playbooks/full_nfv.yml vm_host \
It will check all the included playbooks for the reboot of the control host.


Another playbook example:
- hosts: localhost \
  become: true \
  become_user: root \
  tasks: 
    - name: check the uptime before reboot \
      tags: always \
      command: "uptime" 

    - name: reboot the control host \
      tags: always \
      reboot: \
    . \
    . \
    . 

Run: python3 script.py ../playbooks/reboot_playbook.yml localhost --single-playbook \
It will check this playboook for the reboot of the control host.