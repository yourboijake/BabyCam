import cv2, socket, pickle, struct
from datetime import datetime, timedelta
import imutils
import base64
import time

def run_server():

    #declare socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))

    #accept connection from 
    server_socket.listen(5)
    print("Server is listening...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} accepted")
    
    #send number of bytes in image to client
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame_data = pickle.dumps(frame)
    client_socket.sendall(struct.pack("Q", len(frame_data)))

    #begin streaming
    WIDTH = 400
    fps,st,frames_to_count,cnt = (0,0,20,0)
    resizes, imencodes, b64encodes, framesends = [], [], [], []
    while(cap.isOpened()):
        _,frame = cap.read()
        t = datetime.now()
        frame = imutils.resize(frame,width=WIDTH)
        imencodes.append((datetime.now() - t).microseconds)

        t = datetime.now()
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,95])
        imencodes.append((datetime.now() - t).microseconds)

        t = datetime.now()
        message = base64.b64encode(buffer)
        b64encodes.append((datetime.now() - t).microseconds)

        t = datetime.now()
        server_socket.sendto(message,client_address)
        framesends.append((datetime.now() - t).microseconds)

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

    ''' 
    this method uses TCP packets, replaced by UDP method above
    while True:
        ret, frame = cap.read()
        t1 = datetime.now()
        frame_data = pickle.dumps(frame)
        shapes.append((frame.shape, len(frame_data)))
        dumps.append((datetime.now() - t1).microseconds)
        
        t1 = datetime.now()
        client_socket.sendall(struct.pack("Q", len(frame_data)))
        qs.append((datetime.now() - t1).microseconds)
        
        t1 = datetime.now()
        client_socket.sendall(frame_data)
        framesends.append((datetime.now() - t1).microseconds)
        cv2.imshow('Server', frame)
        if cv2.waitKey(1) == 13:
            break
    '''
#    resizes, imencodes, b64encodes, framesends = [], [], [], []

    cap.release()
    cv2.destroyAllWindows()
    server_socket.close()
    print('closed server socket')
    print('avg dump time: ', sum(resizes) / len(resizes))
    print('avg q time: ', sum(imencodes) / len(imencodes))
    print('avg b64 encode time: ', sum(b64encodes) / len(b64encodes))
    print('avg framesend time: ', sum(framesends) / len(framesends))
