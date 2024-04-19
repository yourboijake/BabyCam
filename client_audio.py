import socket, pyaudio
import keyboard

#set up client side socket
BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '192.168.1.102'
print(host_ip)
port = 9999
message = b'Hello'

#establish connection with server
client_socket.sendto(message,(host_ip,port))

#set up audio output
p = pyaudio.PyAudio()
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
#seconds = 20
out_stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    output=True)

#begin recieving audio stream
while True:
    data,_ = client_socket.recvfrom(BUFF_SIZE)
    out_stream.write(data)

    if keyboard.is_pressed('q'): break

