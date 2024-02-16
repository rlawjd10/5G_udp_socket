import socket
import subprocess
import signal
import time
import sys

host = '192.168.0.13'
port = 3030

# DROP 12.1.0.0/16
subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -A FORWARD -s 12.1.0.0/16 -j DROP'", shell=True, check=True)
# ACCEPT 192.168.0.12(TINM)
subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -I FORWARD 1 -s 12.1.0.0/16 -d 192.168.0.12 -j ACCEPT'", shell=True, check=True)

ip_list = []    # ip list
accept_list = []    # iptables 관리용 ip list

# FILE READ & UPDATE IP_LIST
def read_file(file_list):
    global ip_list
    
    # output.json 있는 ip를 중복없이 file_list에 저장
    f = open("output.json", "r")
    for line in f:
        ip = line.split(",")[-1].strip()
        file_list.append(ip)
    file_list = list(set(file_list))
    f.close()


# INSERT & DELETE IPTABLES RULE
def check_and_update_ip_lists():
    global ip_list
    global accept_list

    # 파일에 있는 ip를 ip_list에 저장
    read_file(ip_list)

    # accept_list로 iptables에 accept 된 ip
    for new_ip in ip_list:
        if new_ip not in accept_list:
            subprocess.run(f"docker exec -i -t oai-spgwu /bin/bash -c 'iptables -I FORWARD 1 -j ACCEPT -s {new_ip}'", shell=True, check=True)
            accept_list.append(new_ip)

    # 현재 파일에 있는 ip list를 확인하기 위한 ip list
    recent_list = []
    read_file(recent_list)

    # accept_list에 있는 ip가 ip_list에 없을 때, delete rule
    for ip in accept_list:
        if ip not in recent_list:
            print(f"drop ip :  {ip}")
            subprocess.run(f"docker exec -i -t oai-spgwu /bin/bash -c 'iptables -D FORWARD -j ACCEPT -s {ip}'", shell=True, check=True)
            accept_list.remove(ip)
            ip_list.remove(ip)


# SIGINT HANDLER FUNCTION
def handler(signum, frame):
    print("\nPRESS CTRL + C")
    
    # iptables reset
    subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -F'", shell=True, check=True)

    #강제 종료
    sys.exit(0)


# SIGINT
signal.signal(signal.SIGINT, handler)

# UDP_SOCKET_PROGRAMMING
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

print(f"UDP 서버가 {host}:{port}에서 실행 중입니다.")

while True:
    data, client_address = server_socket.recvfrom(1024)

    data = data.decode('utf-8')
    print(f"클라이언트로부터 수신: {data}")

    # 무한 루프 & 3초마다 반복 실행 (tshark)
    while(True):
        subprocess.run("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:3' -e json > output.json", shell=True, capture_output=True, text=True)
        check_and_update_ip_lists()
        time.sleep(3)   
        
