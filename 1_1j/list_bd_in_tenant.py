#!/usr/bin/env python
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser("Delete BD under given Tenant instance")
    parser.add_argument('-d', '--host', help='APIC host IP address',required=True)
    parser.add_argument('-u', '--username', help='APIC login account',required=True)
    parser.add_argument('-p', '--password', help='APIC login password',required=True)
    args = parser.parse_args()

    main(args.host, args.username, args.password)
