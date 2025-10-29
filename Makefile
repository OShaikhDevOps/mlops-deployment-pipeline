# Makefile for common tasks
.PHONY: venv install train serve lint test compose

venv:
	python -m venv .venv

install: venv
	. .venv/Scripts/activate && pip install --upgrade pip && pip install -r requirements.txt

train:
	python -c "from src import train; train.train_and_log(quick=False)"

train-quick:
	python -c "from src import train; train.train_and_log(quick=True)"

serve:
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

compose:
	cd infra && docker-compose up -d --build

test:
	pytest -q
