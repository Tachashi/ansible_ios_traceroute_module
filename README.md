# ansible_ios_traceroute_module
Ansible ios_traceroute module for Cisco IOS

# Sample Playbook
```yaml
---

- hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:
    - name: execute traceroute
      ios_traceroute:
        dest: 172.16.1.100
        probe: 4
        source: 192.168.100.201
        ttl_min: 1
        ttl_max: 20
      register: result_traceroute

    - name: debug traceroute
      debug: 
        msg: "{{ result_traceroute }}"
        
    - name: check if the traceroute results (dict) always include specific transit ip address in hop 7
      assert: 
        that:
            - result_traceroute.hop_dict['7'] == ['72.14.202.237']

    - name: check if the traceroute results (list) always include specific transit ip address in hop 7
      assert: 
        that:
            - result_traceroute.hop_list[6][0] == '7'
            - result_traceroute.hop_list[6][1] == '72.14.202.237'
            - result_traceroute.hop_list[6][2] is not defined
```

# Sample Result

**All IP addresses are anonymized using [Netconan](https://github.com/intentionet/netconan), so some IP addresses don't coincide with the playbook.**  

```yaml
PLAY [cisco] **************************************************************************************************

TASK [execute traceroute] *************************************************************************************
ok: [test3]

TASK [debug traceroute] ***************************************************************************************
ok: [test3] => {
    "msg": {
        "changed": false,
        "commands": [
            "traceroute 172.168.147.212 source 192.168.156.52 probe 4 ttl 1 20"
        ],
        "failed": false,
        "hop_dict": {
            "1": [
                "192.168.156.166"
            ],
            "10": [
                "100.42.161.123",
                "100.42.161.117",
                "100.42.161.123",
                "100.42.161.117"
            ],
            "11": [
                "172.153.109.149",
                "100.53.172.191",
                "172.153.109.149"
            ],
            "12": [
                "211.139.161.51",
                "94.253.194.148",
                "211.139.161.51",
                "223.86.54.195"
            ],
            "13": [
                "100.42.160.5",
                "100.42.160.206"
            ],
            "14": [
                "100.42.185.84",
                "100.42.185.83",
                "100.42.185.84"
            ],
            "15": [
                "172.168.147.212"
            ],
            "2": [],
            "3": [
                "172.17.167.44"
            ],
            "4": [
                "122.140.76.127"
            ],
            "5": [
                "18.75.148.128",
                "18.75.148.132",
                "18.75.148.128",
                "18.75.148.132"
            ],
            "6": [
                "18.73.96.252",
                "18.75.146.132",
                "18.73.96.252"
            ],
            "7": [
                "85.90.36.165"
            ],
            "8": [],
            "9": [
                "100.42.189.55",
                "100.42.187.68",
                "100.42.189.55",
                "100.42.187.78"
            ]
        },
        "hop_list": [
            [
                "1",
                "192.168.156.166"
            ],
            [
                "2"
            ],
            [
                "3",
                "172.17.167.44"
            ],
            [
                "4",
                "122.140.76.127"
            ],
            [
                "5",
                "18.75.148.128",
                "18.75.148.132",
                "18.75.148.128",
                "18.75.148.132"
            ],
            [
                "6",
                "18.73.96.252",
                "18.75.146.132",
                "18.73.96.252"
            ],
            [
                "7",
                "85.90.36.165"
            ],
            [
                "8"
            ],
            [
                "9",
                "100.42.189.55",
                "100.42.187.68",
                "100.42.189.55",
                "100.42.187.78"
            ],
            [
                "10",
                "100.42.161.123",
                "100.42.161.117",
                "100.42.161.123",
                "100.42.161.117"
            ],
            [
                "11",
                "172.153.109.149",
                "100.53.172.191",
                "172.153.109.149"
            ],
            [
                "12",
                "211.139.161.51",
                "94.253.194.148",
                "211.139.161.51",
                "223.86.54.195"
            ],
            [
                "13",
                "100.42.160.5",
                "100.42.160.206"
            ],
            [
                "14",
                "100.42.185.84",
                "100.42.185.83",
                "100.42.185.84"
            ],
            [
                "15",
                "172.168.147.212"
            ]
        ],
        "output": [
            "Type escape sequence to abort.",
            "Tracing the route to 172.168.147.212",
            "VRF info: (vrf in name/id, vrf out name/id)",
            "  1 192.168.156.166 197 msec 16 msec 14 msec 11 msec",
            "  2  *  *  *  * ",
            "  3 172.17.167.44 118 msec 109 msec 86 msec 66 msec",
            "  4 122.140.76.127 48 msec 79 msec 65 msec 61 msec",
            "  5 18.75.148.128 75 msec",
            "    18.75.148.132 94 msec",
            "    18.75.148.128 57 msec",
            "    18.75.148.132 40 msec",
            "  6 18.73.96.252 62 msec",
            "    18.75.146.132 95 msec",
            "    18.73.96.252 85 msec 65 msec",
            "  7 85.90.36.165 60 msec 62 msec 46 msec 59 msec",
            "  8  *  *  *  * ",
            "  9 100.42.189.55 58 msec",
            "    100.42.187.68 41 msec",
            "    100.42.189.55 58 msec",
            "    100.42.187.78 59 msec",
            " 10 100.42.161.123 75 msec",
            "    100.42.161.117 52 msec",
            "    100.42.161.123 49 msec",
            "    100.42.161.117 63 msec",
            " 11 172.153.109.149 [MPLS: Label 98614 Exp 4] 43 msec",
            "    100.53.172.191 [MPLS: Label 24722 Exp 4] 90 msec",
            "    172.153.109.149 [MPLS: Label 98614 Exp 4] 110 msec 61 msec",
            " 12 211.139.161.51 58 msec",
            "    94.253.194.148 70 msec",
            "    211.139.161.51 46 msec",
            "    223.86.54.195 60 msec",
            " 13 100.42.160.5 63 msec",
            "    100.42.160.206 58 msec 57 msec 62 msec",
            " 14 100.42.185.84 62 msec 66 msec",
            "    100.42.185.83 86 msec",
            "    100.42.185.84 43 msec",
            " 15 172.168.147.212 74 msec 55 msec 68 msec 60 msec"
        ]
    }
}

TASK [check if the traceroute results (dict) always include specific transit ip address in hop 7] *******************************
ok: [test3] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [check if the traceroute results (list) always include specific transit ip address in hop 7] *******************************
ok: [test3] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY RECAP **********************************************************************************************************************
test3                      : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
