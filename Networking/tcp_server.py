"""
TCP Server

This script creates a TCP server that listens for incoming connections on a specified IP address and port.
When a client connects, the server accepts the connection and spawns a new thread to handle communication
with the client. The server responds with an acknowledgment message after receiving data from the client.
"""

import socket
import threading

# Server configuration
IP = '127.0.0.1'  # IP address to listen on
PORT = 9998       # Port number to listen on

def main():
    """
    Main function to start the TCP server.

    Creates a socket, binds it to the specified IP address and port, and listens for incoming connections.
    When a connection is accepted, it spawns a new thread to handle communication with the client.
    """
    # Create a TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the IP address and port
    server.bind((IP, PORT))

    # Start listening for incoming connections
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    # Main loop to accept incoming connections
    while True:
        # Accept incoming connection
        client, address = server.accept()
        print(f'[*] Accepted connection from {address}')

        # Spawn a new thread to handle communication with the client
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    """
    Function to handle communication with a client.

    Receives data from the client, prints the received message, and sends an acknowledgment back to the client.

    Args:
        client_socket: The socket object representing the client connection.
    """
    with client_socket as sock:
        # Receive data from the client
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')

        # Send acknowledgment back to the client
        sock.send(b'ACK')

if __name__ == '__main__':
    main()
