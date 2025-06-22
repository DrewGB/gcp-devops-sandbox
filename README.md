# GCP DevOps Sandbox

A self-contained sandbox application built with FastAPI, designed to demonstrate modern DevOps workflows, including:

- Containerization with Docker
- Deployment to Google Cloud Platform (GCP)
- Prometheus-style metrics exposure
- CI/CD integration readiness

This project is part of a self-guided bootcamp focused on gaining practical experience relevant to a DevOps/Platform Engineering role.

## Features

* FastAPI: Minimal modern Python framework for rapid API development
* Dockerized: Lightweight docker container setup
* GCP App Engine: Deployable with a single gcloud command
* /metrics Route: Provides Prometheus-style metrics
* Health Check Route: / response with status and version information


## Quickstart

### Run Locally

```bash

# Clone the repository
git clone https://github.com/DrewGB/gcp-devops-sandbox.git
cd gcp-devops-sandbox

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload

```

### Run with Docker

```bash
# Build container
docker build -t gcp-devops-sandbox .

# Run the container
docker run -d -p 8000:8000 --name gcp-devops-sandbox-api gcp-devops-sandbox

```

### Deploy via App Engine

```bash
    
gcloud app deploy
    
```
