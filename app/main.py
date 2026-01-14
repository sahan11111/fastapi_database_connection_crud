from typing import List
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from. import models, schemas
from.database import engine, SessionLocal, Base
# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)
app = FastAPI()
# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Root endpoint for basic check
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the FastAPI CRUD API!"}


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, phone_number=user.phone_number, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user