#packages
import socket
from vidstream import *
import threading
import tkinter

#store IPv4 address in variable and establish connection using sockets & ports
ip_address = socket.gethostbyname(socket.gethostname())
server = StreamingServer(ip_address,7777)
reciever = StreamingServer(ip_address,6666)
