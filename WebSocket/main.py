# app.py
from flask import Flask
import Sock
import eventlet
from eventlet import wsgi
from routes import CAR_SIMULATION_ROUTE, ECHO_ROUTE, car_simulation, echo_socket

app = Flask(__name__)
sock = Sock(app)

# Configuration
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 41414

simulation_status = {"running": False}


@sock.route(CAR_SIMULATION_ROUTE)
def car_simulation_route(ws):
    car_simulation(ws, simulation_status)


@sock.route(ECHO_ROUTE)
def echo_route(ws):
    echo_socket(ws)


if __name__ == '__main__':
    wsgi.server(eventlet.listen((SERVER_ADDRESS, SERVER_PORT)), app)