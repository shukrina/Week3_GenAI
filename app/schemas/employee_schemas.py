from pydantic import BaseModel, EmailStr
from typing import Optional, List

class EmployeeBase(BaseModel):
    lastName: str
    firstName: str
    extension: str
    email: EmailStr  # Validates email format automatically
    officeCode: str
    reportsTo: Optional[int] = None
    jobTitle: str

class EmployeeCreate(EmployeeBase):
    employeeNumber: int  # Provided by client

class EmployeeUpdate(BaseModel):
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    extension: Optional[str] = None
    email: Optional[EmailStr] = None
    officeCode: Optional[str] = None
    reportsTo: Optional[int] = None
    jobTitle: Optional[str] = None

class EmployeeOut(EmployeeBase):
    employeeNumber: int
    class Config:
        from_attributes = True