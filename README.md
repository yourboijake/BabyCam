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
    - use high quality images, do I use RTP for transferring that?
- add audio -> done
- CLI shows IP addresses, not human readable names (is there a way to do this? or do some devices simply not have network names?)
- port is assumed -> need to assign it dynamically (may need to set this up using TCP at beginning of streaming session)
- sometimes the client side IP scanning doesn't return all local devices -> solution pick the IANA User Ports (1024-49151)
- permit multi cast to multiple client nodes
- write a mobile app that talks to other device networks as well


additional misc:
- 2 way audio logic: 
    - swap port and IP information
    - set up listener first (pyaudio input + client-side socket), assign as daemon thread
    - set up server-side output (pyaudio record + server-side socket)
    - run infinite while loop, sending recorded audio frames to output port
- example code: https://github.com/engineer-man/youtube/blob/master/141/client.py 
- open question: does it need to be separate ports for 2-way audio streaming?