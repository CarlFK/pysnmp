from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.asyncio.sync.cmdgen import bulkCmd, bulkWalkCmd
from pysnmp.hlapi.asyncio.transport import UdpTransportTarget
from pysnmp.hlapi.auth import CommunityData
from pysnmp.hlapi.context import ContextData
from pysnmp.smi import compiler
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType


def test_v2c_bulk_sync():
    snmpEngine = SnmpEngine()
    errorIndication, errorStatus, errorIndex, varBinds = bulkCmd(
        snmpEngine,
        CommunityData("public"),
        UdpTransportTarget(("demo.pysnmp.com", 161)),
        ContextData(),
        0,
        50,
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    assert errorIndication is None
    assert errorStatus == 0
    assert len(varBinds) == 50
    assert varBinds[0][0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"
    assert varBinds[0][0][1].prettyPrint() == "SNMPv2-SMI::internet"
    # assert isinstance(varBinds[0][0][1], ObjectIdentifier)

    snmpEngine.transportDispatcher.closeDispatcher()


def test_v2c_get_table_bulk_sync():
    snmpEngine = SnmpEngine()

    builder = snmpEngine.getMibBuilder()
    # Attach MIB compiler to SNMP Engine (MIB Builder)
    # This call will fail if PySMI is not present on the system
    compiler.addMibCompiler(builder)
    # ... alternatively, this call will not complain on missing PySMI
    # compiler.addMibCompiler(snmpEngine.getMibBuilder(), ifAvailable=True)

    builder.loadModules("IF-MIB")

    objects = bulkWalkCmd(
        snmpEngine,
        CommunityData("public"),
        UdpTransportTarget(("demo.pysnmp.com", 161)),
        ContextData(),
        0,
        4,
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(objects)

    assert errorIndication is None
    assert errorStatus == 0
    assert len(varBinds) == 1
    assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"
    assert varBinds[0][1].prettyPrint() == "SNMPv2-SMI::internet"
    # assert isinstance(varBinds[0][1], ObjectIdentifier)

    errorIndication, errorStatus, errorIndex, varBinds = next(objects)

    assert errorIndication is None
    assert errorStatus == 0
    assert len(varBinds) == 1
    assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysUpTime.0"
    # assert isinstance(varBinds[0][1], TimeTicks)

    objects_list = list(objects)
    assert len(objects_list), 50

    errorIndication, errorStatus, errorIndex, varBinds = objects_list[-1]
    assert varBinds[0][0].prettyPrint() == "IF-MIB::ifSpecific.2"

    snmpEngine.transportDispatcher.closeDispatcher()
