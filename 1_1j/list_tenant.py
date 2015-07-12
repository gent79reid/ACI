#!/usr/bin/env python

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.internal.codec.xmlcodec import toXMLStr

import sys
import logging
import requests

# Initialize logging
logging.basicConfig()
# Set the logging level to DEBUG
logging.getLogger().setLevel(logging.DEBUG)

requests_log = logging.getLogger("requests.packages.urllib3")
# Set just the URLLIB3 logging level to INFO
requests_log.setLevel(logging.INFO)
requests_log.propagate = True

requests.packages.urllib3.disable_warnings()

aci_class = sys.argv[1]
session = LoginSession('https://172.21.208.173', 'admin','C1sc0123')
moDir = MoDirectory(session)
moDir.login()

from cobra.mit.request import ConfigRequest

#import the tenant class from the model
from cobra.model.fv import Tenant
# Get the top level policy universe directory
uniMo = moDir.lookupByDn('uni')

## create the tenant object
#fvTenantMo = Tenant(uniMo, 'test1111111111')
#fvTenantMo.delete()#

#configReq = ConfigRequest()
#configReq.addMo(fvTenantMo)
#moDir.commit(configReq)

obj_list = moDir.lookupByClass(aci_class)
#
for mo in obj_list:
	print "{} -> {}".format(mo.name,mo.dn)
