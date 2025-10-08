from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv

load_dotenv()

class InfluxWriter:
    def __init__(self, bucket="drone_data"):
        self.client = InfluxDBClient(
            url="http://localhost:8086",
            token="admin-token",
            org="drone_monitor"
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket

    def write_stats(self, data):
        batPoint = (
            Point("battery")
            .tag("source", data["source"])
            .field("bat", float(data["bat"]))
            .time(data["timestamp"])
        )

        posPoint = (
            Point("position")
            .tag("source", data["source"])
            .field("vgx", float(data["vgx"]))
            .field("vgy", float(data["vgy"]))
            .field("vgz", float(data["vgz"]))
            .field("agx", float(data["agx"]))
            .field("agy", float(data["agy"]))
            .field("agz", float(data["agz"]))
            .time(data["timestamp"])   
        )
        try:
            self.write_api.write(bucket=self.bucket, record=batPoint)
            self.write_api.write(bucket=self.bucket, record=posPoint)
        except Exception as e:
            print(f'Error: {e}')
