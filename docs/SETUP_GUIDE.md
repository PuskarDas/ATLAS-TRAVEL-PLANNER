# Setup Guide

## Backend

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

The API runs at `http://localhost:8000`.

## Frontend

PowerShell may block `npm.ps1`, so use `npm.cmd` on Windows:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

The React app runs at `http://localhost:3000`.

## Tests

```powershell
python -m pytest tests -q
```

## ML Training

```powershell
python -m pip install -r ml_training/requirements.txt
python ml_training/scripts/preprocess.py
python ml_training/scripts/train_recommendation_model.py
```
