# 생각 정리
import socket
import subprocess

host = '192.168.0.13'
port = 3030

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
            #3. tshark -> run? Piopen?
            #4. tshark를 어떻게 자식 프로세스로 해야할까
        except subprocess.CalledProcessError as e:
            print(f"스크립트 입력 중 에러 발생")
