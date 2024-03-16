import subprocess
import os

#check operating system to issue the correct commands
os_type = os.name

#check for all devices on the local network

#get hostname of own device
hostname = subprocess.run('hostname', shell=True, capture_output=True, text=True)
hostname_ip = subprocess.run('hostname -I', shell=True, capture_output=True, text=True)

#run command to get all IPs of network devices
#sudo nmap -sn 10.0.0.127/24
nmap_cmd = f'sudo nmap -sn {hostname_ip}'
nmap = subprocess.run(nmap_cmd, shell=True, capture_output=True, text=True)

#display list of open IPs

#allow user to enter "start server" or "start client <ip>"
