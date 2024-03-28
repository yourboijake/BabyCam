import cv2, socket, pickle, struct
from datetime import datetime, timedelta

def run_server():

    #declare socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))

    #accept connection from 
    server_socket.listen(5)
    print("Server is listening...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} accepted")

    #start video capture, and send to client
    cap = cv2.VideoCapture(0)
    dumps, qs, framesends = [], [], []
    while True:
        ret, frame = cap.read()
        t1 = datetime.now()
        frame_data = pickle.dumps(frame)
        dumps.append((datetime.now() - t1).microseconds)
        
        t1 = datetime.now()
        client_socket.sendall(struct.pack("Q", len(frame_data)))
        qs.append((datetime.now() - t1).microseconds)
        
        client_socket.sendall(frame_data)
        framesends.append((datetime.now() - t1).microseconds)
        cv2.imshow('Server', frame)
        if cv2.waitKey(1) == 13:
            break
    cap.release()
    cv2.destroyAllWindows()
    server_socket.close()
    print('closed server socket')
    print('avg dump time: ', sum(dumps) / len(dumps))
    print('avg q time: ', sum(qs) / len(qs))
    print('avg framesend time: ', sum(framesends) / len(framesends))
