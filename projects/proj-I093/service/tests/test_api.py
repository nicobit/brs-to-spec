import os
import tempfile
from fastapi.testclient import TestClient
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.main import app


client = TestClient(app)


def test_intake_and_status():
    payload = {
        "applicant_name": "Alice Example",
        "dob": "1990-01-01",
        "ni_number": "AB123456C",
        "income": 50000,
        "loan_amount": 10000,
        "purpose": "Home improvement",
        "term": 36,
    }

    r = client.post("/intake", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "arn" in data

    arn = data["arn"]

    r2 = client.get("/status", params={"arn": arn, "dob": "1990-01-01"})
    assert r2.status_code == 200
    sdata = r2.json()
    assert sdata["arn"] == arn
    assert sdata["status"] == "RECEIVED"
