import subprocess
import os
import re
import server, client

#check operating system to issue the correct commands
os_type = os.name
if os_type == 'posix':
    #get hostname of own device
    hostname = subprocess.run('hostname', shell=True, capture_output=True, text=True)
    hostname_ip = subprocess.run('hostname -I', shell=True, capture_output=True, text=True)
    hostname_ip_addr = hostname_ip.stdout.split(' ')[0]
    hostname_ip_prefix = hostname_ip_addr.split('.')[0]
    nmap_cmd = f'sudo nmap -sn {hostname_ip_addr}/24'
else:
    hostname = subprocess.run('hostname', shell=True, capture_output=True, text=True)
    hostname_ip = subprocess.run('ipconfig', shell=True, capture_output=True, text=True)
    hostname_ip_addr = [hn for hn in hostname_ip.stdout.split('\n') if 'IPv4 Address' in hn][0]
    hostname_ip_addr = re.findall('[0-9]+.[0-9]+.[0-9]+.[0-9]+', hostname_ip_addr)[0]
    hostname_ip_prefix = hostname_ip_addr.split('.')[0]
    nmap_cmd = f'nmap -sn {hostname_ip_addr}/24'


while True:
    mode = input('choose to enter server or client mode, or exit program (type "exit")\n>')

    if mode == 'client':
        #run command to get all IPs of network devices
        print('looking for IPs in local network...')
        nmap = subprocess.run(nmap_cmd, shell=True, capture_output=True, text=True)
        local_ip_scans = [x for x in nmap.stdout.split('\n') if 'Nmap scan report' in x]

        local_ips = []
        for ip_scan in local_ip_scans:
            try:
                ip = re.findall('[0-9]+.[0-9]+.[0-9]+.[0-9]+', ip_scan)[0]
                if ip != hostname_ip_addr:
                    local_ips.append(ip)
            except:
                print('failed on ip scan: ', ip_scan)

        #display list of open IPs
        print('local IPs: ')
        for ip in local_ips:
            print(ip)
        
        server_ip = input('select an IP to connect to as client\n>')
        try:
            client.run_client(server_ip=server_ip)
        except Exception as e:
            print('failed with error:', e)   
    elif mode == 'server':
        print('running server, accessible to clients under IP addr:', hostname_ip_addr)
        try:
            server.run_server()
        except Exception as e:
            print('failed with error:', e)
    elif mode == 'exit': break
    else:
        print('mode not valid. please enter again')