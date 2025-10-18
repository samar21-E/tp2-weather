import grpc
import itertools
import time
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated import weather_pb2
from generated import weather_pb2_grpc

def run_round_robin():
    print("Starting Round-Robin Load Balancing Demo...")
    print("=" * 50)

    servers = ["localhost:50051", "localhost:50052"]
    server_cycle = itertools.cycle(servers)

    for request_number in range(1, 7):
        current_server = next(server_cycle)
        print(f"\n Request {request_number}: Connecting to {current_server}")

        try:
            channel = grpc.insecure_channel(current_server)
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            response = stub.GetTemperature(weather_pb2.CityRequest(city="Tunis"))
            print(f" Response: {response.city} {response.temperature}°C")
        except grpc.RpcError as e:
            print(f" Error connecting to {current_server}: {e}")

        time.sleep(1)

    print("\n" + "=" * 50)
    print(" Round-Robin demonstration completed!")

if __name__ == '__main__':
    run_round_robin()