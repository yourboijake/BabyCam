import cv2, socket, pickle, struct
from datetime import datetime, timedelta
import imutils
import base64
import time

def run_server_udp():

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

    vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
    fps,st,frames_to_count,cnt = (0,0,20,0)

    while True:
        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
        WIDTH=400
        resizes, imencodes, b64encodes, framesends = [], [], [], []
        while(vid.isOpened()):
            _,frame = vid.read()
            frame = imutils.resize(frame,width=WIDTH)
            encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,90])
            message = base64.b64encode(buffer)
            print(len(buffer), type(buffer))
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
    cap.release()
    cv2.destroyAllWindows()
    server_socket.close()
    print('closed server socket')
    print('avg dump time: ', sum(resizes) / len(resizes))
    print('avg q time: ', sum(imencodes) / len(imencodes))
    print('avg b64 encode time: ', sum(b64encodes) / len(b64encodes))
    print('avg framesend time: ', sum(framesends) / len(framesends))

def run_server_tcp():
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

