# BabyCam
Video streaming over local network, so you can watch your baby



issues to improve:
- framerate is awful
    transitioning to UDP: use TCP sockets to set up initial session: numpy array shape based on webcam
    - are number of bytes the same for every frame? if not, do I pad the bytestring?
- add audio
- CLI shows IP addresses, not human readable names
- port is assumed -> need to assign it dynamically
- sometimes the client side IP scanning doesn't return all local devices