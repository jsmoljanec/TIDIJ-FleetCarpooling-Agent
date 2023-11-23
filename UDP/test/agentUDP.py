import socket

hostname = socket.gethostname()
ip_address = "127.0.0.1"
# ip_address = socket.gethostbyname(hostname)

port = 50001

serverAddressPort = (ip_address, port)
bufferSize = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    msgFromClient = input("Message to server: ")
    bytesToSend = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    replyMsg, serverAddress = UDPClientSocket.recvfrom(bufferSize)
    print("Reply from server:", replyMsg.decode())
