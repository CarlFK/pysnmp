"""
Bulk walk MIB
+++++++++++++

Send a series of SNMP GETBULK requests using the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for all OIDs past SNMPv2-MIB::system
* run till end-of-mib condition is reported by Agent
* based on asyncio I/O framework

Functionally similar to:

| $ snmpbulkwalk -v2c -c public -Cn0 -Cr50 \
|                demo.pysnmp.com  SNMPv2-MIB::system

"""  #
import asyncio
from pysnmp.hlapi.v1arch.asyncio import *


async def run(varBinds):
    snmpDispatcher = SnmpDispatcher()

    while True:
        iterator = await bulkCmd(
            snmpDispatcher,
            CommunityData("public"),
            UdpTransportTarget(("demo.pysnmp.com", 161)),
            0,
            50,
            *varBinds
        )

        errorIndication, errorStatus, errorIndex, varBindTable = iterator

        if errorIndication:
            print(errorIndication)
            break

        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
        else:
            for varBindRow in varBindTable:
                for varBind in varBindRow:
                    print(" = ".join([x.prettyPrint() for x in varBind]))

        varBinds = varBindTable[-1]
        if isEndOfMib(varBinds):
            break

    snmpDispatcher.transportDispatcher.closeDispatcher()


asyncio.run(run([ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr"))]))