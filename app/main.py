from fastapi import FastAPI
from fastapi import HTTPException, Query
from fastapi import UploadFile, File
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import httpx
import yaml

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of http requests to the FastAPI'
)

PING_SERVICE_COUNT = Counter(
    'ping_service_request_total',
    'Total number of request sent to the /ping-service route'
)

CHECK_STATUS_CODE_COUNT = Counter(
    'check_status_code_request_total',
    'Total number of status code requests to the /check-status-code route'
)

PING_SERVICE_FAILURE = Counter(
    'ping_service_failure_total',
    'Total number of exceptions thrown at the /ping-service route'
)

CHECK_STATUS_CODE_FAILURE = Counter(
    'check_status_code_failure_total',
    'Total number of exceptions thrown at the /check-status-code route'
)

YAML_VALIDATION_COUNT = Counter(
    'yaml_validation_total',
    'Total number of YAML files submitted for validation'
)

YAML_VALIDATION_FAILURE = Counter(
    'yaml_validation_failure_total',
    'Total number of invalid YAML files submitted'
)

app = FastAPI()

@app.get("/")
def read_root():
    REQUEST_COUNT.inc()
    return {
        "tool": "GCP DevOps Sandbox",
        "version": "0.1",
        "status": "OK"
    }

@app.get('/metrics')
def read_metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get('/ping-service')
async def ping_service(url: str = Query(..., description='The Url to ping')):
    PING_SERVICE_COUNT.inc()
    REQUEST_COUNT.inc()

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


@app.get('/check-status-code')
async def check_status_code(url: str = Query(..., description="The url to check the status of")):
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

@app.post('/yaml-validator')
async def yaml_validator(file: UploadFile = File(...)):
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
