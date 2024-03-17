import cv2, socket, pickle, struct

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
    while True:
        ret, frame = cap.read()
        frame_data = pickle.dumps(frame)
        client_socket.sendall(struct.pack("Q", len(frame_data)))
        print(len(frame_data), struct.pack("Q", len(frame_data)))
        client_socket.sendall(frame_data)
        cv2.imshow('Server', frame)
        if cv2.waitKey(1) == 13:
            break
    cap.release()
    cv2.destroyAllWindows()