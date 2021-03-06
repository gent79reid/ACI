#!/usr/bin/env python
from __future__ import print_function
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import DnQuery
from cobra.model.fv import BD
import requests
requests.packages.urllib3.disable_warnings()

def main(host, username, password, tenant):
    apic = "https://%s" % host
    print("Connecting to APIC : %s" % apic)
    moDir = MoDirectory(LoginSession(apic, username, password))
    moDir.login()
    dn_name = "uni/tn-" + tenant
    print(dn_name)
    dnq = DnQuery(dn_name)
    dnq.subtree = 'children'
    tenantMO = moDir.query(dnq)
    for bdMO in tenantMO.BD:
        print("BD NAME => {", bdMO.name, "}")

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser("list_BD")
    parser.add_argument('-d', '--host', help='APIC host IP address', required=True)
    parser.add_argument('-u', '--username', help='APIC login account', required=True)
    parser.add_argument('-p', '--password', help='APIC login password', required=True)
    parser.add_argument('-t', '--tenant', help='Tenant Name', required=True)
    args = parser.parse_args()

main(args.host, args.username, args.password, args.tenant)
