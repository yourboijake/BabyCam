import pyaudio
import socket
import keyboard

def stream_out(port):
    #set up server side socket
    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    host_ip = '0.0.0.0'
    print(host_ip)
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

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    in_stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    while True:
        data = in_stream.read(chunk)
        #send audio to client socket
        server_socket.sendto(data,client_addr)

        #if keyboard.is_pressed('q'): break

    # Stop and close the stream 
    in_stream.stop_stream()
    in_stream.close()
    server_socket.close()