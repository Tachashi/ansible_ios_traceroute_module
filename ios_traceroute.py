#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = r'''
---
module: ios_traceroute
short_description: Identify the path used to reach the target from Cisco IOS network devices
description:
- By using traceroute command, identify the path used to reach the target
- from Cisco IOS network devices.
author:
- Tachashi (@tech_kitara)
version_added: '2.10'
extends_documentation_fragment: ios
options:
  probe:
    description:
    - Number of packets to send per hop.
    type: int
  dest:
    description:
    - The IP Address or hostname (resolvable by network device) of the remote node.
    type: str
    required: true
  source:
    description:
    - The source IP Address.
    type: str
  udp:
    description:
    - The port number of UDP packets to send.
    type: int
  ttl_min:
    description:
    - The minimum time to live. (ttl_min and ttl_max options must be specified at the same time.)
    type: int
  ttl_max:
    description:
    - The maximum time to live. (ttl_min and ttl_max options must be specified at the same time.)
    type: int
  vrf:
    description:
    - The VRF to use for forwarding.
    type: str
'''

EXAMPLES = r'''
- name: Identify the path to 10.10.10.10 using default vrf
  ios_traceroute:
    dest: 10.10.10.10
- name: Identify the path to 10.20.20.20 using prod vrf
  ios_traceroute:
    dest: 10.20.20.20
    vrf: prod
- name: Identify the path to 10.40.40.40 from 10.30.30.30 with setting probe and ttl
  ios_traceroute:
    dest: 10.40.40.40
    source: 10.30.30.30
    probe: 5
    ttl_min: 1
    ttl_max: 15
'''

RETURN = '''
commands:
  description: Show the command sent.
  returned: always
  type: list
  sample: ["traceroute 10.40.40.40 source 10.30.30.30 probe 5 ttl 1 15"]
output:
  description: Raw output of traceroute command.
  returned: always
  type: list
hop:
  description: IP addresses of each hops.
  returned: always
  type: dict
  sample: {"1": ["10.30.30.30"], "2": ["10.10.10.10", "10.20.20.20"], "3": ["10.40.40.40"]}
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.ios.ios import run_commands
from ansible.module_utils.network.ios.ios import ios_argument_spec
import re


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        probe=dict(type="int"),
        dest=dict(type="str", required=True),
        source=dict(type="str"),
        udp=dict(type="int"),
        ttl_min=dict(type="int"),
        ttl_max=dict(type="int"),
        vrf=dict(type="str")
    )

    argument_spec.update(ios_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec)

    probe = module.params["probe"]
    dest = module.params["dest"]
    source = module.params["source"]
    udp = module.params["udp"]
    ttl_min = module.params["ttl_min"]
    ttl_max = module.params["ttl_max"]
    vrf = module.params["vrf"]

    warnings = list()

    results = {}
    if warnings:
        results["warnings"] = warnings

    results["commands"] = [build_trace(module, dest, source, probe, udp, ttl_min, ttl_max, vrf)]

    trace_results = run_commands(module, commands=results["commands"])
    trace_results_list = trace_results[0].split("\n")

    parse_result = []
    for trace_line in trace_results_list:
        hop_result = parse_trace(trace_line)
        if isinstance(hop_result, list):
            parse_result.append(hop_result)
        elif isinstance(hop_result, str) and parse_result != []:
            parse_result[-1].append(hop_result)

    parse_result_dict = {}

    for ip_item in parse_result:
        key = ip_item[0]
        value = list(set(ip_item[1:]))
        parse_result_dict[key] = value

    results["output"] = trace_results_list
    results["hop"] = parse_result_dict
    module.exit_json(**results)


def build_trace(module, dest, source=None, probe=None, udp=None, ttl_min=None, ttl_max=None, vrf=None):
    """
    Function to build the command to send to the terminal for the network device
    to execute. All args come from the module's unique params.
    """
    if vrf is not None:
        cmd = "traceroute vrf {0} {1}".format(vrf, dest)
    else:
        cmd = "traceroute {0}".format(dest)

    for command in ["source", "probe"]:
        arg = module.params[command]
        if arg:
            cmd += " {0} {1}".format(command, arg)

    if udp is not None:
        cmd += " {0} {1}".format("port", udp)

    if ttl_min is not None and ttl_max is not None:
        cmd += " {0} {1} {2}".format("ttl", ttl_min, ttl_max)

    return cmd


def parse_trace(trace_line):
    """
    Function used to parse the hop address information from the traceroute response.
    """
    trace_line_list = trace_line.split(" ")
    num_re = re.compile(r"(^[1-9]$|^[1-9][0-9]$)")
    ip_re = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")

    for trace_num_item in trace_line_list[:3]:
        match_num = num_re.search(trace_num_item)
        if match_num:
            break

    if match_num:
        ip_list = [match_num.group()]
        for trace_item in trace_line_list:
            match_ip = ip_re.search(trace_item)
            if match_ip:
                ip_list.append(match_ip.group(0))
        return ip_list
    else:
        for trace_item in trace_line_list:
            match_ip = ip_re.search(trace_item)
            if match_ip:
                return match_ip.group(0)


if __name__ == "__main__":
    main()
