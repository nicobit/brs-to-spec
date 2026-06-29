from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime
from sqlalchemy.sql import func
from .db import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    arn = Column(String, unique=True, index=True, nullable=False)
    applicant_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    ni_number = Column(String, nullable=True)
    income = Column(Numeric, nullable=True)
    loan_amount = Column(Numeric, nullable=True)
    purpose = Column(String, nullable=True)
    term = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
