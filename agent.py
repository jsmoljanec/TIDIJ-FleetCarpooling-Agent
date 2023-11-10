from flask import Flask
from flask_sock import Sock
import sys

import eventlet
from eventlet import wsgi

app = Flask(__name__)
sock = Sock(app)

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

