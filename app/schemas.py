from pydantic import BaseModel


# Schema for creating an item (input model)
class UserCreate(BaseModel):
    name: str
    phone_number: str
    email: str


# Schema for reading/returning an item (output model)

class User(BaseModel):
    id: int
    name: str
    phone_number: str
    email: str

    class Config:
        # Enable ORM mode to allow Pydantic to read data from SQLAlchemy ORM objects
        orm_mode = True
        # from_attributes = True # For Pydantic v2.x (use this if you have Pydantic v2+)