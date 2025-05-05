from typing import Optional, Literal
from pydantic import BaseModel, EmailStr
from datetime import date

class EmployeeBase(BaseModel):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class EmployeeCreate(EmployeeBase):
    first_name: str
    last_name: str
    email: EmailStr
    hire_date: date
    position: str
    salary: float
    status: Optional[Literal["Active", "Inactive"]] = "Active"

class EmployeeUpdate(EmployeeBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    hire_date: Optional[date] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    status: Optional[Literal["Active", "Inactive"]] = "Active"

class EmployeeResponse(EmployeeBase):
    first_name: str
    last_name: str
    email: EmailStr
    hire_date: date
    position: str
    salary: float
    status: str



