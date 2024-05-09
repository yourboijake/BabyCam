import cv2, socket, pickle, struct
import pyaudio
import socket
from datetime import datetime, timedelta
import imutils
import base64
import time

class Server:
    video_port = None
    audio_port = None

    def stream_video_udp(self):
        BUFF_SIZE = 65536
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_ip = '0.0.0.0'
        socket_address = (host_ip,self.video_port)
        server_socket.bind(socket_address)
        print('Listening at:',socket_address)

        vid = cv2.VideoCapture(0)
        fps,st,frames_to_count,cnt = (0,0,20,0)

        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
        WIDTH=400
        while(vid.isOpened()):
            _,frame = vid.read()
            frame = imutils.resize(frame,width=WIDTH)
            encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,90])
            message = base64.b64encode(buffer)
            server_socket.sendto(message,client_addr)
            frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                server_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1

        vid.release()
        cv2.destroyAllWindows()
        server_socket.close()
        print('closed server socket')

    def stream_video_tcp():
        #declare socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 8888))

        #accept connection
        server_socket.listen(5)
        print("server is listening")
        client_socket, client_address = server_socket.accept()
        print(f"connection from {client_address} accepted")

        cap = cv2.VideoCapture(0)
        _, testframe = cap.read()
        testframe_data = pickle.dumps(testframe)
        client_socket.sendall(struct.pack("Q", len(testframe_data)))

        shapes, framesends = [], []
        while True:
            _, frame = cap.read()
            frame_data = pickle.dumps(frame)
            shapes.append((frame.shape, len(frame_data)))
                
            t1 = datetime.now()
            client_socket.sendall(frame_data)
            framesends.append((datetime.now() - t1).microseconds)
            cv2.imshow('Server', frame)
            if cv2.waitKey(1) == 13:
                break

        cap.release()
        cv2.destroyAllWindows()
        server_socket.close()
        print('closed server socket')
        print('avg frame send time: ', sum(framesends) / len(framesends))
        print(shapes)

    def stream_audio(self):
        #set up server side socket
        BUFF_SIZE = 65536
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_ip = '0.0.0.0'
        print(host_ip)
        socket_address = (host_ip,self.audio_port)
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