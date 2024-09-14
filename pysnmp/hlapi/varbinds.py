#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
from typing import Any, Dict, Tuple

from pysnmp.proto.api import v2c
from pysnmp.smi import builder, view
from pysnmp.smi.rfc1902 import NotificationType, ObjectIdentity, ObjectType

__all__ = ["CommandGeneratorVarBinds", "NotificationOriginatorVarBinds"]


def isEndOfMib(var_binds):  # noqa: N816
    """
    Check if the given variable bindings indicate the end of the MIB.

    Parameters:
    var_binds (list): A list of variable bindings.

    Returns:
    bool: True if it is the end of the MIB, False otherwise.
    """
    return not v2c.apiPDU.getNextVarBinds(var_binds)[1]


class MibViewControllerManager:
    @staticmethod
    def getMibViewController(userCache):
        try:
            mibViewController = userCache["mibViewController"]

        except KeyError:
            mibViewController = view.MibViewController(builder.MibBuilder())
            userCache["mibViewController"] = mibViewController

        return mibViewController


class CommandGeneratorVarBinds(MibViewControllerManager):
    def makeVarBinds(
        self, userCache: Dict[str, Any], varBinds: Tuple[ObjectType, ...]
    ) -> Tuple[ObjectType, ...]:
        mibViewController = self.getMibViewController(userCache)

        resolvedVarBinds = []

        for varBind in varBinds:
            if isinstance(varBind, ObjectType):
                pass

            elif isinstance(varBind[0], ObjectIdentity):
                varBind = ObjectType(*varBind)

            elif isinstance(varBind[0][0], tuple):  # legacy
                varBind = ObjectType(
                    ObjectIdentity(varBind[0][0][0], varBind[0][0][1], *varBind[0][1:]),
                    varBind[1],
                )

            else:
                varBind = ObjectType(ObjectIdentity(varBind[0]), varBind[1])

            resolvedVarBinds.append(
                varBind.resolveWithMib(mibViewController, ignoreErrors=False)
            )

        return tuple(resolvedVarBinds)

    def unmakeVarBinds(
        self,
        userCache: Dict[str, Any],
        varBinds: Tuple[ObjectType, ...],
        lookupMib=True,
    ) -> Tuple[ObjectType, ...]:
        if lookupMib:
            mibViewController = self.getMibViewController(userCache)
            varBinds = tuple(
                ObjectType(ObjectIdentity(x[0]), x[1]).resolveWithMib(mibViewController)
                for x in varBinds
            )

        return varBinds


class NotificationOriginatorVarBinds(MibViewControllerManager):
    def makeVarBinds(self, userCache: Dict[str, Any], varBinds):
        mibViewController = self.getMibViewController(userCache)

        if isinstance(varBinds, NotificationType):
            return varBinds.resolveWithMib(mibViewController, ignoreErrors=False)

        resolvedVarBinds = []

        for varBind in varBinds:
            if isinstance(varBind, NotificationType):
                resolvedVarBinds.extend(
                    varBind.resolveWithMib(mibViewController, ignoreErrors=False)
                )
                continue

            if isinstance(varBind, ObjectType):
                pass

            elif isinstance(varBind[0], ObjectIdentity):
                varBind = ObjectType(*varBind)

            else:
                varBind = ObjectType(ObjectIdentity(varBind[0]), varBind[1])

            resolvedVarBinds.append(
                varBind.resolveWithMib(mibViewController, ignoreErrors=False)
            )

        return resolvedVarBinds

    def unmakeVarBinds(self, userCache: Dict[str, Any], varBinds, lookupMib=False):
        if lookupMib:
            mibViewController = self.getMibViewController(userCache)
            varBinds = [
                ObjectType(ObjectIdentity(x[0]), x[1]).resolveWithMib(mibViewController)
                for x in varBinds
            ]
        return varBinds
