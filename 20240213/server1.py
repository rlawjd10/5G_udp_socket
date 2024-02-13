import socket
import subprocess
import os
import signal
import time
import sys

host = '192.168.0.13'
port = 3030

# DROP 12.1.0.0/16 (iptables rule)
subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -A FORWARD -s 12.1.0.0/16 -j DROP'", shell=True, check=True)
subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -I FORWARD 1 -s 12.1.0.0/16 -d 192.168.0.12 -j ACCEPT'", shell=True, check=True)


# TSHARK
def ip_tshark():
    try:
        # 콘솔에 출력하지 않고 수행만 & 결과값을 result 변수에 저장 & 1개 출력하면 수행 끝(autostop condition)
        result = os.popen("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:1'").read()
        
        # checking
        print(result.split(",")[-1])

        ip_addr = result.split(",")[-1]
        subprocess.run(f"docker exec -i -t oai-spgwu /bin/bash -c 'iptables -A FORWARD -s {ip_addr} -j ACCEPT'", shell=True, check=True)

        print("success")
        
        return print("tshark success")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []


# SIGINT HANDLER FUNCTION
def handler(signum, frame):
    print("PRESS CTRL + C")

    # ACCEPT 12.1.0.0/16 (iptables rule)
    #subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -D FORWARD -s 12.1.0.0/16 -j DROP'", shell=True, check=True)
    
    # iptables reset
    subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -F'", shell=True, check=True)

    #강제 종료
    sys.exit(0)


# SIGINT
signal.signal(signal.SIGINT, handler)


# UDP_SOCKET PROGRAMMING
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

print(f"UDP 서버가 {host}:{port}에서 실행 중입니다.")

while True:
    data, client_address = server_socket.recvfrom(1024)

    print(f"클라이언트로부터 수신: {data}")
    data = data.decode('utf-8')

    if data.strip() == 'success':
        try:
            ip_tshark()
        except subprocess.CalledProcessError as e:
            print(f"스크립트 입력 중 에러 발생")



'''
UDP 서버가 192.168.0.13:3030에서 실행 중입니다.
클라이언트로부터 수신: b'success'
Running as user "root" and group "root". This could be dangerous.
Capturing on 'demo-oai'
6 
12.1.1.2

/bin/bash: line 1: -j: command not found
Error: Command 'docker exec -i -t oai-spgwu /bin/bash -c 'iptables -A FORWARD -s 12.1.1.2
 -j ACCEPT'' returned non-zero exit status 127.
^CPRESS CTRL + C
'''
