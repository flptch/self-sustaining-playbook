# Self - sustaining Ansible playbook

## Description
The python script, which edits the ansible playbook, which reboots the control host. \
The script is still being implemented, the right functionality is not guaranteed.

## How does it work
The script searches for all the tasks, which reboot the control host, in all the playbooks and their roles. If the script finds that kind of task, it creates the global counter in the inventory file, which will set which reboot will be initiated. It also wraps the task into the block, which consists of two tasks. The first task increments the global counter and the second one is a command which initiates reboot. The whole block has a condition of the execution. The global counter has to be equal to the certain number of reboot. For example, to initiate the first reboot, the global counter has to be equal to zero. After the first reboot the global counter is incremented by one, so during the second execution of the playbook, the first reboot won't be initiated again. The script also creates the systemd unit, which starts the playbook on boot. 

## How to run the script
First you have to install all dependencies with: pip3 install -r requirements.txt \
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