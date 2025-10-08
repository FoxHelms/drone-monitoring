import sys, time
from dotenv import load_dotenv
from datetime import datetime
from kafka import KafkaProducer
import json
import socket

PORT = 8890
BUFFER_SIZE = 1518
TOPIC = "drone.stats"

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to listen on all interfaces on port 8890
sock.bind(('0.0.0.0', PORT))

print(f"UDP server listening on port {PORT}...")

while True:
    # time.sleep(1)
    data, addr = sock.recvfrom(BUFFER_SIZE)
    dataStr = data.decode('utf-8')
    # pitch:17;roll:10;yaw:2;vgx:0;vgy:0;vgz:0;templ:55;temph:59;tof:10;h:0;bat:79;baro:-11.73;time:9;agx:314.00;agy:-176.00;agz:-935.00;
    dataDict = {k: float(v) for k, v in (item.split(':') for item in dataStr.strip().strip(';').split(';'))}
    dataDict["source"] = "onboard_sensors"
    dataDict["timestamp"] = str(datetime.now())
    print(f"Received from {addr}: {dataDict}")
    producer.send(
        TOPIC,
        key=dataDict["source"],
        value=dataDict
    )
    print('sent!')
