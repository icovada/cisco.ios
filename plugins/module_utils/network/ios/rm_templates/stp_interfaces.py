# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The STP_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class STP_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(STP_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^interface
                    (\s(?P<name>\S+))
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "bpduguard",
            "getval": re.compile(
                r"""
                \s+spanning-tree\sbpduguard\s(?P<bpduguard_status>\w+)
                $""", re.VERBOSE,
            ),
            "setval": "{{ 'spanning-tree bpduguard enable' if bpduguard == True}}",
            "remval": "no spanning-tree bpduguard",
            "result": {
                "{{ name }}": {"bpduguard": "{{ 'True' if bpduguard_status == 'enable' else 'False' }}"},
            },
        },
    ]
    # fmt: on
