import tkinter as tk
import socket
import ssl
from vidstream import StreamingServer, CameraClient, ScreenShareClient, AudioSender, AudioReceiver
import threading
import pyaudio

local_ip_address = socket.gethostbyname(socket.gethostname())
server = StreamingServer(local_ip_address, 9999)

def start_listening():
    t1 = threading.Thread(target=start_server_ssl, args=(server,))
    t1.start()

def start_server_ssl(stream_server):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.check_hostname = False
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((stream_server.host, stream_server.port))
        server_socket.listen(5)

        while True:
            conn, addr = server_socket.accept()
            ssl_conn = context.wrap_socket(conn, server_side=True)
            stream_server.connections.append(ssl_conn)

def start_camera_stream():
    camera_client = CameraClient(text_target_ip.get(1.0,'end-1c'), 7777)
    t2 = threading.Thread(target=camera_client.start_stream)
    t2.start()

def start_screen_sharing():
    screen_client = ScreenShareClient(text_target_ip.get(1.0,'end-1c'), 7777)
    t3 = threading.Thread(target=screen_client.start_stream)
    t3.start()

def start_audio_server():
    audio_sender = AudioSender(text_target_ip.get(1.0,'end-1c'), 8888)  # Use 8888 port for AudioSender
    t4 = threading.Thread(target=start_microphone_stream, args=(audio_sender,))
    t4.start()

def start_microphone_stream():
    # Constants
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    port = 12345  # Port to listen on

    # Bind to the port
    server_socket.bind((host, port))

    # Queue up to 5 requests
    server_socket.listen(5)

    print("Server listening on {}:{}".format(host, port))

    # Function to handle connections
    def handle_client(client_socket, addr):
        print("Accepted connection from {}:{}".format(addr[0], addr[1]))
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)
        while True:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()
        print("Connection from {}:{} closed".format(addr[0], addr[1]))

    while True:
        # Establish connection with client.
        client_socket, addr = server_socket.accept()
        # Start a new thread to handle the client
        handle_client(client_socket, addr)


window = tk.Tk()
window.title("SERVER")
window.geometry('500x500')

label_target_ip = tk.Label(window,text="\nTarget IP:")
label_target_ip.pack()

text_target_ip = tk.Text(width=40, height=1,bg="lightblue")
text_target_ip.pack()

btn_listen = tk.Button(window, text="LISTEN", width=50, command=start_listening, bg='lightblue')
btn_listen.pack(anchor=tk.CENTER, expand=True)

btn_camera = tk.Button(window, text="CAMERA 📹", width=50,command= start_camera_stream, bg='lightblue')
btn_camera.pack(anchor=tk.CENTER, expand=True)

btn_screen = tk.Button(window, text="SCREEN SHARE 🖥️", width=50,command=start_screen_sharing, bg='lightblue')
btn_screen.pack(anchor=tk.CENTER, expand=True)

btn_audio = tk.Button(window, text="AUDIO 🔉", width=50,command=start_microphone_stream, bg='lightblue')
btn_audio.pack(anchor=tk.CENTER, expand=True)

window.mainloop()



