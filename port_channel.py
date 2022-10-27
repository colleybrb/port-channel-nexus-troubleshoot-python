from netmiko import ConnectHandler
import getpass
import subprocess
import json
import re
import string

def main():
   ip = input("Enter device IP:")
   #module imported to hide password as you type it in the interactive window
   password = getpass.getpass()
   m_n = input("Would you like to find the port channel from mac address=yes or do you know the number already=anything else:")
   # define python dictionary switch for connection credientials to pass to function ConnectHandler
   switch = {
          'device_type': 'cisco_nxos',
          'host': ip,
          'username': '#######',
          'password': password,
          'port' : 22,          # optional, defaults to 22
          'secret': 'secret',     # optional, defaults to ''
}
   net_connect = ConnectHandler(**switch)
   #ELIF decision wheter to find a port channel off mac or off port channel #
   if m_n == "yes":
       z=(1)
   else:
       z=0
       po= input("Enter portchannel as po 4040:")
   # while loop... execute this chunk of code only if you are looking for po off mac address
   while z == 1:
       print("Enter mac address formatted as:")
       print("E.E.E             MAC Address or")
       print("EE-EE-EE-EE-EE-EE  MAC Address or" )
       print("EE:EE:EE:EE:EE:EE  MAC Address or" )
       print("EEEE.EEEE.EEEE     MAC Address")
       mac = input("MAC:") 
       output = net_connect.send_command("show mac address-table address " + mac + " | json")
       #Putting the show command output into a string then to a python dictionary...will see this repeated a few times throughout
       json_dict=json.loads(output)
       po = json_dict['TABLE_mac_address']['ROW_mac_address']['disp_port']
       print("Port-channel is " + po)
       z = (2)
       
   # defining function link_status and passing net_Connect, po and Z to the function
   def link_status(net_connect, po, z):
      #search for eth inside of po if found fix it to a portchannel
      eth = re.findall(r'Eth', po)
      while eth==['Eth']:
         output2 = net_connect.send_command("show run int "+ po +" | egrep word-exp channel-group")
         po=[int(s) for s in output2.split() if s.isdigit()]
         po=po[0]
         po=("po "+str(po))
         print(po)
         print(type(po))
         eth = 0  
      output3 = net_connect.send_command("show port-channel summary int "+ po +" | json")
      print(output3)
      json_output3= json.loads(output3)
      print("Interface "+ po +" information:")
      #Display port-channel information
      if json_output3['TABLE_channel']['ROW_channel']['layer']== "S":
        x=("LAYER 2")
      else:
        x=("LAYER 3")
      print("Interface is: "+x)
      if json_output3['TABLE_channel']['ROW_channel']["status"]== "D":
        x=("DOWN")
      else:
        x=("UP")
      print("Ether Channel Status: "+x)
      print("Port Channel members with status")
      #enables being able to call parts of ROW_member dictionary even if value is returned as string
      if z ==0:
          for key in json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']:
            if (key['port-status'])=="P":
               print(key['port'])
               print("Port is up in port-channel")
            elif key['port-status']=="D":
               print(key['port'])
               print("Port is down")
               int_num = key['port']
               output4 = net_connect.send_command("show run int "+int_num +" all | egrep shutdown | exclude lan")
               print("Admin status: "+ output4)
               output5 = net_connect.send_command("show int "+int_num +" transciever details")
            elif key['port-status']=="I":
               print(key['port'])
               print("Port is individual up")
               fex=re.sub(r'\d\d\d', "", key['port'])
               test_output= net_connect.send_command("attach fex "+ fex )
               test_output2=net_connect.send_command("show lacp internal event-history interface "+ key['port'])
               print(test_output2)
            elif key['port-status']=="H":
               print(key['port'])
               print("Port is hot standby")
            else:
               print(key['port-status'])
               print("Port is suspended")
      else:
         for key in json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']:
            if json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port-status']=="P":
               print(json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port'])
               print("Port is up in port-channel")
            elif json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port-status']=="D":
               print (json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port'])
               print("Port is down")
               int_num = json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port']
               output4 = net_connect.send_command("show run int "+int_num +" all | egrep shutdown | exclude lan")
               print("Admin status: "+ output4)
               output5 = net_connect.send_command("show int "+int_num +" transciever details")
            elif json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port-status']=="I":
               print(json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port'])
               print("Port is individual up")
               fex=re.sub(r'\d\d\d', "", json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port'])
               test_output= net_connect.send_command("attach fex "+ fex )
               test_output2=net_connect.send_command("show lacp internal event-history interface "+ json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port'])
               print(test_output2)
            elif json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port-status']=="H":
               print (json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port'])
               print("Port is hot standby")
            else:
               print(json_output3['TABLE_channel']['ROW_channel']['TABLE_member']['ROW_member']['port-status'])
               print("Port is suspended")      

   link_status(net_connect, po, z)
   
      
  
main()

