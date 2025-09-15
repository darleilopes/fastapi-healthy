# FastAPI Healthy

This is an example of REST API with FastAPI, designed to be executed at Kubernetes with observability focus and metrics.

## About the project

The **FastAPI Healthy** is an example application that shows how to create a REST api with FastAPI, with these features:

- **Observability** metrics to be used with Prometheus
- **Health checks** to be used at Kubernetes
- **Containerization** optimized with multi-stage build
- **Documentation** automatic for OpenAPI/Swagger

## Funcions

- **Health Check** - Endpoint `/healthz` to check healthy
- **Greeting API** - Endpoint `/greet` to personalized greeting
- **Prometheus metrics** - Endpoint `/metrics` with personalized metrics
- **Automatic documentation** - Swagger UI em `/docs`
- **Validation** - Entry validation with [Pydantic](https://docs.pydantic.dev/latest/)
- **Error Handling** - Peronalized errors
- **Middlewares** - Automatic HTTP metrics collections

## Project structure

```
fastapi-healthy/
├── app/                          # app source code
│   ├── __init__.py
│   ├── main.py                   # main FastAPI app
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   ├── router.py             # principal router
│   │   └── v1/                   # API v1
│   │       ├── __init__.py
│   │       └── endpoints/        # API endpoints
│   │           ├── __init__.py
│   │           ├── health.py     # Health check
│   │           ├── greet.py      # Greeting endpoint
│   │           └── metrics.py    # Metrics endpoint (Prometheus)
│   ├── config/                   # Configuration layer
│   │   ├── __init__.py
│   │   └── settings.py           # Settings
│   ├── core/                     # Central logic layer
│   │   ├── __init__.py
│   │   └── metrics.py            # metric system
│   └── models/                   # data layer
│       ├── __init__.py
│       └── responses.py          # responde model
├── requirements.txt              # Python dependencies
└── run.py                        # Execution script
```

## Install and execution

### Requirements

- Python 3.12 or higer
- pip (Python package manager)

### Local instalation

1. **Clone the repository:**
```bash
git clone https://github.com/darleilopes/fastapi-healthy.git
cd fastapi-healthy
```

2. **Creating venv:**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Depedency install:**
```bash
pip install -r requirements.txt
```

4. **App execution:**
```bash
python run.py
```

For dev, you can use auto-reload:
```bash
python run.py --reload
```

The application listen at: http://localhost:8000

### Using Docker

1. **Build the image:**
```bash
./docker-build.sh
```

2. **Container execution:**
```bash
docker run -p 8000:8000 fastapi-healthy:latest
```

## API endpoints

### Root
- **GET /** - App information

### Health Check
- **GET /api/v1/healthz** - Check app healthy
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-09-12T10:30:00Z",
    "version": "1.0.0"
  }
  ```

### Greeting
- **GET /api/v1/greet?name=Pedro** - Personalized greeting
  ```json
  {
    "message": "Hello, Pedro!",
    "name": "Pedro",
    "timestamp": "2025-09-12T10:30:00Z"
  }
  ```

### Metrics
- **GET /api/v1/metrics** - Prometheus metrics format

### Documentation
- **GET /docs** - Interactive Swagger UI documentation
- **GET /redoc** - ReDoc documentation
- **GET /openapi.json** - Schema OpenAPI

## Samples requests (cURL)

### **Root - app info**
```bash
# To get app info
curl -X GET http://localhost:8000/
```

**Response:**
```json
{
  "app": "FastAPI Healthy",
  "version": "1.0.0",
  "environment": "development",
  "docs_url": "/docs",
  "health_url": "/api/v1/healthz",
  "metrics_url": "/api/v1/metrics"
}
```

### **Health Check**
```bash
# Check the api health
curl -X GET http://localhost:8000/api/v1/healthz
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-12T10:30:00Z",
  "version": "1.0.0"
}
```

### **Custom greeting**

**With name:**
```bash
# To great a particular name
curl -X GET "http://localhost:8000/api/v1/greet?name=João"
```

**Response:**
```json
{
  "message": "Hello, Pedro!",
  "name": "Pedro",
  "timestamp": "2025-09-12T10:30:00Z"
}
```

**Standard greeting:**
```bash
# With no name
curl -X GET http://localhost:8000/api/v1/greet
```

**Resposta:**
```json
{
  "message": "Hello, you!",
  "name": "you",
  "timestamp": "2025-09-12T10:30:00Z"
}
```

**Others examples:**
```bash
# Testing with different names
curl -X GET "http://localhost:8000/api/v1/greet?name=Darlei"
curl -X GET "http://localhost:8000/api/v1/greet?name=DevOps"
curl -X GET "http://localhost:8000/api/v1/greet?name=Kubernetes"
```

### **Prometheus**
```bash
# TO get all metrics
curl -X GET http://localhost:8000/api/v1/metrics
```

**Example of response:**
```prometheus
# HELP http_requests_total Total request of HTTP
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/healthz",status="200"} 15.0
http_requests_total{method="GET",endpoint="/greet",status="200"} 8.0

# HELP http_request_duration_seconds Duração de requisições HTTP em segundos
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{method="GET",endpoint="/healthz",le="0.005"} 10.0
http_request_duration_seconds_bucket{method="GET",endpoint="/healthz",le="0.01"} 15.0

# HELP system_cpu_usage_percent Porcentagem de uso de CPU do sistema
# TYPE system_cpu_usage_percent gauge
system_cpu_usage_percent 23.5

# HELP greet_requests_total Total de requisições de saudação
# TYPE greet_requests_total counter
greet_requests_total{name="João"} 3.0
greet_requests_total{name="Maria"} 2.0
greet_requests_total{name="World"} 5.0
```

## Docker

### Image build

This project contains a **Dockerfile multi-stage** optimized:

```bash
./docker-build.sh

# Manual build
docker build -t fastapi-healthy:latest .
```

### Executing the container

```bash
# Simple execution
docker run -p 8000:8000 fastapi-healthy:latest

# Executing including env vars
docker run -p 8000:8000 \
  -e APP_NAME="My API" \
  -e DEBUG=true \
  fastapi-healthy:latest

# Daemon mode
docker run -d -p 8000:8000 --name api-healthy fastapi-healthy:latest
```

## Endpoints metrics

The endpoint `/metrics` allow us to have access to complete metrics:

### App total metrics
- `http_requests_total`
- `http_request_duration_seconds`
- `greet_requests_total`
- `health_checks_total`
- `app_info`

### System metrics
- `system_cpu_usage_percent`
- `system_memory_usage_bytes`
- `system_disk_usage_bytes`
- `system_load_average`
- `system_uptime_seconds`

### Process metrics
- `process_cpu_usage_percent`
- `process_memory_usage_bytes`
- `process_open_file_descriptors`
- `process_threads_total`


## **Running tests**

### **Running tests using containers**

Execute all tests in a isolated environment and clean:

```bash
# With coverage
docker run --rm -v "$(pwd)":/app -w /app python:3.12 bash -c "
  apt-get update && apt-get install -y gcc python3-dev && 
  pip install --no-cache-dir -r requirements-dev.txt && 
  python -m pytest tests/ -v --cov=app --cov-report=term-missing --cov-fail-under=80
"

# Without coverage
docker run --rm -v "$(pwd)":/app -w /app python:3.12 bash -c "
  apt-get update && apt-get install -y gcc python3-dev && 
  pip install --no-cache-dir -r requirements-dev.txt && 
  python -m pytest tests/ -v
"
```

### **Local tests (using venv)**

```bash
# 1. Creating venv
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 2. Install deps
pip install --upgrade pip
pip install -r requirements-dev.txt

# 3. Running full tests
python -m pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=80

# 4. Check coverage report
open htmlcov/index.html  # macOS
# xdg-open htmlcov/index.html  # Linux
```

### **Specific tests**

```bash
python -m pytest tests/api/ -v                    # API tests
python -m pytest tests/core/ -v                   # core tests
python -m pytest tests/models/ -v                 # models tests
python -m pytest tests/config/ -v                 # config tests

# by endpoints
python -m pytest tests/api/v1/test_health.py -v   # Health check
python -m pytest tests/api/v1/test_greet.py -v    # Greeting
python -m pytest tests/api/v1/test_metrics.py -v  # Metrics

# Running a particular test
python -m pytest tests/api/test_main.py::TestMainApplication::test_root_endpoint -v

# Testing with marks
python -m pytest -m "not slow" -v                 # Exclude the slow tests
python -m pytest -m "api" -v                      # Only the API
```

## **CI/CD Pipelines**

This project uses a robust CI/CD pipeline with GitHub Actions that ensures code quality, security, and automated deployment.

### **Pipeline Flow**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                               CI/CD PIPELINE FLOW                           │
└─────────────────────────────────────────────────────────────────────────────┘

   Push to main/develop        Push tags            Manual trigger
           │                        │                      │
           ▼                        │                      │
┌─────────────────┐                 │                      │
│   CI Pipeline   │                 │                      │
│   (.github/     │                 │                      │
│   workflows/    │                 │                      │
│   ci.yml)       │                 │                      │
└─────────────────┘                 │                      │
           │                        │                      │
    If Success                      │                      │
           │                        │                      │
           ▼                        ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CD Pipeline                                    │
│                        (.github/workflows/cd.yml)                           │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           ▼
    Stores at ghcr.io/darleilopes/fastapi-healthy:main
```

### **Published Images**

**Registry:** GitHub Container Registry (GHCR)

**Available Tags:**
- `ghcr.io/darleilopes/fastapi-healthy:main` - Latest main branch
- `ghcr.io/darleilopes/fastapi-healthy:latest` - Same as main
- `ghcr.io/darleilopes/fastapi-healthy:main-<sha>` - Specific commit

**Usage:**
```bash
# Pull the image
docker pull ghcr.io/darleilopes/fastapi-healthy:main

# Run the application
docker run -p 8000:8000 ghcr.io/darleilopes/fastapi-healthy:main

# Access the API
curl http://localhost:8000/api/v1/healthz
```

## **Running using Kind**

To execute this project, spin up a Kind cluster (you should have it cloned):
```
kind create cluster \
  --config=kind/kind-config.yaml \
  --name=fastapi-healthy
```

And make the switch to cluster:
```
kubectl cluster-info --context kind-fastapi-healthy
```

Now clone the image and load into the kind:
```
# image pull
docker pull ghcr.io/darleilopes/fastapi-healthy:main

# load into Kind
kind load docker-image ghcr.io/darleilopes/fastapi-healthy:main --name=fastapi-healthy

# Check if it has been loaded
docker exec -it fastapi-healthy-control-plane crictl images | grep fastapi-healthy
```

Also install NGIX ingress:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Wait for the controller being ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

Then deploy the app:
```
kubectl apply -f kind/fastapi-deploy.yaml 
```

And update your /etc/hosts:
```
echo "127.0.0.1 fastapi-healthy.local" | sudo tee -a /etc/hosts
```

Now you can make the tests:
```
curl http://fastapi-healthy.local:8080/api/v1/healthz
curl http://fastapi-healthy.local:8080/api/v1/metrics
curl "http://fastapi-healthy.local:8080/api/v1/greet?name=Kind"
```

You also can check and test the others endpoints listed [above](#api-endpoints)