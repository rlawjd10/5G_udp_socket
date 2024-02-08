# 원하는 조건의 ip를 print 할 수 있도록
import socket
import subprocess
import os

host = '192.168.0.13'
port = 3030

def ip_tshark():
    try:
        #process = subprocess.Popen("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True).stdout
        #process = subprocess.run("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src", shell=True, check=True)
        
        # 1개 패킷 캡쳐만 하면 됨. 어차피 success되면 해당 ip만 필요하니까. 추후 delete 문제는 나중에
        # os.popen 시도해보고 안되면 subprocess.run().stdout으로 시도해볼 것. 생각해보니까 1개만 담는거면 ㄱㅊ 할 듯
        result = os.popen("tshark -i demo-oai -Y '(ip.src==12.1.0.0/16)&&(ip.dst==192.168.0.12)&&(frame.len eq 98)' -T fields -e ip.src -c 1").read()
        
        print(result.split(",")[1])

        # 자식 프로세스 출력 읽어오고 종료할 때까지 기다림
        # process.wait()
        # 자식 프로세스의 출력을 읽어오고 종료할 때까지 기다림.
        #output, _ = process.communicate()
        # 공백 제거하고 , 기준으로 문자열 분할, 각 줄에 대한 반복
        #ip_src_list = [line.strip().split(",")[1] for line in output.decode('utf-8').strip().split("\n") if line.strip()]
        
        #ip_list = list(set(ip_src_list))
        
        #for ip_src in ip_list:
        	#print(ip_src)
        
        # 중복을 제거하고 필터링한 ip를 main으로 return하기
        return print("tshark success")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

print(f"UDP 서버가 {host}:{port}에서 실행 중입니다.")

while True:
    data, client_address = server_socket.recvfrom(1024)

    print(f"클라이언트로부터 수신: {data}")
    data = data.decode('utf-8')

    if data.strip() == 'success':
        try:
            #1. json 파일로 하지 않는 방향으로 
            #2. tshark에서 출력되는 data를 어떻게 바로 array에 넣을 수 있을까. list(set())으로 하면 중복되지 않음
            #3. tshark -> run? Popen?
            #4. tshark를 어떻게 자식 프로세스로 해야할까
            #5. tshark를 while문으로 어찌저찌...
            #6. tshark로 타임스탬프 찍어서 계속 시간을 갱신하는 방법은 어떨까 - 갱신된 시간보다 작으면 delete
            ip_tshark()
        except subprocess.CalledProcessError as e:
            print(f"스크립트 입력 중 에러 발생")
