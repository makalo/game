
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 22:28:29 2016
@author: zhanghc
"""
#coding=utf-8
#客户端程序TCP 连接

import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(('127.0.0.1',9999))




while(True):
    msg=input("shuru")
    s.send(msg.encode())

import socket
port=8082
host='localhost'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while(True):
    msg=input("shuru")
    s.sendto(msg.encode(),(host,port))

