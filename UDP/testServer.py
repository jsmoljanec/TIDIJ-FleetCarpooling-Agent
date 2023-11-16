import socket

localIP = "127.0.0.1"
localPort = 50001
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(f"{clientMsg}\n{clientIP}\n-----------------\n")

    # Sending a reply to the client
    replyMsg = f"Hello test agent, thanks for messaging!\n-----------------\n"
    UDPServerSocket.sendto(str.encode(replyMsg), address)