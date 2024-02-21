#packages
import socket
from vidstream import *
import threading
import tkinter

#store IPv4 address in variable and establish connection using sockets & ports
ip_address = socket.gethostbyname(socket.gethostname())
server = StreamingServer(ip_address,9999)
reciever = StreamingServer(ip_address,8888)



