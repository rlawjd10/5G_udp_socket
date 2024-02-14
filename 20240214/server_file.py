import socket
import subprocess
import os
import signal
import time
import sys

host = '192.168.0.13'
port = 3030

# DROP 12.1.0.0/16
subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -A FORWARD -s 12.1.0.0/16 -j DROP'", shell=True, check=True)
# ACCEPT 192.168.0.12(TINM)
subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -I FORWARD 1 -s 12.1.0.0/16 -d 192.168.0.12 -j ACCEPT'", shell=True, check=True)








# 파일 읽기
def ip_tshark():
    count = 10
    for i in range(count):
        result = os.popen("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:1'").read()

        with open('output.json', 'a') as f:
            f.write(result.split(",")[-1])
            f.write('\n')
        
        if i == count -1 :
            break
        
        
'''


# 파일 읽기
def ip_tshark():
	result = os.popen("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:10' -e json > output.json").read()
    	#count = 10
    	for i in range(10):
        	with open('output.json', 'r') as f:
            #f.read(result.split(",")[-1])
            		print(f.split(",")[-1].split('\n'))
            #f.write('\n')
        
       # if i < count - 1 :
           # break
        
'''






# SIGINT HANDLER FUNCTION
def handler(signum, frame):
    print("PRESS CTRL + C")
    
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

    if data.strip() == 'success':
        try:
            ip_tshark()
        except subprocess.CalledProcessError as e:
            print(f"스크립트 입력 중 에러 발생")
