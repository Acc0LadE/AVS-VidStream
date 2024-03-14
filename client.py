import tkinter as tk
import socket
import ssl
from vidstream import *
import threading
import pyaudio

local_ip_address = socket.gethostbyname(socket.gethostname())
server = StreamingServer(local_ip_address, 7777)
receiver = StreamingServer(local_ip_address, 6666)

def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t1.start()
    t2.start()

def start_camera_stream():
    camera_client = CameraClient(text_target_ip.get(1.0,'end-1c'), 9999)
    t3 = threading.Thread(target=camera_client.start_stream)
    t3.start()

def start_screen_sharing():
    screen_client = ScreenShareClient(text_target_ip.get(1.0,'end-1c'), 9999)
    t4 = threading.Thread(target=screen_client.start_stream)
    t4.start()

def start_audio_stream():
    audio_sender = AudioSender(text_target_ip.get(1.0,'end-1c'), 8888)  # Connect to the correct port for audio
    t5 = threading.Thread(target=audio_sender.start_stream)
    t5.start()

def receive_audio_server():
    # Constants
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    port = 12345  # Port to connect

    # Connect to server
    client_socket.connect((host, port))

    print("Connected to server")

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Closing connection...")
        client_socket.close()
        stream.stop_stream()
        stream.close()
        p.terminate()


window = tk.Tk()
window.title("CLIENT")
window.geometry('500x500')

label_target_ip = tk.Label(window,text="\nTarget IP:")
label_target_ip.pack()

text_target_ip = tk.Text(width=40, height=1, bg="lightblue")
text_target_ip.pack()

btn_listen = tk.Button(window, text="LISTEN", width=50, command=start_listening, bg='lightblue')
btn_listen.pack(anchor=tk.CENTER, expand=True)

btn_camera = tk.Button(window, text="CAMERA 📹", width=50,command= start_camera_stream, bg='lightblue')
btn_camera.pack(anchor=tk.CENTER, expand=True)

btn_screen = tk.Button(window, text="SCREEN SHARE 🖥️", width=50,command=start_screen_sharing, bg='lightblue')
btn_screen.pack(anchor=tk.CENTER, expand=True)

btn_audio = tk.Button(window, text="AUDIO 🔉", width=50,command=receive_audio_server, bg='lightblue')
btn_audio.pack(anchor=tk.CENTER, expand=True)

window.mainloop()
