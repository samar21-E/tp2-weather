I can't directly create or download files, but I'll provide you with the complete README.md content that you can copy and save as a file. Here's the full markdown content:

```markdown
# Lab 2: Service-Oriented Architecture with gRPC and Load Balancing

## 📋 Lab Overview
This lab demonstrates a Service-Oriented Architecture (SOA) implementation using gRPC with client-side load balancing. The system consists of a client and two weather service servers with round-robin request distribution.

## 🎯 Lab Objectives
- Understand the role of **Service-Oriented Architecture (SOA)** in distributed systems
- Learn how to design and implement **gRPC services** in different programming languages
- Implement **two backend servers** and a **client** with **round-robin load balancing**
- Analyze and visualize the system using UML diagrams
- Interpret the output to understand how load balancing distributes requests

## 🏗️ System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SYSTEM COMPONENTS                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     WEATHER CLIENT                              │   │
│  │                                                                 │   │
│  │  ┌─────────────────┐    ┌─────────────────┐                     │   │
│  │  │  RoundRobin     │    │   ServerList    │                     │   │
│  │  │   Balancer      │    │                 │                     │   │
│  │  │                 │    │ - localhost:50051│                    │   │
│  │  │ - nextServer()  │    │ - localhost:50052│                    │   │
│  │  │ - rotate()      │    │                 │                     │   │
│  │  └─────────────────┘    └─────────────────┘                     │   │
│  │              │                               │                   │   │
│  │              ▼                               ▼                   │   │
│  │  ┌─────────────────┐            ┌─────────────────┐             │   │
│  │  │  gRPC Client    │            │  Request Logger  │             │   │
│  │  │                 │            │                 │             │   │
│  │  │ - makeCall()    │            │ - logRequest()  │             │   │
│  │  │ - handleResp()  │            │ - displayResult()│            │   │
│  │  └─────────────────┘            └─────────────────┘             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                               │                                         │
│                               │ implements                              │
│                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   WEATHER SERVICE                              │   │
│  │                    (gRPC Contract)                             │   │
│  │                                                                 │   │
│  │  service WeatherService {                                      │   │
│  │    rpc GetTemperature(CityRequest) returns (TemperatureResponse)│   │
│  │  }                                                              │   │
│  │                                                                 │   │
│  │  message CityRequest {                                          │   │
│  │    string city = 1;                                             │   │
│  │  }                                                              │   │
│  │                                                                 │   │
│  │  message TemperatureResponse {                                  │   │
│  │    string city = 1;                                             │   │
│  │    double temperature = 2;                                      │   │
│  │  }                                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                               │                                         │
│                   ┌─────────────┴───────────┐                           │
│                   │                         │                           │
│                   ▼                         ▼                           │
│  ┌─────────────────────────┐   ┌─────────────────────────┐             │
│  │     WEATHER SERVER 1    │   │     WEATHER SERVER 2    │             │
│  │                         │   │                         │             │
│  │ ┌─────────────────────┐ │   │ ┌─────────────────────┐ │             │
│  │ │    gRPC Server      │ │   │ │    gRPC Server      │ │             │
│  │ │                     │ │   │ │                     │ │             │
│  │ │ - port: 50051       │ │   │ │ - port: 50052       │ │             │
│  │ │ - maxWorkers: 10    │ │   │ │ - maxWorkers: 10    │ │             │
│  │ └─────────────────────┘ │   │ └─────────────────────┘ │             │
│  │                         │   │                         │             │
│  │ ┌─────────────────────┐ │   │ ┌─────────────────────┐ │             │
│  │ │  Service Handler    │ │   │ │  Service Handler    │ │             │
│  │ │                     │ │   │ │                     │ │             │
│  │ │ - GetTemperature()  │ │   │ │ - GetTemperature()  │ │             │
│  │ │ - returns: 25.0°C   │ │   │ │ - returns: 26.0°C   │ │             │
│  │ └─────────────────────┘ │   │ └─────────────────────┘ │             │
│  │                         │   │                         │             │
│  │ ┌─────────────────────┐ │   │ ┌─────────────────────┐ │             │
│  │ │     Request Logger  │ │   │ │     Request Logger  │ │             │
│  │ │                     │ │   │ │                     │ │             │
│  │ │ - logIncoming()     │ │   │ │ - logIncoming()     │ │             │
│  │ │ - trackMetrics()    │ │   │ │ - trackMetrics()    │ │             │
│  │ └─────────────────────┘ │   │ └─────────────────────┘ │             │
│  └─────────────────────────┘   └─────────────────────────┘             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│               ROUND-ROBIN LOAD BALANCING SEQUENCE                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Client           LoadBalancer        Server1           Server2         │
│    │                   │                 │                 │            │
│    │ 1. makeRequest()  │                 │                 │            │
│    │───────────────────▶                 │                 │            │
│    │                   │                 │                 │            │
│    │                   │ 2. nextServer() │                 │            │
│    │                   │─────────────────┐                 │            │
│    │                   │◀────────────────┘                 │            │
│    │                   │ 3. select Server1                 │            │
│    │                   │───────────────────────────────────┐            │
│    │                   │◀──────────────────────────────────┘            │
│    │                   │                 │                 │            │
│    │ 4. GetTemperature("Tunis")          │                 │            │
│    │─────────────────────────────────────▶                 │            │
│    │                   │                 │                 │            │
│    │                   │                 │ 5. Process Request           │
│    │                   │                 │ ─────────────────┐           │
│    │                   │                 │◀─────────────────┘           │
│    │                   │                 │                 │            │
│    │ 6. TemperatureResponse(25.0°C)      │                 │            │
│    │◀─────────────────────────────────────                 │            │
│    │                   │                 │                 │            │
│    │ 7. makeRequest()  │                 │                 │            │
│    │───────────────────▶                 │                 │            │
│    │                   │                 │                 │            │
│    │                   │ 8. nextServer() │                 │            │
│    │                   │─────────────────┐                 │            │
│    │                   │◀────────────────┘                 │            │
│    │                   │ 9. select Server2                 │            │
│    │                   │───────────────────────────────────┐            │
│    │                   │◀──────────────────────────────────┘            │
│    │                   │                 │                 │            │
│    │10. GetTemperature("Tunis")          │                 │            │
│    │───────────────────────────────────────────────────────▶            │
│    │                   │                 │                 │            │
│    │                   │                 │11. Process Request           │
│    │                   │                 │ ─────────────────┐           │
│    │                   │                 │◀─────────────────┘           │
│    │                   │                 │                 │            │
│    │12. TemperatureResponse(26.0°C)      │                 │            │
│    │◀───────────────────────────────────────────────────────            │
│    │                   │                 │                 │            │
│    │13. Display Results│                 │                 │            │
│    │ ─────────────────┐│                 │                 │            │
│    │◀─────────────────┘│                 │                 │            │
│    │                   │                 │                 │            │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Load Balancing Algorithm

### Round-Robin Logic
```
Initialization:
servers = ["localhost:50051", "localhost:50052"]
current_index = 0

