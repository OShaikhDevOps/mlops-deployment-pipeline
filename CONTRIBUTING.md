# Contributing

Thanks for your interest in contributing to this MLOps deployment pipeline reference.

Getting started:

1. Create a branch for your work:

   git checkout -b feature/your-feature

2. Run the unit tests locally (recommended Python 3.11):

   python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
   pytest -q

Notes:
- The repo includes a `quick` training mode that avoids heavy compiled dependencies. Tests and CI use this mode to keep runs fast and portable.
- Do not commit model artifacts or dataset files. Use DVC to track large data and configure a remote.
- Open a pull request against `dev` and request at least one reviewer.
