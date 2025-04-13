from typing import Optional, Literal
from pydantic import BaseModel, EmailStr
from datetime import date

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    hire_date: date
    position: str
    salary: float
    status: Optional[Literal["Active", "Inactive"]] = "Active"

    class Config:
        orm_mode = True

