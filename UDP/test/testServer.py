import socket, time

localIP = ''
print(localIP)

localPort = 50001
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

is_vehicle_running = False


def start_vehicle(destination_address):
    global is_vehicle_running
    is_vehicle_running = True
    while is_vehicle_running:
        time.sleep(5)
        vehicle_location = f"Latitude: {41.8781}, Longitude: {87.6298}"
        UDPServerSocket.sendto(vehicle_location.encode("utf-8"), destination_address)


def stop_vehicle(destination_address):
    global is_vehicle_running
    is_vehicle_running = False
    UDPServerSocket.sendto("Zaustavljam vozilo!".encode("utf-8"), destination_address)


while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode("utf-8")
    address = bytesAddressPair[1]

    # command = "Message from Client: ".format(message)
    command = message.lower()

    clientIP = "Client IP Address:{}".format(address)
    print(f"{message}\n{clientIP}\n-----------------\n")

    if command == "start":
        print(f"Vozilo sa adrese {address} pokrenuto.")
        start_vehicle(address)
    elif command == "stop":
        print(f"Vozilo sa adrese {address} zaustavljeno.")
        stop_vehicle(address)

    # Sending a reply to the client
    replyMsg = f"Hello test agent, thanks for messaging!\n-----------------\n"
    UDPServerSocket.sendto(str.encode(replyMsg), address)
