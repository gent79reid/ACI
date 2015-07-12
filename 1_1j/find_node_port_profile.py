#!/usr/bin/env python
from __future__ import print_function
from collections import defaultdict
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.model.infra import LeafS, NodeBlk, RsAccPortP
from cobra.mit.request import DnQuery
import requests
import re
requests.packages.urllib3.disable_warnings()

debug = False

def main(host, username, password, node, interface):
    apic = "https://%s" % host
    print("Connecting to APIC : %s" % apic)
    moDir = MoDirectory(LoginSession(apic, username, password))
    moDir.login()

    nodeblk_dict = defaultdict(list)
    nodeblk_list = moDir.lookupByClass("infraNodeBlk")
    node_found = False
    for nodeblkMO in nodeblk_list:
        if int(nodeblkMO.from_) > int(node) or int(nodeblkMO.to_) < int(node):
            continue
        else:
            node_found = True
            node_dn = '/'.join(str(nodeblkMO.dn).split('/')[:3])
            nodeblk_dict[node_dn].append(str(nodeblkMO.dn))
    if node_found is False:
        print("Switch Node {", node, "} DOES NOT exist!")
        exit(1)
    if debug is True:
        print("Printing nodeblk_dict.......")
        for key, value in nodeblk_dict.items():
            print(key, ":", value)
        print("-----------------------------")

    port_dict = {}
    RsAccPortP_list = moDir.lookupByClass("infraRsAccPortP")
    for RsAccPortPMO in RsAccPortP_list:
        portk = str(str(RsAccPortPMO.dn).split('[')[1])[:-1]
        port_dict[portk] = '/'.join(str(RsAccPortPMO.dn).split('/')[:3])

    if debug is True:
        print("Printing port_dict.......")
        for key, value in port_dict.items():
            print(key, ":", value)

        print("-----------------------------")

    Portblk_list = moDir.lookupByClass("infraPortBlk")
    interface_found = False
    for temp_port in Portblk_list:
        if int(interface) == int(temp_port.fromPort):
            interface_found = True
            intP = '/'.join(str(temp_port.dn).split('/')[:3])
            if port_dict[intP] in nodeblk_dict:
                m = re.match("accportprof-(?P<first>.+)", str(temp_port.dn).split('/')[2])
                print("Interface Profile Name => ", m.group("first"))
                print("Interface Profile DN =>", intP)
                n = re.match("nprof-(?P<first>.+)", str(port_dict[intP]).split('/')[2])
                print("Switch Node Profile Name =>", n.group("first"))
                print("Switch Node Profile DN =>", port_dict[intP])
    if interface_found is False:
        print("Interface {", interface, "} DOES NOT exist!")
        exit(1)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser("find_node_port_profile")
    parser.add_argument('-d', '--host', help='APIC host IP address', required=True)
    parser.add_argument('-u', '--username', help='APIC login account', required=True)
    parser.add_argument('-p', '--password', help='APIC login password', required=True)
    parser.add_argument('-n', '--node', help='APIC login password', required=True)
    parser.add_argument('-i', '--interface', help='APIC login password', required=True)
    parser.add_argument('-b', '--debug', action='store_true', help='Turn on debug')
    args = parser.parse_args()

    if args.debug:
        debug = True

    main(args.host, args.username, args.password, args.node, args.interface)
