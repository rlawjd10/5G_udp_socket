import subprocess
import json
import time

ip_lists = []

def run_tshark():
    command = "tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:10' -e json"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def update_ip_list(ip_list, new_ip):
    if new_ip not in ip_list:
        ip_list.append(new_ip)
        print(f"Added IP: {new_ip} to the list.")
    else:
        print(f"IP: {new_ip} already exists in the list.")

def check_and_update_ip_lists(tshark_output):
    tshark_ips = json.loads(tshark_output)
    for ip_list in ip_lists:
        for ip in tshark_ips:
            update_ip_list(ip_list, ip)

def main():
    while True:
        tshark_output = run_tshark()
        check_and_update_ip_lists(tshark_output)
        time.sleep(5)

if __name__ == "__main__":
    main()



import subprocess
import json
import time

ip_lists = []

def run_tshark():
    command = "tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:10' -e json"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def update_ip_list(ip_list, new_ip):
    if new_ip not in ip_list:
        ip_list.append(new_ip)
        print(f"Added IP: {new_ip} to the list.")
    else:
        print(f"IP: {new_ip} already exists in the list.")

def check_and_update_ip_lists(tshark_output):
    tshark_ips = json.loads(tshark_output)
    for ip_list in ip_lists:
        for ip in tshark_ips:
            update_ip_list(ip_list, ip)

def main():
    while True:
        tshark_output = run_tshark()
        check_and_update_ip_lists(tshark_output)
        time.sleep(5)

if __name__ == "__main__":
    main()
