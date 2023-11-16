import socket

serverAddressPort = ("127.0.0.1", 50001)
bufferSize = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    msgFromClient = input("Message to server: ")
    bytesToSend = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    replyMsg, serverAddress = UDPClientSocket.recvfrom(bufferSize)
    print("Reply from server:", replyMsg.decode())