import socket
import subprocess
import os
import signal
import time
import sys
#import subprocess import Popen, PIPE, STDOUT

host = '192.168.0.13'
port = 3030

# DROP 12.1.0.0/16 (iptables rule)
#subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -A FORWARD -s 12.1.0.0/16 -j DROP'", shell=True, check=True)


# TSHARK
def ip_tshark():
    try:
        # os - 콘솔에 출력하지 않고 수행만 & 결과값을 result 변수에 저장 & 1개 출력하면 수행 끝(output point)
        result = os.popen("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:1'").read()

        # subprocess 로 함 해보기 ~
        #result = subprocess.run("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:1'", stdout=subprocess.PIPE, text=true)
        #result = subprocess.check_output("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -a 'duration:1'")
        
        #checking (나중에 지울것)
        print(result.split(",")[-1])

        ip_addr = []
        ip_addr = list(set(result.split(",")[-1]))

        print(f"ip_addr = {ip_addr}")
        

        return print("tshark success")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []


# SIGINT HANDLER FUNCTION
def handler(signum, frame):
    print("PRESS CTRL + C")

    # ACCEPT 12.1.0.0/16 (iptables rule)
    #subprocess.run("docker exec -i -t oai-spgwu /bin/bash -c 'iptables -D FORWARD -s 12.1.0.0/16 -j DROP'", shell=True, check=True)

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
