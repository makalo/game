import socket
s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s2.connect(('127.0.0.1',9998))
print(s2.recv(1024))
for data in ['wang','song','chen']:
    s2.send(data.encode())
    print(s2.recv(1024))

#s2.send(b'exit')