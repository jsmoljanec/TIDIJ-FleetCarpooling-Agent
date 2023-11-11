from flask import Flask
from flask_sock import Sock
import sys, time, json

import eventlet
from eventlet import wsgi

app = Flask(__name__)
sock = Sock(app)

@sock.route('/route-simulation')
def car_simulation(ws):
    start_point = {"latitude": 37.7749, "longitude": -122.4194}
    end_point = {"latitude": 37.7749, "longitude": -122.4313}

    for i in range(11):
        progress = i / 10.0  # Računanje napretka
        current_location = {
            "latitude": start_point["latitude"] + progress * (end_point["latitude"] - start_point["latitude"]),
            "longitude": start_point["longitude"] + progress * (end_point["longitude"] - start_point["longitude"]),
        }
        ws.send(json.dumps(current_location))
        time.sleep(1)

@sock.route('/echo')
def echo_socket(ws):
    print("Klijent povezan")
    while True:
        message = ws.receive()
        if message is not None:
            print("Primljena poruka od klijenta:", message)
            response_message = f"Odgovor na: {message} i server saljeee pozz"
            ws.send(response_message)

while True:
    try:
        if __name__ == '__main__':
            wsgi.server(eventlet.listen(('127.0.0.1', 41414)), app)
        pass
    except KeyboardInterrupt:
        print('\nSkripta je zaustavljena.')
        sys.exit(0)