Algorithm:
function next_server():
server = servers[current_index]
current_index = (current_index + 1) % len(servers)
return server

Request Flow:
Request 1 → Server1 (25.0°C)
Request 2 → Server2 (26.0°C)
Request 3 → Server1 (25.0°C)
Request 4 → Server2 (26.0°C)
Request 5 → Server1 (25.0°C)
Request 6 → Server2 (26.0°C)
```

## 📊 Expected Output

```
🔄 Starting Round-Robin Load Balancing Demo...
==================================================

📨 Request 1: Connecting to localhost:50051
✅ Response: Tunis 25.0°C
⏱️ Response time: 15ms

📨 Request 2: Connecting to localhost:50052  
✅ Response: Tunis 26.0°C
⏱️ Response time: 12ms

📨 Request 3: Connecting to localhost:50051
✅ Response: Tunis 25.0°C
⏱️ Response time: 18ms

📨 Request 4: Connecting to localhost:50052
✅ Response: Tunis 26.0°C
⏱️ Response time: 14ms

==================================================
🎯 Round-Robin Load Balancing Completed!
• Total Requests: 4
• Server1 Responses: 2 (50%)
• Server2 Responses: 2 (50%)
• Average Response Time: 14.75ms
```

## 🏷️ Diagram Legend

### Relationship Types:
- `─────▶` **Dependency**: Client depends on Service interface
- `┌──┐` **Realization**: Servers implement Service contract  
- `└──┘` 
- `─────┼` **Association**: Direct communication link

### Component Types:
- **Rectangle**: Component/Class
- **Interface Box**: Contract/Interface definition  
- **Rounded Rectangle**: Sub-component/Module

### Sequence Types:
- **Solid Arrow**: Synchronous message
- **Dashed Arrow**: Return message
- **Activation Box**: Method execution duration

## 🛠️ Technical Implementation

### Protocol Buffer Definition
```proto
syntax = "proto3";

package weather;

service WeatherService {
  rpc GetTemperature(CityRequest) returns (TemperatureResponse);
}

message CityRequest {
  string city = 1;
}

message TemperatureResponse {
  string city = 1;
  double temperature = 2;
}
```

### Key Components
- **WeatherClient**: Python/Go client with round-robin load balancing
- **WeatherServer1**: Server instance on port 50051 (returns 25.0°C)
- **WeatherServer2**: Server instance on port 50052 (returns 26.0°C)
- **WeatherService**: gRPC service contract defining the API

## 🎯 Learning Outcomes

This lab demonstrates:
- **Service-Oriented Architecture** principles
- **gRPC** for efficient service communication
- **Client-side load balancing** with round-robin algorithm
- **System design** using UML diagrams
- **Distributed system** scalability patterns

## 📝 Lab Report Requirements

Students must include:
1. Complete source code for all components
2. UML Component and Sequence diagrams
3. Analysis of load balancing behavior
4. Explanation of SOA principles demonstrated
5. Discussion of potential enhancements

---
*Lab 2 - Service-Oriented Architecture with gRPC and Load Balancing*
```

To save this as a .md file:

1. **Copy** the entire content above
2. **Open** a text editor (VS Code, Notepad++, etc.)
3. **Paste** the content
4. **Save as** `README.md`
5. **Set file type** to "All Files" with `.md` extension

The file is now ready for your lab submission!