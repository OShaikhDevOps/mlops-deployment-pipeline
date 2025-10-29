# End-to-End ML Deployment Pipeline with MLOps Practices

Designed and implemented a scalable MLOps pipeline for deploying machine learning models with CI/CD automation, monitoring, and reproducibility in production.

## Overview

This repository contains a reference implementation of an end-to-end MLOps pipeline that takes models from experimentation to production with reproducible training, artifact versioning, CI/CD, containerized serving, and monitoring.

Key features:
- Data versioning using DVC
- Experiment tracking using MLflow
- Containerized serving with FastAPI and Docker
- CI with GitHub Actions
- Terraform skeleton for infra (S3, ECS/Fargate)
- Prometheus metrics endpoint for monitoring

See the `src/` directory for training and serving code, `dvc.yaml` for pipeline stages, and `.github/` for CI.

---

Quick start (local):

1. Create a virtual environment and install dependencies:

   python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt

2. Train a quick model locally:

   python src/train.py

3. Run the API locally:

   uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

4. Predict:

   POST http://localhost:8000/predict with JSON {"features": [..]}


Notes:
- This repository provides a reference implementation and examples. Adapt storage, registry, and infrastructure to your environment.
- For production use, configure MLflow tracking server, DVC remote storage, and CI secrets.

Licensed under MIT.
