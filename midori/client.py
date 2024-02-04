import socket
import sys
from encrypt import *
import random

key = "0xce600392180739a971cacc28c41bd5ad"

msgFromClient = sys.argv[1]
msgFromClient = msgFromClient.ljust(16, "0")
state = encrypt(msgFromClient, key, 128)
digest = ""
for i in range(4):
    for j in range(4):
        digest += hex(state[i][j])[2:].zfill(2)
print("Message sent by client: ", digest)
bytesToSend = str.encode(digest)

serverAddressPort = ("127.0.0.1", 8080)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
