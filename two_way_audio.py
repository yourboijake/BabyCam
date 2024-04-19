from server_audio import stream_out
from client_audio import stream_in
import threading

port_out = int(input('Port for output stream: '))
port_in = int(input('Port for input stream: '))
server_ip = input('IP address of server for input stream: ')


print('starting connection')

thread1 = threading.Thread(target=stream_out, args=(port_out), name='stream_out')
thread2 = threading.Thread(target=stream_in, args=(port_in, server_ip), name='stream_in')

thread1.start()
thread2.start()

thread1.join()
thread2.join()