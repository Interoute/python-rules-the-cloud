#! /usr/bin/env python
# Python script for the Interoute Virtual Data Centre API:
#   Name: vm_deploy.py
#   Purpose: Deploy a virtual machine
#   Requires: class VDCApiCall in the file vdc_api_call.py
# For download and information: 
#   http://cloudstore.interoute.com/main/knowledge-centre/library/vdc-api-python-scripts
#
# Copyright (C) Interoute Communications Limited, 2014

from __future__ import print_function
import vdc_api_call as vdc
import getpass
import json
import os
import pprint

if __name__ == '__main__':
    cloudinit_scripts_dir = 'cloudinit-scripts'
    config_file = os.path.join(os.path.expanduser('~'), '.vdcapi')
    if os.path.isfile(config_file):
        with open(config_file) as fh:
            data = fh.read()
            config = json.loads(data)
            api_url = config['api_url']
            apiKey = config['api_key']
            secret = config['api_secret']
            try:
                cloudinit_scripts_dir = config['cloudinit_scripts_dir']
            except KeyError:
                pass
    else:
        print('API url (e.g. http://10.220.18.115:8080/client/api):', end='')
        api_url = raw_input()
        print('API key:', end='')
        apiKey = raw_input()
        secret = getpass.getpass(prompt='API secret:')

    # Create the api access object
    api = vdc.VDCApiCall(api_url, apiKey, secret)

    # Get the desired hostname of the VM
    vm_hostname = raw_input('Enter the desired VM hostname:')

    # Get the VM description
    vm_description = raw_input('Enter the desired VM description:')

    # Get the zone ID- you can find these IDs using the zone_get_all.py script
    zone_id = raw_input('Enter the zone ID:')

    # Get the template ID- you can find these IDs using the template_get_by_zone.py
    # script
    template_id = raw_input('Enter the template ID:')

    # Get the service offering ID- you can find these using the
    # service_offering_get_all.py script
    service_offering_id = raw_input('Enter the service offering ID:')

    # Deploy the VM

    request = {
        'serviceofferingid': service_offering_id,
        'templateid': template_id,
        'zoneid': zone_id,
        'displayname': vm_description,
        'name': vm_hostname
    }

    result = api.deployVirtualMachine(request)

    pprint.pprint(api.wait_for_job(result['jobid']))
