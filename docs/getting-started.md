# KnowGridFlow (EOIP) - Developer Getting Started Guide (S-04)

Welcome to KnowGridFlow (EOIP) - Enterprise Ontology and Operational Intelligence Platform.

## 1. Prerequisites
- Python 3.11+
- Node.js 20+
- Git

## 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/org/KnowGridFlow.git
cd KnowGridFlow

# Create and activate python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install package in editable mode with development tools
pip install -e .[dev]

# Install web application dependencies
cd apps/web
npm install
cd ../..
```

## 3. Running the Development Harness
```bash
# Start backend API (FastAPI)
python -m uvicorn apps.api.main:app --reload --port 8000

# Start frontend development server (Vite)
cd apps/web
npm run dev
```

## 4. Running the Test Suite
```bash
# Run unit tests
pytest tests/unit/

# Run QA Gate Integrity verification
pytest tests/unit/test_qa_gate_integrity.py
```
