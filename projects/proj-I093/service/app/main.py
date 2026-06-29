from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from . import db, schemas, crud
from .db import SessionLocal, init_db
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Proj I093 - Intake Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db_sess = SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/intake", response_model=schemas.ApplicationOut)
def intake(application: schemas.ApplicationCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # basic validation: applicant_name and dob required by schema
    try:
        db_app = crud.create_application(db, application)
    except Exception as e:
        logger.exception("Error creating application")
        raise HTTPException(status_code=500, detail="internal error")

    # enqueue background work (stub)
    background_tasks.add_task(_enqueue_application, db_app.arn)

    return {"arn": db_app.arn}


@app.get("/status", response_model=schemas.StatusOut)
def status(arn: str, dob: str, db: Session = Depends(get_db)):
    db_app = crud.get_application_by_arn(db, arn)
    if not db_app:
        raise HTTPException(status_code=404, detail="not found")
    # basic dob check (string compare to stored date isoformat)
    if str(db_app.dob) != dob:
        raise HTTPException(status_code=404, detail="not found")
    return {"arn": db_app.arn, "status": "RECEIVED"}


def _enqueue_application(arn: str):
    # In a real system this would publish to Service Bus / Kafka.
    logger.info(f"Enqueued application {arn} for scoring (stub)")
