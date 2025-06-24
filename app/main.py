from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import httpx
import yaml

# -----------------------------------------------
# Prometheus Metrics Definitions
# -----------------------------------------------

# Total number of incoming HTTP requests to the API
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of http requests to the FastAPI'
)

# Count of /ping-service requests and failures
PING_SERVICE_COUNT = Counter(
    'ping_service_request_total',
    'Total number of request sent to the /ping-service route'
)
PING_SERVICE_FAILURE = Counter(
    'ping_service_failure_total',
    'Total number of exceptions thrown at the /ping-service route'
)

# Count of /check-status-code requests and failures
CHECK_STATUS_CODE_COUNT = Counter(
    'check_status_code_request_total',
    'Total number of status code requests to the /check-status-code route'
)
CHECK_STATUS_CODE_FAILURE = Counter(
    'check_status_code_failure_total',
    'Total number of exceptions thrown at the /check-status-code route'
)

# Count of submitted YAML files and failed validations
YAML_VALIDATION_COUNT = Counter(
    'yaml_validation_total',
    'Total number of YAML files submitted for validation'
)
YAML_VALIDATION_FAILURE = Counter(
    'yaml_validation_failure_total',
    'Total number of invalid YAML files submitted'
)

# Initialize FastAPI app
app = FastAPI()

# -----------------------------------------------
# Health Check / Root Endpoint
# -----------------------------------------------

@app.get("/")
def read_root():
    """
    Basic health check endpoint.
    Returns API metadata.
    """
    REQUEST_COUNT.inc()
    return {
        "tool": "GCP DevOps Sandbox",
        "version": "0.1",
        "status": "OK"
    }

# -----------------------------------------------
# Prometheus Metrics Endpoint
# -----------------------------------------------

@app.get("/metrics")
def read_metrics():
    """
    Exposes Prometheus-compatible metrics.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# -----------------------------------------------
# Ping External Service
# -----------------------------------------------

@app.get("/ping-service")
async def ping_service(url: str = Query(..., description="The URL to ping")):
    """
    Pings a given URL and returns the status code and response time.
    """
    REQUEST_COUNT.inc()
    PING_SERVICE_COUNT.inc()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)

        return {
            "url": url,
            "status_code": response.status_code,
            "response_time_ms": response.elapsed.total_seconds() * 1000,
        }

    except httpx.RequestError as e:
        PING_SERVICE_FAILURE.inc()
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

# -----------------------------------------------
# Check if External URL Returns 200
# -----------------------------------------------

@app.get("/check-status-code")
async def check_status_code(url: str = Query(..., description="The URL to check the status of")):
    """
    Checks whether the given URL returns HTTP 200.
    """
    REQUEST_COUNT.inc()
    CHECK_STATUS_CODE_COUNT.inc()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)

        return {
            "status_is_ok": response.status_code == 200,
            "status_code": response.status_code,
        }

    except httpx.RequestError as e:
        CHECK_STATUS_CODE_FAILURE.inc()
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

# -----------------------------------------------
# YAML File Validator
# -----------------------------------------------

@app.post("/yaml-validator")
async def yaml_validator(file: UploadFile = File(...)):
    """
    Validates an uploaded YAML file.
    Returns parsed data if valid, or error if invalid.
    """
    REQUEST_COUNT.inc()
    YAML_VALIDATION_COUNT.inc()

    try:
        content = await file.read()
        yaml_data = yaml.safe_load(content)

        return {
            "valid": True,
            "parsed": yaml_data,
        }

    except yaml.YAMLError as e:
        YAML_VALIDATION_FAILURE.inc()
        return {
            "valid": False,
            "error": str(e),
        }
