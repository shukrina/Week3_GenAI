from pydantic import BaseModel
from typing import Optional, List

class OfficeBase(BaseModel):
    city: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    state: Optional[str] = None
    country: str
    postalCode: str
    territory: str

class OfficeCreate(OfficeBase):
    officeCode: str  # PK provided by client

class OfficeUpdate(BaseModel):
    # All fields optional for partial updates
    city: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    territory: Optional[str] = None

class OfficeOut(OfficeBase):
    officeCode: str
    class Config:
        from_attributes = True

# Used for the nested /employees endpoint
from .employee_schemas import EmployeeOut 
class OfficeWithEmployees(OfficeOut):
    employees: List[EmployeeOut] = []