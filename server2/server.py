import grpc
from concurrent import futures
import sys
import os

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from generated.weather_pb2 import CityRequest, TemperatureResponse
from generated.weather_pb2_grpc import WeatherServiceServicer, add_WeatherServiceServicer_to_server

class WeatherService(WeatherServiceServicer):
    def GetTemperature(self, request, context):
        print(f" Server2 received request for: {request.city}")
        return TemperatureResponse(
            city=request.city,
            temperature=26.0
        )

def serve():
    print(" Starting Server2 on port 50052...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WeatherServiceServicer_to_server(WeatherService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print(" Server2 is running on port 50052")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print(" Server2 stopped")

if __name__ == '__main__':
    serve()