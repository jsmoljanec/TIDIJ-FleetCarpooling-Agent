from flask import Flask
from flask_sock import Sock
import sys
import time
import json
import eventlet
from eventlet import wsgi

app = Flask(__name__)
sock = Sock(app)

# Configuration
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 41414

CAR_SIMULATION_ROUTE = '/route-simulation'
ECHO_ROUTE = '/echo'

# Constants for car simulation
START_POINT = {"latitude": 37.7749, "longitude": -122.4194}
END_POINT = {"latitude": 37.7749, "longitude": -122.4313}

@sock.route(CAR_SIMULATION_ROUTE)
def car_simulation(ws):
    for i in range(11):
        progress = i / 10.0
        current_location = {
            "latitude": START_POINT["latitude"] + progress * (END_POINT["latitude"] - START_POINT["latitude"]),
            "longitude": START_POINT["longitude"] + progress * (END_POINT["longitude"] - START_POINT["longitude"]),
        }
        ws.send(json.dumps(current_location))
        time.sleep(1)

@sock.route(ECHO_ROUTE)
def echo_socket(ws):
    print("Client connected")
    while True:
        message = ws.receive()
        if message is not None:
            print("Received message from client:", message)
            response_message = f"Response to: {message} and the server sends greetings"
            ws.send(response_message)

def run_server():
    try:
        if __name__ == '__main__':
            wsgi.server(eventlet.listen((SERVER_ADDRESS, SERVER_PORT)), app)
    except KeyboardInterrupt:
        print('\nScript stopped.')
        sys.exit(0)

if __name__ == '__main__':
    run_server()
