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
        
    - name: check if the traceroute results always include specific transit ip address in hop 7
      assert: 
        that:
            - result_traceroute.hop['7'] == ['172.30.100.1']
```

# Sample Result

**All IP addresses are anonymized using [Netconan](https://github.com/intentionet/netconan), so some IP addresses don't coincide with the playbook.**  

```yaml
PLAY [cisco] ************************************************************************************************************

TASK [execute traceroute] ***********************************************************************************************
ok: [test3]

TASK [debug traceroute] *************************************************************************************************
ok: [test3] => {
    "msg": {
        "changed": false,
        "commands": [
            "traceroute 172.174.88.165 source 192.168.173.198 probe 4 ttl 1 20"
        ],
        "failed": false,
        "hop": {
            "1": [
                "192.168.173.43"
            ],
            "10": [
                "108.224.66.109",
                "108.224.66.161",
                "108.224.66.172"
            ],
            "11": [
                "108.254.165.36",
                "172.159.216.191"
            ],
            "12": [
                "215.123.152.64",
                "74.246.135.251",
                "222.152.243.188"
            ],
            "13": [
                "108.224.67.238",
                "108.224.67.103"
            ],
            "14": [
                "108.224.80.18",
                "108.224.80.23"
            ],
            "15": [
                "172.174.88.165"
            ],
            "2": [],
            "3": [
                "172.30.231.192"
            ],
            "4": [
                "126.244.74.242"
            ],
            "5": [
                "18.232.93.6",
                "18.232.93.1"
            ],
            "6": [
                "18.235.248.200",
                "18.235.248.207"
            ],
            "7": [
                "68.32.20.116"
            ],
            "8": [],
            "9": [
                "74.246.135.176",
                "108.224.82.72",
                "108.224.82.242"
            ]
        },
        "output": [
            "Type escape sequence to abort.",
            "Tracing the route to 172.174.88.165",
            "VRF info: (vrf in name/id, vrf out name/id)",
            "  1 192.168.173.43 186 msec 16 msec 13 msec 11 msec",
            "  2  *  *  *  * ",
            "  3 172.30.231.192 51 msec 55 msec 44 msec 62 msec",
            "  4 126.244.74.242 54 msec 79 msec 39 msec 59 msec",
            "  5 18.232.93.6 43 msec",
            "    18.232.93.1 63 msec",
            "    18.232.93.6 60 msec",
            "    18.232.93.1 64 msec",
            "  6 18.235.248.200 56 msec 80 msec 53 msec",
            "    18.235.248.207 62 msec",
            "  7 68.32.20.116 61 msec 55 msec 59 msec 39 msec",
            "  8  *  *  *  * ",
            "  9 108.224.82.72 57 msec",
            "    74.246.135.176 39 msec",
            "    108.224.82.242 60 msec 61 msec",
            " 10 108.224.66.161 62 msec",
            "    108.224.66.109 70 msec",
            "    108.224.66.172 72 msec",
            "    108.224.66.161 54 msec",
            " 11 108.254.165.36 [MPLS: Label 27008 Exp 4] 70 msec",
            "    172.159.216.191 [MPLS: Label 178553 Exp 4] 57 msec",
            "    108.254.165.36 [MPLS: Label 25624 Exp 4] 71 msec 56 msec",
            " 12 74.246.135.251 79 msec",
            "    222.152.243.188 77 msec",
            "    74.246.135.251 60 msec",
            "    215.123.152.64 53 msec",
            " 13 108.224.67.238 58 msec 62 msec",
            "    108.224.67.103 70 msec 68 msec",
            " 14 108.224.80.23 58 msec",
            "    108.224.80.18 59 msec",
            "    108.224.80.23 70 msec 70 msec",
            " 15 172.174.88.165 77 msec 60 msec 61 msec 63 msec"
        ]
    }
}

TASK [check if the traceroute results (dict) always include specific transit ip address in hop 7] ***********************
ok: [test3] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY RECAP **************************************************************************************************************
test3                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```
