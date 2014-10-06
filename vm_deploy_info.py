#! /usr/bin/env python
# Python script for the Interoute Virtual Data Centre API:
#   Name: vm_deploy_info.py
#   Purpose: List information required for deployment of a VM
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

    #THE CODE ABOVE HERE YOU DO NOT NEED TO CHANGE.

    #THE CODE BELOW IS WHERE YOU MAKE THE API CALLS AND
    #PROCESS THE DATA THAT IS IN THE RESPONSE

    
    # Zones information
    resultZones = api.listZones({})
    print("\nZONES:")
    for zone in resultZones['zone']:
        print("%s (id: %s)" % (zone['name'],zone['id']))
    
    # Templates information
    request = {'templatefilter': 'executable'}
    resultTemplates = api.listTemplates(request)

    print("\n\nTEMPLATES:")
    for template in resultTemplates['template']:
        print('%s: %s (TYPE: %s, ZONE: %s)' % (
            template['id'],
            template['name'],
            template['ostypename'],
            template['zonename']
        ))

    # Service offerings information
    resultServiceOfferings = api.listServiceOfferings({})
    print("\n\nSERVICE OFFERINGS:")
    for so in resultServiceOfferings['serviceoffering']:
        print("RAM-CPU: %s (id: %s)" % (so['name'],so['id']))
    


    

