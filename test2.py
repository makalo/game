import socket
port=8081
host='192.168.0.1'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while(True):
    msg=input("shuru")
    s.sendto(msg.encode(),(host,port))