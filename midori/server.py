import socket
from decrypt import *

localIP = "127.0.0.1"

localPort = 8080

bufferSize = 1024

msgFromServer = "Message recieved"

bytesToSend = str.encode(msgFromServer)
# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")


# Listen for incoming datagrams
key = "0xce600392180739a971cacc28c41bd5ad"

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    message = message.decode()
    clientMsg = "Message from Client:{}".format(message)
    state = []
    for i in range(4):
        state.append(
            [int(message[i * 8 + j : i * 8 + j + 2], 16) for j in range(0, 8, 2)]
        )

    state = decrypt(state, key, 128)
    text = ""
    for i in range(4):
        for j in range(4):
            text += chr(state[i][j])
    print("Decrypted Text: ", text)

    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
