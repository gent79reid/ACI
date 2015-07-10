#!/usr/bin/env python
from __future__ import print_function
from cobra.model.fv import Tenant, BD
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import DnQuery, ConfigRequest
import cobra.model.pol
import cobra.model.infra
from cobra.internal.codec.xmlcodec import toXMLStr
from cobra.model.fvns import VlanInstP, EncapBlk

import requests
requests.packages.urllib3.disable_warnings()

def main(host, username, password, pool_name, from_vlan, to_vlan):
    apic = "https://%s" % host
    print("Connecting to APIC : %s" % apic)
    moDir = MoDirectory(LoginSession(apic, username, password))
    moDir.login()
    topMO = moDir.lookupByDn('uni')
    moDir.lookupByDn
    infraInfra = cobra.model.infra.Infra(topMO)
    fvnsVlanInstP = VlanInstP(infraInfra,name=pool_name, allocMode="static")
    temp_from_vlan = "vlan-" + from_vlan
    temp_to_vlan = "vlan-" + to_vlan
    fvnsEncapBlk = EncapBlk(fvnsVlanInstP, temp_from_vlan, temp_to_vlan)

    print(toXMLStr(topMO))
    c = ConfigRequest()
    c.addMo(infraInfra)
    moDir.commit(c)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser("Create VLAN Pool")
    parser.add_argument('-d', '--host', help='APIC host IP address', required=True)
    parser.add_argument('-u', '--username', help='APIC login account', required=True)
    parser.add_argument('-p', '--password', help='APIC login password', required=True)
    parser.add_argument('-s', '--pool_name', help='APIC login password', required=True)
    parser.add_argument('-v', '--vlan_range', help='VLAN Range, eg 100-200', required=True)
    args = parser.parse_args()

    vlan_r = args.vlan_range
    from_vlan = vlan_r.split("-")[0]
    to_vlan = vlan_r.split("-")[1]

    main(args.host, args.username, args.password, args.pool_name, from_vlan, to_vlan)
