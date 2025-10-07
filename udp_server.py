import socket

PORT = 8890
BUFFER_SIZE = 1024

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to listen on all interfaces on port 8890
sock.bind(('0.0.0.0', PORT))

print(f"UDP server listening on port {PORT}...")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"Received from {addr}: {data.decode('utf-8')}")

