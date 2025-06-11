# GCP DevOps Sandbox

A sandbox FastAPI app used to learn GCP deployment, containerization, CI/CD, and platform tooling.

## Quickstart

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
gcloud app deploy