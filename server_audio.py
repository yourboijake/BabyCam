import pyaudio
import wave
import socket
import keyboard

#set up server side socket
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '0.0.0.0'
print(host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

#wait for client connection
msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
print('GOT connection from ',client_addr)


#begin streaming audio to client
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 20
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

in_stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

out_stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    output=True)

frames = []  # Initialize array to store frames

while True:
    data = in_stream.read(chunk)
    #send audio to client socket
    #frames.append(data)
    server_socket.sendto(data,client_addr)

    if keyboard.is_pressed('q'): break

# Stop and close the stream 
in_stream.stop_stream()
in_stream.close()
server_socket.close()

'''
for fr in frames:
    out_stream.write(fr)


out_stream.stop_stream()
out_stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

import pdb; pdb.set_trace()

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

'''