from sqlalchemy.orm import Session
from . import models, schemas, arn as arn_lib


def create_application(db: Session, app_in: schemas.ApplicationCreate) -> models.Application:
    arn = arn_lib.generate_arn()
    db_obj = models.Application(
        arn=arn,
        applicant_name=app_in.applicant_name,
        dob=app_in.dob,
        ni_number=app_in.ni_number,
        income=app_in.income,
        loan_amount=app_in.loan_amount,
        purpose=app_in.purpose,
        term=app_in.term,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_application_by_arn(db: Session, arn: str):
    return db.query(models.Application).filter(models.Application.arn == arn).first()
