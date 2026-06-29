# Proj I093 - Intake Service (scaffold)

This is a minimal FastAPI scaffold for the E-001 Application Intake service.

Run locally:

```powershell
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```powershell
pytest -q
```
