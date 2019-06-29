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
            - result_traceroute.hop[6][0] == '7'
            - result_traceroute.hop[6][1] == '72.31.100.1'
            - result_traceroute.hop[6][2] is not defined
```

# Sample Result

**All IP addresses are anonymized, so some IP addresses don't coincide with the playbook.**  

```yaml
PLAY [cisco] **************************************************************************************************

TASK [execute traceroute] *************************************************************************************
ok: [192.168.100.201]

TASK [debug traceroute] ***************************************************************************************
ok: [192.168.100.201] => {
    "msg": {
        "changed": false,
        "commands": [
            "traceroute 172.155.123.165 source 192.168.151.3 probe 4 ttl 1 20"
        ],
        "failed": false,
        "hop": [
            [
                "1",
                "192.168.151.164"
            ],
            [
                "2"
            ],
            [
                "3",
                "172.18.149.12"
            ],
            [
                "4",
                "111.206.198.61"
            ],
            [
                "5",
                "28.13.229.239",
                "28.13.229.233"
            ],
            [
                "6",
                "28.15.133.184",
                "28.13.225.73",
                "28.15.133.184"
            ],
            [
                "7",
                "81.168.187.176"
            ],
            [
                "8"
            ],
            [
                "9",
                "116.129.12.118",
                "116.129.12.223",
                "116.129.8.125",
                "116.129.8.126"
            ],
            [
                "10",
                "116.129.16.56",
                "116.129.16.160",
                "116.129.16.224",
                "116.129.16.55"
            ],
            [
                "11",
                "116.156.60.253",
                "172.160.223.35"
            ],
            [
                "12",
                "218.107.31.164",
                "213.174.81.41",
                "218.107.31.164"
            ],
            [
                "13",
                "116.129.17.125",
                "116.129.17.184"
            ],
            [
                "14",
                "116.129.15.135",
                "116.129.15.131",
                "116.129.15.135",
                "116.129.15.131"
            ],
            [
                "15",
                "172.155.123.165"
            ]
        ],
        "output": [
            "Type escape sequence to abort.",
            "Tracing the route to 172.155.123.165",
            "VRF info: (vrf in name/id, vrf out name/id)",
            "  1 192.168.151.164 6 msec 6 msec 6 msec 5 msec",
            "  2  *  *  *  * ",
            "  3 172.18.149.12 48 msec 60 msec 58 msec 60 msec",
            "  4 111.206.198.61 59 msec 60 msec 60 msec 61 msec",
            "  5 28.13.229.239 63 msec 67 msec",
            "    28.13.229.233 52 msec 68 msec",
            "  6 28.15.133.184 58 msec 56 msec",
            "    28.13.225.73 63 msec",
            "    28.15.133.184 96 msec",
            "  7 81.168.187.176 57 msec 56 msec 62 msec 58 msec",
            "  8  *  *  *  * ",
            "  9 116.129.12.118 47 msec",
            "    116.129.12.223 39 msec",
            "    116.129.8.125 39 msec",
            "    116.129.8.126 41 msec",
            " 10 116.129.16.56 63 msec",
            "    116.129.16.160 49 msec",
            "    116.129.16.224 50 msec",
            "    116.129.16.55 45 msec",
            " 11 116.156.60.253 [MPLS: Label 24870 Exp 4] 68 msec 62 msec 95 msec",
            "    172.160.223.35 [MPLS: Label 214957 Exp 4] 88 msec",
            " 12 218.107.31.164 56 msec",
            "    213.174.81.41 63 msec",
            "    218.107.31.164 63 msec 62 msec",
            " 13 116.129.17.125 44 msec",
            "    116.129.17.184 41 msec 66 msec 59 msec",
            " 14 116.129.15.135 60 msec",
            "    116.129.15.131 59 msec",
            "    116.129.15.135 59 msec",
            "    116.129.15.131 59 msec",
            " 15 172.155.123.165 61 msec 70 msec 60 msec 70 msec"
        ]
    }
}

TASK [check if the traceroute results always include specific transit ip address in hop 7] ********************
ok: [192.168.100.201] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY RECAP ****************************************************************************************************
192.168.151.3            : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
