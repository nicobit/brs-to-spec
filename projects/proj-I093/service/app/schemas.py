from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ApplicationCreate(BaseModel):
    applicant_name: str
    dob: date
    ni_number: Optional[str] = None
    income: Optional[float] = None
    loan_amount: Optional[float] = None
    purpose: Optional[str] = None
    term: Optional[int] = None


class ApplicationOut(BaseModel):
    arn: str


class StatusOut(BaseModel):
    arn: str
    status: str = Field(default="RECEIVED")
