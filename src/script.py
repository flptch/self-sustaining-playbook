#!/usr/bin/env python3
import yaml
from yaml.loader import SafeLoader
from playbook_classes.Playbook import Playbook

with open('../playbooks/infra/full_nfv.yml') as file:
    data = yaml.load(file, Loader = SafeLoader)
    Playbook = Playbook('full_nfv.yml', data)

#print(Playbook.getHeaders()[1])