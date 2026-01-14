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


@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if phone number already exists
    existing_user = db.query(models.User).filter(
        models.User.phone_number == user.phone_number
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Phone number already registered"
        )
    
    # Check if email already exists (if email is also unique)
    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    if existing_email:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    # Create new user
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name=user.name
    db_user.phone_number=user.phone_number
    db_user.email=user.email
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return ("Successfully deleted")