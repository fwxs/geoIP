#!/usr/bin/env python3

import maxminddb
import os
import socket
import sys
import utils


def getCityInformation(ipdaddress):
    """
    Retrieve city information about the provided IP address.
    :param ipdaddress: address to retrieve information from.
    """
    dbName = "GeoLite2-City.mmdb"

    if not os.path.exists(dbName):
        utils.getCityDatabase()

    conx = maxminddb.open_database(dbName)

    utils.CityLocation(conx.get(ipdaddress))


def getASNInformation(ipaddress):
    """
    Get ASN information of the provided IP address.
    :param ipaddress:
    """
    dbName = "GeoLite2-ASN.mmdb"

    if not os.path.exists(dbName):
        utils.getASNDatabase()

    conx = maxminddb.open_database(dbName)
    info = conx.get(ipaddress)

    print("\n\033[0;36m[*]\033[0;0m ASN: ", info["autonomous_system_number"])
    print("\033[0;36m[*]\033[0;0m Organization: ", info["autonomous_system_organization"])


def getGeoInformation(ipAddress):
    getCityInformation(ipAddress)
    getASNInformation(ipAddress)


def getHostInformation(ipAddress):
    """
    Get the DNS name of the provided IP address.
    It'll return 'Unresolved hostname' if it doesn't have a DNS name registered.
    :param ipAddress: Address to retrieve information from.
    """

    try:
        hostname = socket.gethostbyaddr(ipAddress)

        if hostname[0] != "":
            print("\t\033[0;32m[+]\033[0;0m Host name: ", hostname[0])
            if len(hostname[1]) != 0:
                for alias in hostname[1]:
                    print("\t\033[0;32m[+]\033[0;0m Alias: ", alias)

    except socket.herror:
        print("\033[0;31mError: Unresolved hostname, probably a desktop computer\033[0;0m\n")

    except Exception as genErr:
        print("\033[0;31mError:", genErr, "\033[0;0m")
        sys.exit()


def getIPInformation(ipaddress):
    print("\033[1;32m[*]\033[0;0m IP address {} information.".format(ipaddress))

    getHostInformation(ipaddress)
    getGeoInformation(ipaddress)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} ipaddress".format(sys.argv[0]))
        sys.exit()

    getIPInformation(sys.argv[1])
