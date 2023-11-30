# routes.py
import json
import time

CAR_SIMULATION_ROUTE = '/route-simulation'
ECHO_ROUTE = '/echo'

# Constants for car simulation
START_POINT = {"latitude": 37.7749, "longitude": -122.4194}
END_POINT = {"latitude": 37.7749, "longitude": -122.4313}

START = "start"
END = "end"


def car_simulation(ws, simulation_status):
    print(f"Route connected: {ws.receive()}")

    while True:
        message = ws.receive()

        if message == START and not simulation_status["running"]:
            simulation_status["running"] = True
            for i in range(11):
                progress = i / 10.0
                current_location = {
                    "latitude": START_POINT["latitude"] + progress * (END_POINT["latitude"] - START_POINT["latitude"]),
                    "longitude": START_POINT["longitude"] + progress * (
                                END_POINT["longitude"] - START_POINT["longitude"]),
                }
                print(current_location)
                ws.send(json.dumps(current_location))
                time.sleep(0.5)

            simulation_status["running"] = False

        elif message == END and simulation_status["running"]:
            simulation_status["running"] = False
            print("Simulation stopped")


def echo_socket(ws):
    print("Echo route connected with client!")
    while True:
        message = ws.receive()
        if message is not None:
            print("Received message from client:", message)
            response_message = f"Response to: {message} and the agent sends greetings"
            ws.send(response_message)
