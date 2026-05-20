from pydantic import BaseModel, field_validator
from typing import Optional, List, Literal
from datetime import date

# Specific statuses allowed by Page 14
OrderStatus = Literal['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']

class OrderBase(BaseModel):
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: OrderStatus
    comments: Optional[str] = None
    customerNumber: int

class OrderCreate(OrderBase):
    orderNumber: int # PK provided by client

class OrderUpdate(BaseModel):
    # Useful for updating status or shipping date as per Page 14
    shippedDate: Optional[date] = None
    status: Optional[OrderStatus] = None
    comments: Optional[str] = None

class OrderOut(OrderBase):
    orderNumber: int
    class Config:
        from_attributes = True

# Requirement: requiredDate must be after orderDate
class OrderCreateRequest(OrderCreate):
    @field_validator('requiredDate')
    @classmethod
    def validate_dates(cls, v, info):
        if 'orderDate' in info.data and v < info.data['orderDate']:
            raise ValueError('requiredDate must be after orderDate')
        return v