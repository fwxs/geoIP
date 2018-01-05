#! /usr/bin/env python3

import subprocess
import re
import requests
import sys
import tarfile


class CityLocation:
    def __init__(self, cityData):
        self.cityData = cityData
        self.getCityData()

    def _getLocation(self, value):
        """
        Parse 'location' key values.
        :param value: Maxminddb location key.
        """
        print("\033[0;32m[*]\033[0;0m Timezone: ", value["time_zone"])
        print("\033[0;32m[*]\033[0;0m Latitude: {0}\tLongitude: {1}".format(value["latitude"], value["longitude"]))
        print("\033[0;32m[*]\033[0;0m Accuracy radius: {} km".format(value["accuracy_radius"]))

    def _getSubdivisions(self, value):
        """
        Enumerate the subdivisions.
        :param value: 'Subdivisions key' values.
        """
        i = 1
        print("\033[1;34m[*]\033[0;0m Subdivisions")

        for sub in value:
            print("\t[+] Subdivision No{0}: {1}".format(i, sub["names"]["en"]))

    def getCityData(self):
        """
        Parse GeoLite2-city database data.
        """
        for key, value in self.cityData.items():

            if key == "location":
                self._getLocation(value)
            elif key == "subdivisions":
                self._getSubdivisions(value)
            elif key == "postal":
                print("\033[0;34m[*]\033[0;0m Postal code: ", value["code"])
            else:
                print("\033[0;34m[*]\033[0;0m {0}: {1}".format(key.title(), value["names"]["en"]))


def downloadDatabase(dbType):
    """
    Download provided database name.
    :param dbType: Database name [City or ASN].
    :return: Database filename.
    """
    url = "http://geolite.maxmind.com/download/geoip/database/GeoLite2-{}.tar.gz".format(dbType)
    print("[*] Downloading {} database.".format(dbType))
    try:
        response = requests.get(url, stream=True)
        outputFile = "GeoLite2-{0}-.tar.gz".format(dbType)

        with open(outputFile, "wb") as file:
            bytesRead = 0
            for chunk in response.iter_content(chunk_size=200):
                bytesRead += len(chunk)
                file.write(chunk)
                print("Bytes written: {0}\r".format(bytesRead), flush=True)

        print("[*] File {} created.".format(outputFile))
        return outputFile

    except Exception as genErr:
        print(genErr, file=sys.stderr)
        exit(0)


def decompress(file):
    """
    Decompress the GeoLite2-[City, ASN].tar.gz
    :param file: Filename.
    :return: Decompressed filename.
    """
    mmdbName = re.compile("GeoLite2-(ASN|City|Country)\.mmdb$")

    with tarfile.open(file, mode="r:gz") as gzFile:
        for member in gzFile.getmembers():

            if re.search(mmdbName, member.name):
                name = member.name.rpartition("/")[0]

                print("[*] Decompressing {}.".format(name))
                gzFile.extract(member.name)

                return member.name


def moveDBFile(mmdbName):
    """
    Move the database file to the script directory.
    :param mmdbName: Database filename.
    """
    args = ["mv", mmdbName, "."]
    subprocess.Popen(args)
    directory = mmdbName.rpartition("/")[0]
    subprocess.Popen(["rm", "-r", directory])


def getCityDatabase():
    file = downloadDatabase("City")
    moveDBFile(decompress(file))


def getAsnDatabase():
    file = downloadDatabase("ASN")
    moveDBFile(decompress(file))
