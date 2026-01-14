from pydantic import BaseModel, EmailStr, Field, field_validator
import re
# Schema for creating an item (input model)


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    phone_number: str = Field(..., min_length=10, max_length=15, description="User's phone number")
    email: EmailStr = Field(..., description="User's email address")
    

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone_number": "9876543210",
                "email": "john@example.com"
            }
        }


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