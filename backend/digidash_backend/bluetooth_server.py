'''
Main server process for connecting to client devices and sending over sensor readings
'''

import bluetooth
import json
from signal_reader import SignalReaderDummy

def start_bluetooth_server():
    sr = SignalReaderDummy(**config)

    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1  # Choose a Bluetooth port number (must match the client)

    try:
        server_socket.bind(("", port))
        server_socket.listen(1)

        print("Bluetooth server started. Waiting for connections...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to client: {client_address}")

            try:
                while True:
                    # Get sensor readings
                    sensor_data = sr.sample_signal()

                    # Send sensor readings to the client
                    data_to_send = json.dumps(sensor_data)
                    client_socket.send(data_to_send)

                    # You can also receive data from the client if needed
                    # received_data = client_socket.recv(1024)

            except Exception as e:
                print(f"Bluetooth communication error: {e}")
                client_socket.close()

    except Exception as e:
        print(f"Bluetooth server error: {e}")
    finally:
        server_socket.close()

if __name__ == '__main__':
    with open('config1.json', 'r') as f:
        config = json.load(f)

    start_bluetooth_server()
