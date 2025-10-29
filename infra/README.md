# Local infra (docker-compose)

This directory contains a docker-compose file that brings up a local dev stack:
- `app` - the model serving FastAPI app (built from repo)
- `mlflow` - local MLflow tracking server
- `prometheus` - metrics scraper
- `grafana` - dashboarding

Quick start (from repo root):

```powershell
cd infra
docker-compose up -d --build
```

Visit:
- FastAPI app: http://localhost:8000
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000  (admin/admin)

