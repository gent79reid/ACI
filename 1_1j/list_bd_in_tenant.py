#!/usr/bin/env python
from __future__ import print_function
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.model.fv import Tenant, BD
from cobra.mit.request import DnQuery

import requests
requests.packages.urllib3.disable_warnings()

def main(host, username, password, tenant):
    apic = "https://%s" % host
    print("Connecting to APIC : %s" % apic)
    moDir = MoDirectory(LoginSession(apic, username, password))
    moDir.login()

    t_obj_list = moDir.lookupByClass("fvTenant")
    for t_mo in t_obj_list:
        if t_mo.name == tenant:
            bd_list = moDir.lookupByClass("fvBD", t_mo.dn)
            for mo in bd_list:
                print("NAME: {:10s}".format(mo.name))
                print("DN: {:10s}".format(mo.dn))
                print("MAC: {:10s}".format(mo.mac))
                print("UID: {:10s}".format(mo.uid))
                print("arpFlood: {:10s}".format(mo.arpFlood))
                print("MUT: {:10s}".format(mo.mtu))
                print()
            return



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser("list_BD")
    parser.add_argument('-d', '--host', help='APIC host IP address',required=True)
    parser.add_argument('-u', '--username', help='APIC login account',required=True)
    parser.add_argument('-p', '--password', help='APIC login password',required=True)
    parser.add_argument('-t', '--tenant', help='Tenant Name',required=True)
    args = parser.parse_args()

    main(args.host, args.username, args.password, args.tenant)
