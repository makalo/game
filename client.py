import socket
port=8082
host='localhost'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while(True):
    msg=input("shuru")
    s.sendto(msg.encode(),(host,port))