# Cisco Port-channel troubleshooter

This project is intended as an intro to utilizing netmiko for troubleshooting port-channels on traditional decentralized control planes. 

### What it does
* Inputs credentials
* Checks host for mac, finds port-channel associated and puts the status in readible format.
* Outputa internal interface logs for that port-channel.
* If you had a team of developers you could regex known patterns to issues.

### Typical Output 
```
****Intentionally left this a little messy so you can see the data types and data sources****
Enter device IP:10.xx.x.x
Password:
Would you like to find the port channel from mac address=yes or do you know the number already=anything else:yes
Enter mac address formatted as:
E.E.E             MAC Address or
EE-EE-EE-EE-EE-EE  MAC Address or
EE:EE:EE:EE:EE:EE  MAC Address or
EEEE.EEEE.EEEE     MAC Address
MAC:00f2.8b7d.xxx
Port-channel is Ethernet118/1/x
po 3054
<class 'str'>
{
  "TABLE_channel": {
    "ROW_channel": {
      "group": 30xx,
      "port-channel": "port-channel30xx",
      "layer": "S",
      "status": "D",
      "type": "Eth",
      "prtcl": "LACP",
      "TABLE_member": {
        "ROW_member": {
          "port": "Ethernet118/1/x",
          "port-status": "I"
        }
      }
    }
  }
}

Interface po 3054 information:
Interface is: LAYER 2
Ether Channel Status: DOWN
Port Channel members with status
Ethernet118/1/x
Port is individual up


>>>>FSM: <Ethernet118/1/5> has 361 logged transitions<<<<<

1) FSM:<Ethernet118/1/5> Transition at 669018 usecs after Sat Sep 29 00:40:36 2018
    Previous state: [LACP_ST_INDIVIDUAL_OR_DEFAULT]
    Triggered event: [LACP_EV_RECEIVE_PARTNER_PDU_TIMED_OUT]
    Next state: [FSM_ST_NO_CHANGE]
.....
......
```
### Notes
* This is something I used to start programming with Cisco/ Nexus.
* I hope the example is a catalyst for other network guys getting into python
* I have not updated since 2018ish.

 


***If you have issues and need help reach out.***
