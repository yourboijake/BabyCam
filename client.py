import cv2, socket, pickle, struct

def run_client(server_ip):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 8888))

    #get size of frames for session metadata
    data = b""
    payload_size = struct.calcsize("Q")
    framesize_packet = client_socket.recv(4 * 1024)
    framesize = struct.unpack("Q", framesize_packet)[0]

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet
        if not data:
            break
        while len(data) < framesize:
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