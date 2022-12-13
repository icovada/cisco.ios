# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios stp_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.stp_interfaces.stp_interfaces import (
    STP_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.stp_interfaces import (
    STP_interfacesTemplate,
)


class STP_interfacesFacts(object):
    """The ios stp_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = STP_interfacesArgs.argument_spec

    def get_stp_interfaces_data(self, connection):
        return connection.get("show running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for STP_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_stp_interfaces_data(connection)

        # parse native config using the L2_interfaces template
        stp_interfaces_parser = STP_interfacesTemplate(lines=data.splitlines(), module=self._module)
        objs = list(stp_interfaces_parser.parse().values())

        if objs:
            ansible_facts["ansible_network_resources"].pop("stp_interfaces", None)

        params = utils.remove_empties(
            stp_interfaces_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["stp_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
