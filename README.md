
SNMP Library for Python
=======================

[![Become a Sponsor](https://img.shields.io/badge/Become%20a%20Sponsor-lextudio-orange.svg?style=for-readme)](https://github.com/sponsors/lextudio)
[![PyPI](https://img.shields.io/pypi/v/pysnmp.svg)](https://pypi.python.org/pypi/pysnmp)
[![PyPI Downloads](https://img.shields.io/pypi/dd/pysnmp)](https://pypi.python.org/pypi/pysnmp/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pysnmp.svg)](https://pypi.python.org/pypi/pysnmp/)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/lextudio/pysnmp/master/LICENSE.rst)

This is a pure-Python, open source and free implementation of v1/v2c/v3
SNMP engine distributed under 2-clause [BSD license](https://www.pysnmp.com/pysnmp/license.html).

The PySNMP project was initially sponsored by a [PSF](http://www.python.org/psf/) grant.
Thank you!

This repo is derived from Ilya Etingof's project [etingof/pysnmp](https://github.com/etingof/pysnmp), but [LeXtudio Inc. has taken over the entire PySNMP ecosystem](https://github.com/etingof/pysnmp/issues/429), including the library, documentation, and the website.

Ilya sadly passed away on 10-Aug-2022. Announcement [here](https://lists.openstack.org/pipermail/openstack-discuss/2022-August/030062.html).  His work is still of great use to the Python community and he will be missed.

Features
--------

* Complete SNMPv1/v2c and SNMPv3 support
* SMI framework for resolving MIB information and implementing SMI
  Managed Objects
* Complete SNMP entity implementation
* USM Extended Security Options support (3DES, 192/256-bit AES encryption)
* Extensible network transports framework (UDP/IPv4, UDP/IPv6)
* Asynchronous socket-based IO API support
* [Asyncio](https://docs.python.org/3/library/asyncio.html) integration
* [PySMI](https://www.pysnmp.com/pysmi/) integration for dynamic MIB compilation
* Built-in instrumentation exposing protocol engine operations
* Python eggs and py2exe friendly
* 100% Python, works with Python 3.8+
* MT-safe (if SnmpEngine is thread-local)

Features, specific to SNMPv3 model include:

* USM authentication (MD5/SHA-1/SHA-2) and privacy (DES/AES) protocols (RFC3414, RFC7860)
* View-based access control to use with any SNMP model (RFC3415)
* Built-in SNMP proxy PDU converter for building multi-lingual
  SNMP entities (RFC2576)
* Remote SNMP engine configuration
* Optional SNMP engine discovery
* Shipped with standard SNMP applications (RFC3413)

Download & Install
------------------

The PySNMP software is freely available for download from [PyPI](https://pypi.python.org/pypi/pysnmp)
and [GitHub](https://github.com/lextudio/pysnmp.git).

Just run:

```bash
$ pip install pysnmp
```

To download and install PySNMP along with its dependencies:

* [PyASN1](https://pyasn1.readthedocs.io)
* [PySMI](https://www.pysnmp.com/pysmi/) (required for MIB services only)
* If cryptography package presents strong SNMPv3 encryption is enabled

Make sure you check out other sibling projects of PySNMP on
[the home page](https://www.pysnmp.com/).

Examples
--------

PySNMP is designed in a layered fashion. Top-level and easiest to use API is known as
*hlapi*. Here's a quick example on how to SNMP GET:

```python
from pysnmp.hlapi.v1arch.asyncio import *

import asyncio


async def run():
    with Slim(1) as slim:
        errorIndication, errorStatus, errorIndex, varBinds = await slim.get(
            'public',
            'demo.pysnmp.com',
            161,
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
        else:
            for varBind in varBinds:
                print(" = ".join([x.prettyPrint() for x in varBind]))

asyncio.run(run())
```

This is how to send SNMP TRAP:

```python
from pysnmp.hlapi.v3arch.asyncio import *

import asyncio


async def run():
    snmpEngine = SnmpEngine()
    errorIndication, errorStatus, errorIndex, varBinds = await sendNotification(
        snmpEngine,
        CommunityData('public', mpModel=0),
        await UdpTransportTarget.create(('demo.pysnmp.com', 162)),
        ContextData(),
        "trap",
        NotificationType(ObjectIdentity("1.3.6.1.6.3.1.1.5.2")).addVarBinds(
            ("1.3.6.1.6.3.1.1.4.3.0", "1.3.6.1.4.1.20408.4.1.1.2"),
            ("1.3.6.1.2.1.1.1.0", OctetString("my system")),
        ),
    )

    if errorIndication:
        print(errorIndication)

    snmpEngine.closeDispatcher()

asyncio.run(run())
```

> We maintain publicly available SNMP Agent and TRAP sink at
> [demo.pysnmp.com](https://www.pysnmp.com/snmp-simulation-service). You are
> welcome to use it while experimenting with whatever SNMP software you deal with.

Other than that, PySNMP is capable to automatically fetch and use required MIBs from HTTP sites
or local directories. You could configure any MIB source available to you (including
[this one](https://mibs.pysnmp.com)) for that purpose.

For more sample scripts please refer to [examples section](https://www.pysnmp.com/pysnmp/examples/index.html#high-level-snmp)
at PySNMP web site.

Documentation
-------------

Library documentation can be found at the [PySNMP docs site](https://www.pysnmp.com/pysnmp/).

If something does not work as expected, please [learn the support options](https://www.pysnmp.com/support).

Pull requests are appreciated! ;-)

Copyright (c) 1999-2020, [Ilya Etingof](https://lists.openstack.org/pipermail/openstack-discuss/2022-August/030062.html).
Copyright (c) 2022-2024, [LeXtudio Inc](mailto:support@lextudio.com).
Copyright (c) 1999-2024, [Other PySNMP contributors](https://github.com/lextudio/pysnmp/THANKS.txt).
All rights reserved.
