import cv2, socket, pickle, struct
import numpy as np
import time
import base64
import socket, pyaudio


class Client:
    video_port = None
    audio_port = None
    server_ip = None

    def stream_video_udp(self):
        BUFF_SIZE = 65536
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        message = b'Hello'

        client_socket.sendto(message,(self.server_ip,self.video_port))
        fps,st,frames_to_count,cnt = (0,0,20,0)
        while True:
            packet,_ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data,dtype=np.uint8)
            frame = cv2.imdecode(npdata,1)
            frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1

    def stream_video_tcp(server_ip):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 8888))

        #get size of frames for session metadata
        data = b""
        payload_size = struct.calcsize("Q")
        framesize_packet = client_socket.recv(4 * 1024)
        framesize = struct.unpack

        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # 4K buffer size
                if not packet:
                    break
                data += packet
            if not data:
                break
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)  # 4K buffer size
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow('Client', frame)
            if cv2.waitKey(1) == 13:
                break
        cv2.destroyAllWindows()
        client_socket.close()
        print('closed client socket')


    def stream_audio(self):

        #set up client side socket
        BUFF_SIZE = 65536
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        print(self.server_ip, self.audio_port)
        message = b'Hello'

        #establish connection with server
        client_socket.sendto(message,(self.server_ip,self.audio_port))

        #set up audio output
        p = pyaudio.PyAudio()
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        out_stream = p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            output=True)

        #begin recieving audio stream
        while True:
            data,_ = client_socket.recvfrom(BUFF_SIZE)
            out_stream.write(data)

            #if keyboard.is_pressed('q'): break