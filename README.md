# smart-home
Monorepo for smart home 


### 1. Entity Relationship Diagram (ERD)
```mermaid
erDiagram
    USER ||--o{ ACCOUNT : owns
    ACCOUNT ||--o{ WORKSPACE : has
    WORKSPACE ||--o{ ROOM : contains
    ROOM ||--o{ FUNCTION : includes
    DEVICE ||--o{ FUNCTION : implements
    USER ||--o{ TASK : creates
    FUNCTION ||--o{ TASK : triggered_by

    USER {
        string id
        string email
        string name
        string role
    }

    ACCOUNT {
        string id
        string name
    }

    WORKSPACE {
        string id
        string accountId
        string name
        string address
    }

    ROOM {
        string id
        string workspaceId
        string name
    }

    DEVICE {
        string id
        string name
        string ownerId
        string mqttTopic
    }

    FUNCTION {
        string id
        string deviceId
        string roomId
        string type
        string name
        string unit
    }

    TASK {
        string id
        string userId
        string functionId
        datetime scheduledTime
        int duration
        string command
    }
```

### 2. DTO Examples
```ts
// RegisterUserRequestDTO
{
  email: string,
  password: string,
  name: string
}

// CreateWorkspaceRequestDTO
{
  accountId: string,
  name: string,
  address: string
}

// BindDeviceDTO
{
  deviceId: string,
  accountId: string,
  mqttTopic: string
}

// CreateFunctionDTO
{
  deviceId: string,
  roomId: string,
  type: "light" | "watering" | "blinds" | "temperature" | "humidity",
  name: string
}

// CreateTaskDTO
{
  functionId: string,
  command: string,
  scheduledTime?: datetime,
  duration?: number
}
```

### 3. Flow Diagrams
#### 3.1 Device Binding Flow
```mermaid
sequenceDiagram
  participant User
  participant UI
  participant API Gateway
  participant Device Service
  participant MQTT Broker

  User->>UI: Add Device
  UI->>API Gateway: POST /devices
  API Gateway->>Device Service: registerDevice()
  Device Service->>MQTT Broker: registerTopic(deviceId)
  Device Service-->>API Gateway: 200 OK
  API Gateway-->>UI: Device registered
```

#### 3.2 Execute Function Immediately
```mermaid
sequenceDiagram
  participant User
  participant UI
  participant API Gateway
  participant Task Service
  participant Function Service
  participant MQTT Broker
  participant ESP32

  User->>UI: Click "Turn on Light"
  UI->>API Gateway: POST /task {immediate}
  API Gateway->>Task Service: createImmediateTask()
  Task Service->>Function Service: resolveDeviceAndTopic()
  Function Service->>MQTT Broker: publish(topic, payload)
  MQTT Broker->>ESP32: receive command
  ESP32-->>MQTT Broker: ack status
  MQTT Broker-->>Function Service: status update
```

#### 3.3 Scheduled Task Flow
```mermaid
sequenceDiagram
  participant User
  participant UI
  participant API Gateway
  participant Task Service
  participant Scheduler
  participant Function Service
  participant MQTT Broker
  participant ESP32

  User->>UI: Schedule watering
  UI->>API Gateway: POST /task {schedule}
  API Gateway->>Task Service: storeTask()
  Task Service->>Scheduler: planExecution(time)
  Scheduler->>Function Service: executeAtTime()
  Function Service->>MQTT Broker: publish(topic, payload)
  MQTT Broker->>ESP32: execute command
```

---

### 4. C4 Container Diagram (Level 2)
```mermaid
flowchart TB
    subgraph Client
      A[Mobile/Web UI]
    end

    subgraph Gateway
      B[API Gateway]
    end

    subgraph Services
      C[User Service]
      D[Workspace Service]
      E[Task Service]
      F[Function Service]
    end

    subgraph Broker
      G[MQTT Broker]
    end

    subgraph Devices
      H[ESP32 Controller]
    end

    A --> B
    B --> C
    B --> D
    B --> E
    B --> F
    F --> G
    G --> H
    H --> G
    G --> F
```

---

### 5. Security Considerations
- HTTPS + OAuth2/JWT between client and services
- mTLS or API key auth between services
- TLS-secured MQTT with per-device credentials
- Role-based access (owner, user, guest)
- Each task/function/device scoped per account
