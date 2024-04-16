# BabyCam
Video streaming over local network, so you can watch your baby


Resources:
TCP: https://medium.com/@anshulsjr6/building-a-basic-video-streaming-application-in-python-with-opencv-cfb6995e2479
UDP: https://pyshine.com/Send-video-over-UDP-socket-in-Python/



issues to improve:
- framerate is awful
    transitioning to UDP: use TCP sockets to set up initial session: numpy array shape based on webcam
    - UDP is way faster: solution is to UDP instead of TCP. However, must compress images to guarantee no more than 65k bytes per message
    - Alternate solution: only do the TCP setup once in the beginning (send the size of the packets), since TCP allows you to assume payloads of equal size in successive packets (implemented in server.py and client.py)
    - also, the TCP version uses pickle, and struct packing. Can we just use b64 string encoding? would that be faster?
- add audio
- CLI shows IP addresses, not human readable names
- port is assumed -> need to assign it dynamically (may need to set this up using TCP at beginning of streaming session)
- sometimes the client side IP scanning doesn't return all local devices