#!/usr/bin/env python

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.internal.codec.xmlcodec import toXMLStr

import sys
import logging
# Initialize logging
logging.basicConfig()
# Set the logging level to DEBUG
logging.getLogger().setLevel(logging.DEBUG)

requests_log = logging.getLogger("requests.packages.urllib3")
# Set just the URLLIB3 logging level to INFO
requests_log.setLevel(logging.INFO)
requests_log.propagate = True


aci_class = sys.argv[1]
session = LoginSession('https://172.21.208.173', 'admin','C1sc0123')
moDir = MoDirectory(session)
moDir.login()

import logging

#import the tenant class from the model
from cobra.model.fv import Tenant

# Get the top level policy universe directory
uniMo = moDir.lookupByDn('uni')

# create the tenant object
#fvTenantMo = Tenant(uniMo, 'ExampleCorp')

obj_list = moDir.lookupByClass(aci_class)
#
for mo in obj_list:
	print "{} -> {}".format(mo.name,mo.dn)
